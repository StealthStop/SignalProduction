from CRABClient.UserUtilities import config, getUsernameFromSiteDB
config = config()

config.General.requestName = 'stealth_stop_650_singlino_SHuHd_DIGI'
config.General.workArea = 'crab_projects'
config.General.transferOutputs = True
config.General.transferLogs = True

config.JobType.pluginName = 'Analysis'
config.JobType.psetName = 'step1_DIGI_650_SHuHd.py'
config.JobType.numCores = 1
config.JobType.maxMemoryMB = 3900

config.Data.inputDataset = '/stealth_stop_650_singlino_SHuHd_GENSIM/soha-stealth_stop_650_singlino_SHuHd_RAWSIMoutput-d055f8d8080afd807a1d0700c168c320/USER'
config.Data.inputDBS = 'phys03'
config.Data.splitting = 'FileBased'
config.Data.unitsPerJob = 1
config.Data.outLFNDirBase = '/store/user/soha/stealth'
config.Data.publication = True
config.Data.outputDatasetTag = 'stealth_stop_650_singlino_SHuHd_DIGI'

config.Site.storageSite = 'T3_US_FNALLPC'
config.Data.ignoreLocality = True
config.Site.whitelist = ["T2_US_UCSD","T2_US_Wisconsin","T2_US_Nebraska","T2_US_Caltech","T2_US_MIT"]
