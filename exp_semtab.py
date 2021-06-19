from experiments.mtab4d import m_test_semtab

for round_id in [1, 2, 3, 4]:
    m_test_semtab(round_id=round_id, n_thread=4, data_version="semtab_org")
    m_test_semtab(
        round_id=round_id, n_thread=4, data_version="semtab_2019_dbpedia_2016-10"
    )
