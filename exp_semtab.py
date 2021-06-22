from experiments.mtab4d import m_test_semtab

if __name__ == "__main__":
    for round_id in [1, 2, 3, 4, 5]:
        for dataset in ["semtab_org", "semtab_2019_dbpedia_2016-10"]:
            for search_mode in ["b", "f", "a"]:
                print(f"Round {round_id} - SearchMode: {search_mode} - Data:{dataset}")
                m_test_semtab(round_id=round_id, n_thread=4, data_version=dataset)
