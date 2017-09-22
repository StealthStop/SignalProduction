from CRABClient.UserUtilities import config, getUsernameFromSiteDB
config = config()

config.General.requestName = 'stealth_stop_350_singlino_SYY_test1_DIGI_V2'
config.General.workArea = 'crab_projects'
config.General.transferOutputs = True
config.General.transferLogs = True

config.JobType.pluginName = 'Analysis'
config.JobType.psetName = 'step1_DIGI_SYY_test1.py'
config.JobType.numCores = 4

config.Data.inputDataset = '/stealth_stop_350_singlino_SYY_test1_GENSIM/soha-stealth_stop_350_singlino_SYY_test1_RAWSIMoutput-3e0ede18a629c4819212ba3ff63fe107/USER'
config.Data.inputDBS = 'phys03'
config.Data.splitting = 'FileBased'
config.Data.unitsPerJob = 100
config.Data.outLFNDirBase = '/store/user/soha/stealth'
config.Data.publication = True
config.Data.outputDatasetTag = 'stealth_stop_350_singlino_SYY_test1_DIGI_V2'

config.Site.storageSite = 'T3_US_FNALLPC'
config.Data.ignoreLocality = True
config.Site.whitelist = ["T2_US*"]
config.Site.blacklist = ["T2_US_Purdue"]
