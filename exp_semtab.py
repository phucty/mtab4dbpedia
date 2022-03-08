import os.path

from experiments.mtab4d import m_test_semtab, m_test_evaluation
import m_setting as st
import api.utilities.m_iw as iw


def semtab2019():
    for dataset in [st.DATA_VERSION_FIXED, st.DATA_VERSION_ORG]:
        for round_id in [1, 4, 3, 2, 5]:
            for search_mode in ["b", "f", "a"]:
                print(f"Round {round_id} - SearchMode: {search_mode} - Data: {dataset}")
                m_test_semtab(
                    round_id=round_id,
                    n_thread=10,
                    data_version=dataset,
                    search_mode=search_mode,
                )


def print_results():
    run_eval = True
    results = {}
    if os.path.exists(st.dir_eval_res):
        try:
            results = iw.load_obj_pkl(st.dir_eval_res)
            run_eval = False
        except Exception as message:
            iw.print_status(message)
    if run_eval:

        for dataset in [st.DATA_VERSION_ORG, st.DATA_VERSION_FIXED]:
            for round_id in [1, 4, 3, 2, 5]:
                for search_mode in ["b", "f", "a"]:
                    print(
                        f"Round {round_id} - SearchMode: {search_mode} - Data: {dataset}"
                    )
                    eval_res = m_test_evaluation(
                        c_round=round_id, data_version=dataset, search_mode=search_mode
                    )
                    results[(dataset, round_id, search_mode)] = eval_res
        iw.save_obj_pkl(st.dir_eval_res, results)

    # Print SemTab 2019 Org
    dataset = st.DATA_VERSION_ORG
    rounds = [1, 2, 3, 4, 5]
    tasks = ["cea", "cta", "cpa"]
    task_str = {task: [] for task in tasks}
    for search_mode in ["b", "f", "a"]:
        res_round = {}
        for round_id in rounds:
            eval_res = results[(dataset, round_id, search_mode)]
            cea_f1 = "-"
            cea_p = "-"
            cta_ah = "-"
            cta_ap = "-"
            cpa_f1 = "-"
            cpa_p = "-"
            if eval_res.get("res_cea"):
                cea_f1 = eval_res.get("res_cea").get("f1")
                cea_p = eval_res.get("res_cea").get("precision")
            if eval_res.get("res_cpa"):
                cpa_f1 = eval_res.get("res_cpa").get("f1")
                cpa_p = eval_res.get("res_cpa").get("precision")
            if eval_res.get("res_cta"):
                cta_ah = eval_res.get("res_cta").get("ah")
                cta_ap = eval_res.get("res_cta").get("ap")
            res_round[round_id] = [cea_f1, cea_p, cta_ah, cta_ap, cpa_f1, cpa_p]
            for i, to_str_value in enumerate(res_round[round_id]):
                if isinstance(to_str_value, float):
                    res_round[round_id][i] = f"{to_str_value:.3f}"

        cea_f1_str = "\t".join(str(res_round[round_id][0]) for round_id in rounds)
        cea_p_str = "\t".join(str(res_round[round_id][1]) for round_id in rounds)
        task_str["cea"].append(f"MTab4D{search_mode}\t{cea_f1_str}\t{cea_p_str}")

        cta_ah_str = "\t".join(str(res_round[round_id][2]) for round_id in rounds)
        cta_ap_str = "\t".join(str(res_round[round_id][3]) for round_id in rounds)
        task_str["cta"].append(f"MTab4D{search_mode}\t{cta_ah_str}\t{cta_ap_str}")

        cpa_f1_str = "\t".join(str(res_round[round_id][4]) for round_id in rounds)
        cpa_p_str = "\t".join(str(res_round[round_id][5]) for round_id in rounds)
        task_str["cpa"].append(f"MTab4D{search_mode}\t{cpa_f1_str}\t{cpa_p_str}")

    for task, task_lines in task_str.items():
        iw.print_status(f"Tasks: {task}")
        for task_line in task_lines:
            iw.print_status(task_line)

    # Print on adapted dataset
    task_str = {task: [] for task in tasks}
    datasets = [st.DATA_VERSION_ORG, st.DATA_VERSION_FIXED]
    for search_mode in ["b", "f", "a"]:
        res_round = {}
        for round_id in rounds:
            res_dataset = {}
            for dataset in datasets:
                eval_res = results[(dataset, round_id, search_mode)]
                cea_f1 = "-"
                cta_ah = "-"
                cpa_f1 = "-"
                if eval_res.get("res_cea"):
                    cea_f1 = eval_res.get("res_cea").get("f1")
                if eval_res.get("res_cpa"):
                    cpa_f1 = eval_res.get("res_cpa").get("f1")
                if eval_res.get("res_cta"):
                    cta_ah = eval_res.get("res_cta").get("ah")
                res_round[dataset] = [cea_f1, cta_ah, cpa_f1]

                for i, to_str_value in enumerate(res_round[dataset]):
                    if isinstance(to_str_value, float):
                        res_round[dataset][i] = f"{to_str_value:.3f}"

            res_dataset = []
            for i in range(3):

                combine_str = f"{res_round[st.DATA_VERSION_ORG][i]}\t{res_round[st.DATA_VERSION_FIXED][i]}"
                if (
                    len(res_round[st.DATA_VERSION_ORG][i]) == 5
                    and len(res_round[st.DATA_VERSION_FIXED][i]) == 5
                ):
                    ratio = (
                        float(res_round[st.DATA_VERSION_FIXED][i])
                        / float(res_round[st.DATA_VERSION_ORG][i])
                        - 1
                    ) * 100
                    if ratio > 0:
                        combine_str += f" (+{ratio:.2f}%)"
                    else:
                        combine_str += f" ({ratio:.2f}%)"

                res_dataset.append(combine_str)

            res_round[round_id] = res_dataset

        cea_f1_str = "\t".join(str(res_round[round_id][0]) for round_id in rounds)
        task_str["cea"].append(f"MTab4D{search_mode}\t{cea_f1_str}")

        cta_ah_str = "\t".join(str(res_round[round_id][1]) for round_id in rounds)
        task_str["cta"].append(f"MTab4D{search_mode}\t{cta_ah_str}")

        cpa_f1_str = "\t".join(str(res_round[round_id][2]) for round_id in rounds)
        task_str["cpa"].append(f"MTab4D{search_mode}\t{cpa_f1_str}")

    for task, task_lines in task_str.items():
        iw.print_status(f"Tasks: {task}")
        for task_line in task_lines:
            iw.print_status(task_line)


def semtab2021(round_id=5, search_mode="f", dataset="semtab2021"):
    print(f"Round {round_id} - SearchMode: {search_mode} - Data: {dataset}")
    m_test_semtab(
        round_id=round_id, n_thread=4, data_version=dataset, search_mode=search_mode,
    )


if __name__ == "__main__":
    semtab2019()
    print_results()
