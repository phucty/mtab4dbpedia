from experiments.mtab4d import MTab4D, m_test_evaluation, m_test_semtab
from api.utilities import m_iw
import m_setting as st


def run_examples():
    mtab_api = MTab4D()
    # 1. Entity Search
    print("Search Entity: Tokyo")
    print(mtab_api.search_entity("Tokyo"))

    # 2. Get entity information
    print("Get Entity Information: Tokyo")
    print(mtab_api.get_entity_info("Tokyo"))

    # 3. Table annotation
    # Table v18_665 in Round 4
    print("Table Annotation (with targets): v18_665")
    table_content = m_iw.load_object_csv(
        st.dir_tables.format(data_version=st.DATA_VERSION_ORG, round_id=4)
        + "/v18_665.csv",
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
    print("Table Annotation (without targets): v18_665")
    results_auto = mtab_api.get_table_annotation(
        table_content, table_name="UNKNOWN", predict_target=True
    )
    print(results_auto)

    # 4. Evaluation: Submit annotation results in /results
    # print("Evaluation: Round 1")
    for round_id in [4]:  # ,1, 2, 3, 4,
        for data_version in [
            st.DATA_VERSION_FIXED,
            st.DATA_VERSION_ORG,
        ]:
            for search_mode in ["b", "f", "a"]:
                print(
                    f"Round {round_id} - SearchMode: {search_mode} - Data: {data_version}"
                )
                m_test_evaluation(
                    round_id, data_version=data_version, search_mode=search_mode
                )

    # 5. Numerical labeling
    print("Numerical column labeling: ")
    print(mtab_api.search_numerical_labeling([1.50, 1.51, 1.52, 1.53, 1.54]))


if __name__ == "__main__":
    run_examples()
    m_test_semtab(
        round_id=1,
        data_version=st.DATA_VERSION_FIXED,
        search_mode="a",
        table_name="75367212_2_2745466355267233390",
    )
