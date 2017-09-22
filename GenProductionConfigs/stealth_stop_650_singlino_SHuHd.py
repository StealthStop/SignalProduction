import FWCore.ParameterSet.Config as cms
from Configuration.Generator.Pythia8CommonSettings_cfi import *
from Configuration.Generator.Pythia8CUEP8M1Settings_cfi import *

externalLHEProducer = cms.EDProducer("ExternalLHEProducer",
    args = cms.vstring("/cvmfs/cms.cern.ch/phys_generator/gridpacks/slc6_amd64_gcc481/13TeV/madgraph/V5_2.3.3/sus_sms/SMS-StopStop/SMS-StopStop_mStop-650_tarball.tar.xz"),
    nEvents = cms.untracked.uint32(20),
    numberOfParameters = cms.uint32(1),
    outputFile = cms.string('cmsgrid_final.lhe'),
    scriptName = cms.FileInPath('GeneratorInterface/LHEInterface/data/run_generic_tarball_cvmfs.sh')
)
#Link to datacards:
#https://github.com/CMS-SUS-XPAG/GenLHEfiles/tree/151728db3c4512142d9100f929d2b8a60066941e/GridpackWorkflow/production/SMS-StopStop/templatecards

baseSLHATable="""
BLOCK QNUMBERS 5000001 # singlino singlinobar
      1     0  # 3 times electric charge
      2     2  # number of spin states (2S+1)
      3     1  # colour rep (1: singlet, 3: triplet, 6: sextet, 8: octet)
      4     1  # Particle/Antiparticle distinction (0=own anti)
BLOCK QNUMBERS 5000002 # singlet singletbar
      1     0  # 3 times electric charge
      2     1  # number of spin states (2S+1)
      3     1  # colour rep (1: singlet, 3: triplet, 6: sextet, 8: octet)
      4     1  # Particle/Antiparticle distinction (0=own anti)

BLOCK MASS
#     ID code   pole mass in GeV
      1000006    650.0  # m(stop)
      5000001    100.0  # m(singlino)
      5000002    90.0  # m(singlet)
      1000039    1.0  # m(Gravitino)

#         ID            Width
DECAY   1000006     1.00000000E+00   # stop decays
#           BR         NDA      ID1       ID2  
     1.00000000E-00    2           6    5000001       # BR(stop -> top singlino)
#         ID            Width
DECAY   5000001     1.00000000E-03   # singlino decays
#           BR         NDA      ID1       ID2 
     1.00000000E-00    2     5000002   1000039        # BR(singlino -> singlet gravitino)
#         ID            Width
DECAY   5000002     1.00000000E-03   # singlet decays
#           BR         NDA      ID1       ID2 
     1.00000000E-00    2          5        -5        # BR(singlet -> b b~)
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
      'JetMatching:qCut = 68.0', #this is the actual merging scale
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
