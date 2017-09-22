from CRABClient.UserUtilities import config, getUsernameFromSiteDB
config = config()

config.General.requestName = 'stealth_stop_650_singlino_SYY_AOD'
config.General.workArea = 'crab_projects'
config.General.transferOutputs = True
config.General.transferLogs = True

config.JobType.pluginName = 'Analysis'
config.JobType.psetName = 'step2_RAW2DIGI_RECO_EI_650_SYY.py'
config.JobType.numCores = 4

config.Data.inputDataset = '/stealth_stop_650_singlino_SYY_GENSIM/soha-stealth_stop_650_singlino_SYY_DIGI-c9d8db7dc9aa0d51309bb91832f5f0f2/USER'
config.Data.inputDBS = 'phys03'
config.Data.splitting = 'FileBased'
config.Data.unitsPerJob = 1
config.Data.outLFNDirBase = '/store/user/soha/stealth'
config.Data.publication = True
config.Data.outputDatasetTag = 'stealth_stop_650_singlino_SYY_AOD'

config.Site.storageSite = 'T3_US_FNALLPC'
config.Data.ignoreLocality = True
config.Site.whitelist = ["T2_US_*"]