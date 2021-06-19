import os
from collections import defaultdict
from contextlib import closing
from datetime import timedelta
from time import time
from multiprocessing import Pool

import requests
from requests.packages.urllib3.util.retry import Retry
from requests.adapters import HTTPAdapter
from tqdm import tqdm

from api.utilities import m_iw
import m_setting as st


class MTab4D(object):
    def __init__(self):
        self.DOMAIN = "http://119.172.242.147:5000"  # "http://0.0.0.0:5000"
        self.F_ENTITY_SEARCH = f"{self.DOMAIN}/api/v1/search"
        self.F_GET_ENTITY_INFO = f"{self.DOMAIN}/api/v1/info"
        self.F_MTAB = f"{self.DOMAIN}/api/v1/mtab"
        self.F_EVAL = f"{self.DOMAIN}/api/v1/eval"

        self.session = requests.Session()
        retries = Retry(
            total=2, backoff_factor=1, status_forcelist=[500, 502, 503, 504]
        )
        self.session.mount("https://", HTTPAdapter(max_retries=retries))
        self.session.mount("http://", HTTPAdapter(max_retries=retries))

    def _request(self, func_name, query_args):
        responds = defaultdict()
        try:
            _responds = self.session.post(func_name, json=query_args, timeout=None)
            if _responds.status_code == 200:
                responds = _responds.json()
        except Exception as message:
            print(f"\n{message}\n{str(query_args)}")
        return responds

    def search_entity(self, query_value, limit=20):
        query_args = {
            "q": query_value,
            "limit": limit,
        }
        if not query_value:
            return []
        _responds = self._request(self.F_ENTITY_SEARCH, query_args)

        if _responds and _responds.get("hits"):
            responds = [[r["id"], r["score"]] for r in _responds["hits"]]
        else:
            responds = []
        return responds

    def get_entity_info(self, dbpedia_title):
        if not dbpedia_title:
            return []
        responds = defaultdict()
        query_args = {"q": dbpedia_title}
        _responds = self._request(self.F_GET_ENTITY_INFO, query_args)
        if _responds and _responds.get("info"):
            responds = _responds["info"]
        return responds

    def get_eval(self, round_id, res_cea=None, res_cta=None, res_cpa=None):
        query_args = defaultdict()
        query_args["round"] = round_id
        if res_cea:
            query_args["cea"] = res_cea
        if res_cta:
            query_args["cta"] = res_cta
        if res_cpa:
            query_args["cpa"] = res_cpa

        responds = self._request(self.F_EVAL, query_args)
        return responds

    def get_table_annotation(
        self,
        table_content,
        table_name,
        tar_cea=None,
        tar_cta=None,
        tar_cpa=None,
        round_id=0,
    ):
        query_args = {
            "table_name": table_name,
            "table": table_content,
            "tar_cea": tar_cea,
            "tar_cta": tar_cta,
            "tar_cpa": tar_cpa,
            "round_id": round_id,
        }
        responds = self._request(self.F_MTAB, query_args)
        return responds


def m_test_evaluation(c_round=1, data_version="semtab_2019_dbpedia_2016-10"):
    # start = time()
    res_cea = m_iw.load_object_csv(
        st.dir_cea_res.format(round_id=c_round, data_version=data_version)
    )
    res_cta = m_iw.load_object_csv(
        st.dir_cta_res.format(round_id=c_round, data_version=data_version)
    )
    res_cpa = m_iw.load_object_csv(
        st.dir_cpa_res.format(round_id=c_round, data_version=data_version)
    )
    mtab_api = MTab4D()
    res_a = mtab_api.get_eval(
        c_round,
        res_cea=res_cea,
        res_cta=res_cta,
        res_cpa=res_cpa,
    )
    # iw.print_status(f"{str(timedelta(seconds=round(time() - start)))}")
    print(f"Round {c_round}:")
    if res_a.get("cea"):
        print("    CEA:" + str(res_a.get("cea")))
    if res_a.get("cta"):
        print("    CTA:" + str(res_a.get("cta")))
    if res_a.get("cpa"):
        print("    CPA:" + str(res_a.get("cpa")))


def pool_table_annotation(args):
    try:
        mtab_api = MTab4D()
        # iw.print_status(args.get("table_id"))
        responds = mtab_api.get_table_annotation(
            args["table_content"],
            table_name=args.get("table_id"),
            tar_cea=args.get("tar_cea"),
            tar_cta=args.get("tar_cta"),
            tar_cpa=args.get("tar_cpa"),
            round_id=args.get("round_id"),
        )
        return responds
    except Exception as message:
        return {"status": "Error", "message": message}


def m_test_semtab(round_id=1, data_version="semtab_2019_dbpedia_2016-10", n_thread=1):
    start = time()

    # Load tables
    dir_tables = m_iw.get_files_from_dir(
        st.dir_tables.format(data_version=data_version, round_id=round_id),
        is_sort=True,
        reverse=True,
    )
    tar_cea, tar_cta, tar_cpa = defaultdict(list), defaultdict(list), defaultdict(list)

    # Load target cea
    for line in m_iw.load_object_csv(
        st.dir_cea_tar.format(data_version=data_version, round_id=round_id)
    ):
        table_id, col_i, row_i = line[:3]
        tar_cea[table_id].append([row_i, col_i])

    # Load target cta
    for line in m_iw.load_object_csv(
        st.dir_cta_tar.format(data_version=data_version, round_id=round_id)
    ):
        table_id, col_i = line[:2]
        tar_cta[table_id].append(col_i)

    # Load target cpa
    for line in m_iw.load_object_csv(
        st.dir_cpa_tar.format(data_version=data_version, round_id=round_id)
    ):
        table_id, col_i1, col_i2 = line[:3]
        tar_cpa[table_id].append([col_i1, col_i2])

    # Create input args
    args = []
    for dir_table in dir_tables:
        table_content = m_iw.load_object_csv(dir_table)
        table_id = os.path.splitext(os.path.basename(dir_table))[0]
        args_obj = {
            "table_content": table_content,
            "table_id": table_id,
            "tar_cea": tar_cea.get(table_id),
            "tar_cta": tar_cta.get(table_id),
            "tar_cpa": tar_cpa.get(table_id),
            "round_id": round_id,
        }
        args.append(args_obj)

    # Call MTab4D
    res_cea, res_cta, res_cpa = [], [], []
    with tqdm(total=len(dir_tables)) as p_bar:
        with closing(Pool(processes=n_thread)) as p:
            for output_args in p.imap_unordered(pool_table_annotation, args):
                p_bar.update()
                if not output_args or output_args["status"] == "Error":
                    print("Error POST: Could get POST input")
                    if output_args.get("message"):
                        print(output_args.get("message"))
                    return
                if output_args.get("semantic"):
                    if output_args["semantic"].get("cea"):
                        res_cea.extend(
                            [output_args["table_name"], c, r, a]
                            for r, c, a in output_args["semantic"]["cea"]
                        )
                    if output_args["semantic"].get("cta"):
                        res_cta.extend(
                            [
                                output_args["table_name"],
                                c,
                                " ".join(a),
                            ]
                            for c, a in output_args["semantic"]["cta"]
                        )
                    if output_args["semantic"].get("cpa"):
                        res_cpa.extend(
                            [
                                output_args["table_name"],
                                c1,
                                c2,
                                a,
                            ]
                            for c1, c2, a in output_args["semantic"]["cpa"]
                        )

    # Save annotation files
    m_iw.save_object_csv(
        st.dir_cea_res.format(round_id=round_id, data_version=data_version), res_cea
    )
    m_iw.save_object_csv(
        st.dir_cta_res.format(round_id=round_id, data_version=data_version), res_cta
    )
    m_iw.save_object_csv(
        st.dir_cpa_res.format(round_id=round_id, data_version=data_version), res_cpa
    )
    m_test_evaluation(round_id, data_version=data_version)
    print(f"{str(timedelta(seconds=round(time() - start)))}")
