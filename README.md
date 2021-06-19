MTab4DBpedia 
===========
Tabular data annotation with DBpedia version 2016-10
---

## Features:
### 1. Entity Search
Search relevant entities from DBpedia (2016-10) with BM25 algorithm (k1=1.2, b=0.75) 

Example: the query is Tokyo, and get 20 relevant entities.

**Command:** 
```bash
% curl --request POST --header "Content-Type: application/json" --data '{"q":"Tokyo", "limit":20}' http://119.172.242.147:5000/api/v1/search
```

### 2. Get entity information: 
Get entity information from DBpedia (2016-10). The responded object include DBpedia title, mapping to Wikidata, Wikipedia, label, Aliases, types, pagerank score, entity statements, and literal statements. 

Example: Get information of the entity of Tokyo
**Command:** 
```bash
% curl --request POST --header "Content-Type: application/json" --data '{"q":"Tokyo"}' http://119.172.242.147:5000/api/v1/info
```

### 3. Table annotation:
Table annotation with MTab4DBpedia. Please refer m_main.py on how to use. 

### 4. Evaluation:
Submit annotation file (CEA, CTA, CPA), then get the results. 
Please refer m_main.py on how to use. 


## Reproduce MTab4DBpedia results:
1. Clone MTab4DBpedia, and open project
```bash
git clone https://github.com/phucty/mtab4dbpedia.git
cd mtab4dbpedia
```

2. Create conda environment, activate, and install mtab4dbpedia
```bash
conda create -n mtab4dbpedia python=3.6
conda activate mtab4dbpedia
pip install -r requirements.txt
```

3. Other setup:

- Change DIR_ROOT in m_setting.py to your project directory. Current value is (This is the directory in my laptop)
```
DIR_ROOT = "/Users/phuc/git/mtab4dbpedia"
```

- Please update the DOMAIN also, since it might be changed in the future. 
```
DOMAIN = "http://119.172.242.147:5000"
```

- Uncompress data files
```
data/semtab_2019_dbpedia_2016-10.zip
data/semtab_org.zip
```

4. Run experiment for 4 rounds of SemTab 2019 (original), and SemTab 2019 DBpedia 2016-10
```
python exp_semtab.py
```