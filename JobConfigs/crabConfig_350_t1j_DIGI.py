from CRABClient.UserUtilities import config, getUsernameFromSiteDB
config = config()

config.General.requestName = 'rpv_sbottom_350_t1j_DIGI'
config.General.workArea = 'crab_projects'
config.General.transferOutputs = True
config.General.transferLogs = True

config.JobType.pluginName = 'Analysis'
config.JobType.psetName = 'step1_DIGI_t1j.py'
config.JobType.numCores = 1
config.JobType.maxMemoryMB = 3900

config.Data.inputDataset = '/rpv_sbottom_350_t1j_GENSIM/soha-rpv_sbottom_350_t1j_RAWSIMoutput-55104b4d5937852247d11ffb4c97179a/USER'
config.Data.inputDBS = 'phys03'
config.Data.splitting = 'FileBased'
config.Data.unitsPerJob = 1
config.Data.outLFNDirBase = '/store/user/soha/rpv'
config.Data.publication = True
config.Data.outputDatasetTag = 'rpv_sbottom_350_t1j'

config.Site.storageSite = 'T3_US_FNALLPC'
config.Data.ignoreLocality = True
config.Site.whitelist = ["T2_US_UCSD","T2_US_Wisconsin","T2_US_Nebraska","T2_US_Caltech","T2_US_MIT"]
