from CRABClient.UserUtilities import config, getUsernameFromSiteDB
config = config()

config.General.requestName = 'rpv_stop_350_t3j_uds_MINIAOD'
config.General.workArea = 'crab_projects'
config.General.transferOutputs = True
config.General.transferLogs = True

config.JobType.pluginName = 'Analysis'
config.JobType.psetName = 'step1_PAT_t3j_uds.py'
config.JobType.numCores = 4

config.Data.inputDataset = '/rpv_stop_350_t3j_uds_GENSIM/soha-rpv_stop_350_t3j_uds_AOD-10eb51ad31c82400fba5d8dba97dfe26/USER'
config.Data.inputDBS = 'phys03'
config.Data.splitting = 'FileBased'
config.Data.unitsPerJob = 1
config.Data.outLFNDirBase = '/store/user/soha/rpv'
config.Data.publication = True
config.Data.outputDatasetTag = 'rpv_stop_350_t3j_uds_MINIAOD'

config.Site.storageSite = 'T3_US_FNALLPC'
config.Data.ignoreLocality = True
config.Site.whitelist = ["T2_US_*"]
