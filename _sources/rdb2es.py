__encode__ = 'UTF-8'
__license__ = 'DataMarketingKorea'
__author__ = 'MS'
__title__ = '22/1Q Study 네이버 블로그 RDB2ES'
"""
* 수정이력
    2022-03-27      MS    최초작성
"""
import os
import copy
import time
import traceback
from datetime import datetime, timedelta
import psycopg2 as pg
import numpy as np
import pandas as pd
import pandas.io.sql as psql
from elasticsearch import Elasticsearch, helpers


class RDB2ES:
    def __init__(self):
        self.goal_date = None
        self.goal_ym = None
        self.rdb_table = None
        self.selected_data = None
        self.es_index = None

        self.host = os.environ.get('DATABASE_HOST') or "localhost"
        self.port = os.environ.get('DATABASE_PORT') or 5432
        self.dbname = os.environ.get('DATABASE_NAME') or "postgres"
        self.user = os.environ.get('DATABASE_USER') or "postgres"
        self.password = os.environ.get('DATABASE_PASSWORD') or ""

        self.es_host = os.environ.get('ELASTICSEARCH_HOST') or ""
        self.es_port = os.environ.get('ELASTICSEARCH_PORT') or ""

    def get_from_rdb(self):
        try:
            query = f"""
            SELECT id, title, contents, keyword, platform, writer, reg_date, crawl_url, comment_cnt, like_cnt
            FROM {self.rdb_table}
            -- WHERE reg_date BETWEEN current_date - 1 AND current_date;
            WHERE reg_date >= '2022-02-01'::date;
            """
            # 일별로 나눠야하지 않을까?
            # query = f"""
            # SELECT id, title, contents, keyword, platform, writer, reg_date, crawl_url, comment_cnt, like_cnt
            # FROM {self.rdb_table};
            # """
            with pg.connect(
                host=self.host, dbname=self.dbname, port=self.port, user=self.user, password=self.password
            ) as rdb_conn:
                self.selected_data = psql.read_sql(query, rdb_conn)
            print(f"Select {self.rdb_table} Success!")
        except Exception as e:
            print(f"[ERROR] Failed to select...")
            # print(f"[ERROR] Select [{self.goal_date}] Failed...")
            raise e

    def put_to_es(self):
        actions = []
        for idx, doc in self.selected_data.iterrows():
            item_document = {
                'id': doc[0],
                'title': doc[1],
                'contents': doc[2],
                'keyword': doc[3],
                'platform': doc[4],
                'writer': doc[5],
                'reg_date': doc[6],
                'crawl_url': doc[7],
                'comment_cnt': doc[8],
                'like_cnt': doc[9],
            }

            action = {
                '_index': self.es_index,
                '_type': '_doc',
                '_op_type': 'index',
                '_source': item_document,
            }
            try:
                actions.append(action)
            except Exception as e:
                print(action)
                print(e)
        print(f"Length of selected data: {len(actions)}")
        es_conn = Elasticsearch(hosts=self.es_host, port=self.es_port, timeout=30, max_retries=5)
        print("[INFO] Start to Bulk insert into ES index")
        start_time = time.time()
        for i in range(int(len(actions) / 1000)):
            if i < int(len(actions) / 1000) - 1:
                helpers.bulk(client=es_conn, actions=actions[i * 1000:(i+1) * 1000])
            else:
                helpers.bulk(client=es_conn, actions=actions[i * 1000:])
        end_time = time.time()
        print(f"[INFO] Finished for Bulk insert into ES index: Elapsed {round(end_time - start_time, 2)}")

    def run(self, goal_date):
        start_time = time.time()
        self.goal_date = goal_date
        self.goal_ym = self.goal_date[2:6]
        self.rdb_table = f"t_naver_blog"
        # self.rdb_table = f"t_naver_blog_{self.goal_date}"
        # self.es_index = f"mbti_naver_blog_{self.goal_ym}"
        self.es_index = f"mbti_naver_blog_2202"
        arguments = {
            "goal_date": self.goal_date,
            "rdb_table": self.rdb_table,
            "es_index": self.es_index,
        }
        print(f"Argument: {arguments}")

        # Select from RDB table
        self.get_from_rdb()

        # Insert into ES Index
        self.put_to_es()

        end_time = time.time()
        print(f"[INFO] Success {goal_date} | Total Elapsed: {round(end_time - start_time, 2)}")


if __name__ == '__main__':
    target_date = datetime.today().strftime("%Y%m%d")
    print(f"Target date: {target_date}")
    time.sleep(5)
    main = RDB2ES()
    main.run(target_date)

