import FWCore.ParameterSet.Config as cms
from Configuration.Generator.Pythia8CommonSettings_cfi import *
from Configuration.Generator.Pythia8CUEP8M1Settings_cfi import *

externalLHEProducer = cms.EDProducer("ExternalLHEProducer",
    args = cms.vstring("/cvmfs/cms.cern.ch/phys_generator/gridpacks/slc6_amd64_gcc481/13TeV/madgraph/V5_2.3.3/sus_sms/SMS-StopStop/SMS-StopStop_mStop-550_tarball.tar.xz"),
    nEvents = cms.untracked.uint32(10),
    numberOfParameters = cms.uint32(1),
    outputFile = cms.string('cmsgrid_final.lhe'),
    scriptName = cms.FileInPath('GeneratorInterface/LHEInterface/data/run_generic_tarball_cvmfs.sh')
)
#Link to datacards:
#https://github.com/CMS-SUS-XPAG/GenLHEfiles/tree/151728db3c4512142d9100f929d2b8a60066941e/GridpackWorkflow/production/SMS-StopStop/templatecards

baseSLHATable="""
BLOCK MASS
#     ID code   pole mass in GeV
      1000006    550.0  # m(stop)
      1000022    100.0  # m(~chi_10) 

#         ID            Width
DECAY   1000006     1.00000000E+00   # stop decays
#           BR         NDA      ID1       ID2 
     1.00000000E+00    2     1000022       6        # BR(stop -> ~chi_10 top)

#         ID            Width
DECAY   1000022     1.00000000E-01   # ~chi_10 decays
#           BR         NDA      ID1       ID2       ID3   
     1.00000000E+00     3        2         1         3     # BR(~chi_10 -> u d s) 
"""

generator = cms.EDFilter("Pythia8HadronizerFilter",
  maxEventsToPrint = cms.untracked.int32(1),
  pythiaPylistVerbosity = cms.untracked.int32(1),
  filterEfficiency = cms.untracked.double(1.0),
  pythiaHepMCVerbosity = cms.untracked.bool(False),
  comEnergy = cms.double(13000.),
  PythiaParameters = cms.PSet(
    pythia8CommonSettingsBlock,
    pythia8CUEP8M1SettingsBlock,
    JetMatchingParameters = cms.vstring(
      'JetMatching:setMad = off',
      'JetMatching:scheme = 1',
      'JetMatching:merge = on',
      'JetMatching:jetAlgorithm = 2',
      'JetMatching:etaJetMax = 5.',
      'JetMatching:coneRadius = 1.',
      'JetMatching:slowJetPower = 1',
      'JetMatching:qCut = 64.0', #this is the actual merging scale
      'JetMatching:nQmatch = 5', #4 corresponds to 4-flavour scheme (no matching of b-quarks), 5 for 5-flavour scheme
      'JetMatching:nJetMax = 2', #number of partons in born matrix element for highest multiplicity
      'JetMatching:doShowerKt = off', #off for MLM matching, turn on for shower-kT matching
      '6:m0 = 172.5',
      'Check:abortIfVeto = on',
    ), 
    parameterSets = cms.vstring('pythia8CommonSettings',
      'pythia8CUEP8M1Settings',
      'JetMatchingParameters'
    )
  ),
  SLHATableForPythia8 = cms.string(baseSLHATable),
)
