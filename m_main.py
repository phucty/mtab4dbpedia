from experiments.mtab4d import MTab4D, m_test_semtab, m_test_evaluation


if __name__ == "__main__":
    mtab_api = MTab4D()
    # 1. Entity Search
    print(mtab_api.search_entity("Tokyo"))

    # 2. Get entity information
    print(mtab_api.get_entity_info("Tokyo"))

    # # 3. Table annotation
    for round_id in [1, 2, 3, 4]:
        m_test_semtab(round_id=round_id, n_thread=4, data_version="semtab_org")
        m_test_semtab(
            round_id=round_id, n_thread=4, data_version="semtab_2019_dbpedia_2016-10"
        )

    # 4. Evaluation
    for round_id in [1, 2, 3, 4]:
        m_test_evaluation(round_id, data_version="semtab_org")
        m_test_evaluation(round_id, data_version="semtab_2019_dbpedia_2016-10")
