DIR_ROOT = "/Users/phuc/git/mtab4dbpedia"

DOMAIN = "https://dbpedia.mtab.app"

# Dataset Directories
dir_tables = DIR_ROOT + "/data/{data_version}/Round {round_id}/tables"

# Target files
dir_cea_tar = (
    DIR_ROOT
    + "/data/{data_version}/Round {round_id}/targets/CEA_Round{round_id}_Targets.csv"
)
dir_cta_tar = (
    DIR_ROOT
    + "/data/{data_version}/Round {round_id}/targets/CTA_Round{round_id}_Targets.csv"
)
dir_cpa_tar = (
    DIR_ROOT
    + "/data/{data_version}/Round {round_id}/targets/CPA_Round{round_id}_Targets.csv"
)

# Ground Truth files
dir_cea_gt = (
    DIR_ROOT
    + "/data/{data_version}/Round {round_id}/gt/CEA_Round{round_id}_Targets.csv"
)
dir_cta_gt = (
    DIR_ROOT
    + "/data/{data_version}/Round {round_id}/gt/CTA_Round{round_id}_Targets.csv"
)
dir_cpa_gt = (
    DIR_ROOT
    + "/data/{data_version}/Round {round_id}/gt/CPA_Round{round_id}_Targets.csv"
)

# Result files
dir_cea_res = DIR_ROOT + "/results/Round {round_id}/{data_version}_cea.csv"
dir_cta_res = DIR_ROOT + "/results/Round {round_id}/{data_version}_cta.csv"
dir_cpa_res = DIR_ROOT + "/results/Round {round_id}/{data_version}_cpa.csv"
