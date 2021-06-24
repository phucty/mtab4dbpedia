from experiments.mtab4d import m_test_semtab

if __name__ == "__main__":
    for round_id in [1, 2, 3, 4, 5]:
        for data_version in ["semtab_org", "semtab_2019_dbpedia_2016-10"]:
            for search_mode in ["f", "b", "a"]:
                print(
                    f"Round {round_id} - SearchMode: {search_mode} - Data: {data_version}"
                )
                m_test_semtab(
                    round_id=round_id,
                    n_thread=4,
                    data_version=data_version,
                    search_mode=search_mode,
                )
