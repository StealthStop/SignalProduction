#!/usr/bin/env python

import os, sys, argparse, subprocess, shutil, random, json, math
from time import strftime

# Should seed with system time...
random.seed()

# Generate a cmsDriver command to execute for a given step of the production chain
def generate_cmsdriver_command(step, model, mass, year, fragments, conditions):

    command =  "cmsDriver.py "

    # For the LHEGEN step, pass the generator fragment for the corresponding signal model and mass
    if step == "LHEGEN":
        command += "Configuration/GenProduction/python/%s.py "%(fragments[model][year][mass])
        command += "--customise_commands process.RandomNumberGeneratorService.externalLHEProducer.initialSeed=${SEED} "

    command += "--python_filename %s_%s_cfg.py "%(year,step)
    command += "--eventcontent %s "%(conditions[step]["CONTENT"])
    command += "--datatier %s "%(conditions[step]["TIER"])
    command += "--fileout file:%s_out.root "%(step)
    command += "--conditions %s "%(conditions[step][year]["GT"])

    # For steps that use beamspot configuring, note the difference for 2016
    if step == "LHEGEN" or step == "SIM":
        extra = ""

        if year != "2016":
            extra = "Early"

        command += "--beamspot Realistic25ns13TeV%s%sCollision "%(extra,year)
    
    command += "--geometry DB:Extended "

    # Use the simply-named output ROOT file from the previous step as input for the current step
    if "INSTEP" in conditions[step]: 
        command += "--filein file:./../../%s_out.root "%(conditions[step]["INSTEP"])

    # If doing the PU mixing step, provide a dbs link to sample from
    if step == "DIGIPREMIX":
        command += "--pileup_input '%s' "%(conditions[step][year]["PUMIX"])
        command += "--datamix PreMix --procModifiers premix_stage2 "  

    if step == "HLT":

        # The HLT step uses a menu-like tag as the "step" argument
        command += "--step %s "%(conditions[step][year]["STEP"])

        # The HLT step uses special UL versions of older CMSSW, so command is used to avoid the version check
        command += "--customise_commands 'process.source.bypassVersionCheck = cms.untracked.bool(True)' "

        # For some reason, for 2016, some additional keep and drop commands are provided for the HLT step
        if year == "2016":
            command += "--outputCommand 'keep *_mix_*_*,keep *_genPUProtons_*_*' --inputCommands 'keep *','drop *_*_BMTF_*','drop *PixelFEDChannel*_*_*_*' "
    else:
        command += "--step %s "%(conditions[step]["STEP"])
          
    command += "--era Run2_%s "%(year)

    if step != "LHEGEN" and step != "HLT":
        command += "--runUnscheduled "

    command += "--no_exec --mc -n ${EVENTS} "

    return command

# Write .sh script to be run by each spawned job
def generate_job_steerer(workingDir, year, model, mass, steps):

    scriptFile = open("%s/runJob.sh"%(workingDir), "w")
    scriptFile.write("#!/bin/bash\n\n")
    scriptFile.write("SEED=$1\n")
    scriptFile.write("EVENTS=$2\n\n")
    scriptFile.write("source /cvmfs/cms.cern.ch/cmsset_default.sh\n") 
    scriptFile.write("tar -xf payload.tar.gz\n")
    scriptFile.write("rm payload.tar.gz\n\n")

    # Each job will generate the cmsRun config for each step on the fly
    for step in steps:
        CMSSW_VERSION = conditions[step][year]["CMSSW"]
        command = generate_cmsdriver_command(step, model, mass, year, fragments, conditions)
        scriptFile.write("echo 'Running step %s'\n\n"%(step))
        scriptFile.write("export SCRAM_ARCH=%s\n\n"%(conditions[step][year]["ARCH"]))

        scriptFile.write("if [ ! -d \"%s\" ]\n"%(CMSSW_VERSION))
        scriptFile.write("then\n")
        scriptFile.write("    eval `scramv1 project CMSSW %s`\n"%(CMSSW_VERSION))
        scriptFile.write("fi\n\n")
        
        # Move the copied over generator fragments into the CMSSW folder
        if step == "LHEGEN":
            scriptFile.write("mv Configuration %s/src\n"%(CMSSW_VERSION))

        scriptFile.write("cd %s/src\n"%(CMSSW_VERSION))
        scriptFile.write("eval `scramv1 runtime -sh`\n")
        scriptFile.write("eval `scramv1 b -j 4`\n\n")
        scriptFile.write("%s\n\n"%(command))

        # For most steps, add a bit to the end of the cmsRun config that should allow for random seeding of various processes
        if step != "RECO" and step != "HLT" and step != "MINIAOD":
            scriptFile.write("echo '' >> %s_%s_cfg.py\n"%(year, step))
            scriptFile.write("echo 'from IOMC.RandomEngine.RandomServiceHelper import RandomNumberServiceHelper' >> %s_%s_cfg.py\n"%(year, step))
            scriptFile.write("echo 'randHelper = RandomNumberServiceHelper(process.RandomNumberGeneratorService)' >> %s_%s_cfg.py\n"%(year, step))
            scriptFile.write("echo 'randHelper.resetSeeds('$SEED')' >> %s_%s_cfg.py\n\n"%(year, step))

        if step == "DIGIPREMIX":
            scriptFile.write("mv ./../../pumix.py .\n\n")
            scriptFile.write("sed -i \"1s/^/DUMMY = pumix['%s']\\n/\" %s_%s_cfg.py\n"%(year, year, step))
            scriptFile.write("sed -i \"1s/^/from pumix import pumix\\n/\" %s_%s_cfg.py\n"%(year, step))
            scriptFile.write("sed -i \"s|\\[\'DUMMY\'\\]|DUMMY|g\" %s_%s_cfg.py\n"%(year, step))

        scriptFile.write("%s_START=`eval date`\n"%(step))
        scriptFile.write("cmsRun %s_%s_cfg.py\n\n"%(year, step))
        scriptFile.write("%s_STOP=`eval date`\n"%(step))
        scriptFile.write("mv *.root ../..\n\n")
        scriptFile.write("cd ../..\n\n")
        scriptFile.write("ls -lhrt\n\n\n\n")

    for step in steps:
        scriptFile.write("echo %s_START: $%s_START\n"%(step,step))
        scriptFile.write("echo %s_STOP:  $%s_STOP\n\n"%(step,step))

    scriptFile.write("\n\n\n\nxrdcp -f MINIAOD_out.root %s/%s_%s%s_${SEED}.root 2>&1\n"%(outputDir, year, model, mass))
    scriptFile.close()

# Write Condor submit file 
def generate_condor_submit(workingDir, outputDir, eventsPerJob, specEventsPerJob, njobs):

    condorSubmit = open("%s/condorSubmit.jdl"%(workingDir), "w")
    condorSubmit.write("Executable              =  %s/runJob.sh\n"%(workingDir))
    condorSubmit.write("Universe                =  vanilla\n")
    condorSubmit.write("Requirements            =  OpSys == \"LINUX\" && Arch ==\"x86_64\"\n")
    condorSubmit.write("RequestMemory           =  8 Gb\n")
    condorSubmit.write("RequestCpus             =  4\n")
    condorSubmit.write("should_transfer_files   =  YES\n")
    condorSubmit.write("when_to_transfer_output =  ON_EXIT\n")
    condorSubmit.write("x509userproxy           =  $ENV(X509_USER_PROXY)\n")
    condorSubmit.write("Transfer_Input_Files    =  %s/payload.tar.gz\n\n"%(workingDir))

    for iJob in xrange(0, njobs):
        
        seed = random.randint(0, 2147483647)

        condorSubmit.write("transfer_output_remaps  = \"MINIAOD_out.root = condor/%s/MINIAOD_%d.root\"\n"%(outputDir.split("condor/")[-1], iJob))
        condorSubmit.write("Output                  =  %s/logs/job_%d.stdout\n"%(workingDir, iJob))
        condorSubmit.write("Error                   =  %s/logs/job_%d.stderr\n"%(workingDir, iJob))
        condorSubmit.write("Log                     =  %s/logs/job_%d.log\n"%(workingDir, iJob))

        if iJob == njobs-1:
            condorSubmit.write("Arguments               = %d %d\n"%(seed, eventsPerJob+specEventsPerJob))
        else:
            condorSubmit.write("Arguments       = %d %d\n"%(seed, eventsPerJob))

        condorSubmit.write("Queue\n\n")

    condorSubmit.close()

if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    parser.add_argument("--noSubmit"     , dest="noSubmit"     , help="do not submit to cluster", default=False, action="store_true")
    parser.add_argument("--tag"          , dest="tag"          , help="Unique tag"              , type=str , default="TEST")
    parser.add_argument("--year"         , dest="year"         , help="Which year"              , type=str , required=True)
    parser.add_argument("--model"        , dest="model"        , help="Which model"             , type=str , required=True)
    parser.add_argument("--mass"         , dest="mass"         , help="Which mass"              , type=str , required=True)
    parser.add_argument("--nEvents"      , dest="nEvents"      , help="Number of jobs"          , type=int , required=True)
    parser.add_argument("--eventsPerJob" , dest="eventsPerJob" , help="Script file for step1"   , type=int , default=100)
    #parser.add_argument("--outputDir"    , dest="outputDir"    , help="Location for output"     , type=str , required=True)
    args = parser.parse_args()

    tag          = args.tag
    year         = args.year
    model        = args.model
    mass         = args.mass
    nevents      = args.nEvents
    eventsPerJob = args.eventsPerJob
    noSubmit     = args.noSubmit

    # Get CMSSW environment
    HOME = os.getenv("HOME")
    USER = os.getenv("USER")
    PWD  = os.getenv("PWD")

    baseDir = "%s"%(PWD)
    taskDir = strftime("%Y%m%d_%H%M%S")
    
    #outputDir = args.outputDir
    outputDir = "%s/condor/%s_%s%s%s_%s/output"%(baseDir, tag, year, model, mass, taskDir) 
    workingDir = "%s/condor/%s_%s%s%s_%s"%(baseDir, tag, year, model, mass,  taskDir)
    
    # After defining the directory to work the job in and output to, make them
    #subprocess.call(["eos", "root://cmseos.fnal.gov", "mkdir", "-p", outputDir[23:]])
    if not os.path.isdir(workingDir): os.makedirs(workingDir)
    if not os.path.isdir(outputDir): os.makedirs(outputDir)
    
    if outputDir.split("/")[-1] == "":  outputDir  = outputDir[:-1]
    if workingDir.split("/")[-1] == "": workingDir = workingDir[:-1]

    fragFile = "%s/fragments.json"%(baseDir)
    f = open(fragFile, "r")
    fragments = json.load(f)
    f.close()

    condFile = "%s/conditions.json"%(baseDir)
    f = open(condFile, "r") 
    conditions = json.load(f)
    f.close()

    # Create directories to save logs
    os.makedirs("%s/logs"%(workingDir))

    steps = ["LHEGEN", "SIM", "DIGIPREMIX", "HLT", "RECO", "MINIAOD"]

    shutil.copy2("payload.tar.gz", "%s"%(workingDir))

    # Make the .sh to run the show
    generate_job_steerer(workingDir, year, model, mass, steps)

    njobs = int(math.floor(nevents / eventsPerJob))

    specEventsPerJob = nevents - njobs*eventsPerJob

    # Make the jdl to hold condor's hand
    generate_condor_submit(workingDir, outputDir, eventsPerJob, specEventsPerJob, njobs)

    subprocess.call(["chmod", "+x", "%s/runJob.sh"%(workingDir)])

    if args.noSubmit: quit()
    
    os.system("condor_submit %s/condorSubmit.jdl"%(workingDir))
