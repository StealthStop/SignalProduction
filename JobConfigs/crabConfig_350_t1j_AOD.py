from CRABClient.UserUtilities import config, getUsernameFromSiteDB
config = config()

config.General.requestName = 'rpv_sbottom_350_t1j_AOD'
config.General.workArea = 'crab_projects'
config.General.transferOutputs = True
config.General.transferLogs = True

config.JobType.pluginName = 'Analysis'
config.JobType.psetName = 'step2_RAW2DIGI_RECO_EI_t1j.py'
config.JobType.numCores = 4

config.Data.inputDataset = '/rpv_sbottom_350_t1j_GENSIM/soha-rpv_sbottom_350_t1j-c9d8db7dc9aa0d51309bb91832f5f0f2/USER'
config.Data.inputDBS = 'phys03'
config.Data.splitting = 'FileBased'
config.Data.unitsPerJob = 1
config.Data.outLFNDirBase = '/store/user/soha/rpv'
config.Data.publication = True
config.Data.outputDatasetTag = 'rpv_sbottom_350_t1j_AOD'

config.Site.storageSite = 'T3_US_FNALLPC'
config.Data.ignoreLocality = True
config.Site.whitelist = ["T2_US_*"]
