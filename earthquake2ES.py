__encode__ = 'UTF-8'
__author__ = 'MS'
__title__ = '22/3Q Study 지진 데이터 파싱 및 ES 적재'
"""
* 수정이력
    2022-09-08      MS    최초작성
"""
import json
import time
import requests
import traceback
import pandas as pd
from datetime import datetime
from elasticsearch import Elasticsearch, helpers


class Earthquake2ES:
    def __init__(self, start_time, end_time):
        # self.start_time = datetime.strftime(start_time, '%Y-%m-%d')
        # self.end_time = datetime.strftime(end_time, '%Y-%m-%d')
        self.start_time = start_time
        self.end_time = end_time
        self.data = None
        self.es_host = '192.168.2.180'
        self.es_port = '9201'
        self.index = 'earthquake'

    def get_data(self):
        default_url = 'https://earthquake.usgs.gov/fdsnws/event/1/query'
        parameters = {
          'format': 'geojson',
          'starttime': self.start_time,
          'endtime': self.end_time
        }
        res = requests.get(url=default_url, params=parameters)
        self.data = json.loads(res.text)

    def make_dataframe(self):
        df1 = pd.DataFrame([i['properties'] for i in self.data['features']])
        df2 = pd.DataFrame(
          [i['geometry']['coordinates'] for i in self.data['features']],
          columns=['longitude', 'latitude', 'depth']
        )
        df = pd.concat([df1, df2], axis=1)
        print(f"[DEBUG] Length of data: {len(df)}")
        pd.to_datetime(df['time'], unit='ms')
        df.drop(
          labels=[
            'felt', 'cdi', 'mmi', 'alert', 'nst', 'dmin', 'updated',
            'tz', 'url', 'detail', 'status', 'net', 'sig', 'types'
          ],
          axis=1,
          inplace=True
        )
        df.sort_values(by=['time'], inplace=True)
        df.reset_index(drop=True, inplace=True)
        fill_values = {
          'mag': -1,
          'place': 'Unknown',
          'tsunami': -1,
          'code': 'Unknown',
          'ids': 'Unknown',
          'sources': 'Unknown',
          'rms': -1,
          'gap': -1,
          'magType': 'Unknown'
        }
        df.fillna(value=fill_values, inplace=True)

        return df

    def to_elasticsearch(self, dataframe):
        loop_cnt = 0
        actions = []
        for row in dataframe.iloc:
            row = row.to_dict()
            document = {
                'title': row['title'],
                'place': row['place'],
                'time': row['time'],
                'type': row['type'],
                'mag': row['mag'],
                # 'felt': row['felt'],
                # 'cdi': row['cdi'],
                # 'mmi': row['mmi'],
                # 'alert': row['alert'],
                'tsunami': row['tsunami'],
                'code': row['code'],
                'ids': row['ids'],
                'sources': row['sources'],
                # 'nst': row['nst'],
                # 'dmin': row['dmin'],
                'rms': row['rms'],
                'gap': row['gap'],
                'magType': row['magType'],
                'location': [
                  {'lat': row['latitude'], 'lon': row['longitude']}
                ],
                'depth': row['depth']
            }
            index = f'{self.index}_{self.start_time[2:4] + self.start_time[5:7]}'
            action = {
              '_index': index,
              '_type': '_doc',
              '_op_type': 'index',
              '_source': document
            }
            # if loop_cnt == 0:
            #     loop_cnt += 1
            #     print(f"Keys of dataframe: {dataframe.keys()}\nKeys of document: {document.keys()}")
            try:
                actions.append(action)
            except Exception:
                traceback.print_exc()

        print(f"[DEBUG] Length of actions: {len(actions)}")
        es_conn = Elasticsearch(
          hosts=self.es_host,
          port=self.es_port,
          timeout=25,
          max_retries=5,
          retry_on_timeout=True
        )

        helpers.bulk(client=es_conn, actions=actions)

    def run(self):
        print(f"[DEBUG] Start time: {self.start_time} | End time: {self.end_time}")
        self.get_data()
        dataframe = self.make_dataframe()
        self.to_elasticsearch(dataframe=dataframe)


if __name__ == '__main__':
    '''
    start = input("""
* Start time(ex: 2022-01-01):
    """)
    end = input("""
* End time(ex: 2022-01-31):
    """)
    '''
    date_list = [
      ('2022-01-01', '2022-01-31'), ('2022-02-01', '2022-02-28'), ('2022-03-01', '2022-03-31'),
      ('2022-04-01', '2022-04-30'), ('2022-05-01', '2022-05-31'), ('2022-06-01', '2022-06-30'),
      ('2022-07-01', '2022-07-31'), ('2022-08-01', '2022-08-31')
    ]
    for start, end in date_list:
        s_time = time.time()
        module = Earthquake2ES(start_time=start, end_time=end)
        module.run()
        print(f"[INFO] Elapsed time: {round(time.time() - s_time, 3)}")

"""
# Elasticsearch template
PUT _template/template_earthquake
{
  "index_patterns" : [
    "earthquake_*"
  ],
  "settings" : {
    "index" : {
      "analysis" : {
        "analyzer" : {
          "token_whitespace" : {
            "filter" : [
              "lowercase"
            ],
            "tokenizer" : "whitespace"
          }
        }
      },
      "number_of_shards" : "2",
      "number_of_replicas" : "1"
    }
  },
  "mappings" : {
    "properties" : {
      "title": {
        "type": "text",
        "analyzer" : "token_whitespace"
      },
      "place": {
        "type": "text",
        "analyzer" : "token_whitespace"
      },
      "time": {
        "type": "date"
      },
      "type": {
        "type": "keyword"
      },
      "mag": {
        "type": "float"
      },
      "tsunami": {
        "type": "keyword"
      },
      "code": {
        "type": "keyword"
      },
      "ids": {
        "type": "keyword"
      },
      "sources": {
        "type": "keyword"
      },
      "rms": {
        "type": "keyword"
      },
      "gap": {
        "type": "keyword"
      },
      "magType": {
        "type": "keyword"
      },
      "location": {
        "type": "geo_point"
      },
      "depth": {
        "type": "float"
      }
    }
  },
  "aliases" : {
    "earthquake" : { }
  }
}
"""
