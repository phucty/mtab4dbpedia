from experiments.mtab4d import MTab4D, m_test_evaluation
from api.utilities import m_iw
import m_setting as st


if __name__ == "__main__":
    mtab_api = MTab4D()

    # 1. Entity Search
    print(mtab_api.search_entity("Tokyo"))

    # 2. Get entity information
    print(mtab_api.get_entity_info("Tokyo"))

    # 3. Table annotation
    # Table v18_665 in Round 4
    table_content = m_iw.load_object_csv(
        st.dir_tables.format(data_version="semtab_org", round_id=4) + "/v18_665.csv",
    )
    # Let provide matching targets (data taken from round 4 dataset)
    tar_cea = [
        [0, 1],
        [1, 1],
        [0, 2],
        [1, 2],
        [0, 3],
        [1, 3],
        [0, 4],
        [1, 4],
        [0, 5],
        [1, 5],
    ]
    tar_cta = [0, 1]
    tar_cpa = [[0, 1], [0, 2], [0, 3]]
    results_targets = mtab_api.get_table_annotation(
        table_content,
        table_name="UNKNOWN",
        tar_cea=tar_cea,
        tar_cta=tar_cta,
        tar_cpa=tar_cpa,
    )
    print(results_targets)

    # Let MTab do automatically predict targets
    results_auto = mtab_api.get_table_annotation(
        table_content, table_name="UNKNOWN", predict_target=True
    )
    print(results_auto)

    # 4. Evaluation: Submit annotation results in /results
    for round_id in [1]:  # , 2, 3, 4, 5
        m_test_evaluation(round_id, data_version="semtab_org")
        m_test_evaluation(round_id, data_version="semtab_2019_dbpedia_2016-10")

    # 5. Numerical labeling
    print(mtab_api.search_numerical_labeling([1.50, 1.51, 1.52, 1.53, 1.54]))
