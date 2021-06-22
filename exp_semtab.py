from experiments.mtab4d import m_test_semtab

if __name__ == "__main__":
    for round_id in [1, 2, 3, 4]:
        print(f"Round {round_id}")
        print("SemTab 2019: Original")
        m_test_semtab(round_id=round_id, n_thread=4, data_version="semtab_org")
        print("SemTab 2019: DBpedia 2016-10")
        m_test_semtab(
            round_id=round_id, n_thread=4, data_version="semtab_2019_dbpedia_2016-10"
        )
