DIR_ROOT = "/Users/phucnguyen/git/mtab4dbpedia"

DOMAIN = "https://dbpedia.mtab.app"  # "http://192.168.0.12:5000/"  #

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
    DIR_ROOT + "/data/{data_version}/Round {round_id}/gt/CEA_Round{round_id}_gt.csv"
)
dir_cta_gt = (
    DIR_ROOT + "/data/{data_version}/Round {round_id}/gt/CTA_Round{round_id}_gt.csv"
)
dir_cpa_gt = (
    DIR_ROOT + "/data/{data_version}/Round {round_id}/gt/CPA_Round{round_id}_gt.csv"
)

# Result files
dir_cea_res = (
    DIR_ROOT + "/results/Round {round_id}/{data_version}_{search_mode}_cea.csv"
)
dir_cta_res = (
    DIR_ROOT + "/results/Round {round_id}/{data_version}_{search_mode}_cta.csv"
)
dir_cpa_res = (
    DIR_ROOT + "/results/Round {round_id}/{data_version}_{search_mode}_cpa.csv"
)
dir_eval_res = DIR_ROOT + "/results/eval_results.pkl"

DATA_VERSION_ORG = "semtab_org"
DATA_VERSION_FIXED = "semtab_2019_dbpedia_2016-10"

# DBpedia
DBR = "http://dbpedia.org/resource/"
DBR1 = "http://dbpedia.org/page/"
DBR2 = "Http://dbpedia.org/page/"
DBO = "http://dbpedia.org/ontology/"
DBP = "http://dbpedia.org/property/"

# DIR_W_ITEMS = f"{DIR_MODELS}/wiki_items.lmdb"
