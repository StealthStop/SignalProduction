from WMCore.Configuration import Configuration
config = Configuration()

config.section_("General")
config.General.requestName = 'stealth_stop_350_singlino_SYY_test1'
config.General.workArea = 'crab_projects'

config.section_("JobType")
config.JobType.pluginName = 'PrivateMC'
config.JobType.psetName = 'stealth_stop_350_singlino_SYY_py_LHE_GEN_SIM.py'
config.JobType.allowUndistributedCMSSW = True

config.section_("Data")
# config.Data.primaryDataset = 'MinBias'
config.Data.outputPrimaryDataset = 'stealth_stop_350_singlino_SYY_test1_GENSIM'
config.Data.splitting = 'EventBased'
config.Data.unitsPerJob = 10
NJOBS = 2  # This is not a configuration parameter, but an auxiliary variable that we use in the next line.
config.Data.totalUnits = config.Data.unitsPerJob * NJOBS
config.Data.outLFNDirBase = '/store/user/soha/stealth/stealth_stop_350_singlino_SYY_test1_GENSIM'
config.Data.publication = True
#config.Data.publishDataName = 'CMSDAS2017_CRAB3_MC_generation_test0'
config.Data.outputDatasetTag = 'stealth_stop_350_singlino_SYY_test1'

config.section_("Site")
config.Site.storageSite = 'T3_US_FNALLPC'
