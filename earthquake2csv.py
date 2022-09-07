import json
import time
import requests
import pandas as pd
from datetime import datetime


class MakeCSV:
    def __init__(self, start_time, end_time):
        # self.start_time = datetime.strftime(start_time, '%Y-%m-%d')
        # self.end_time = datetime.strftime(end_time, '%Y-%m-%d')
        self.start_time = start_time
        self.end_time = end_time
        self.data = None

    def get_data(self):
        default_url = 'https://earthquake.usgs.gov/fdsnws/event/1/query'
        parameters = {
          'format': 'geojson',
          'starttime': self.start_time,
          'endtime': self.end_time
        }
        res = requests.get(url=default_url, params=parameters)
        self.data = json.loads(res.text)

    def make_csv(self):
        df1 = pd.DataFrame([i['properties'] for i in self.data['features']])
        df2 = pd.DataFrame(
          [i['geometry']['coordinates'] for i in self.data['features']],
          columns=['longitude', 'latitude', 'depth']
        )
        df = pd.concat([df1, df2], axis=1)
        print(f"[DEBUG] Length of data: {len(df)}")
        pd.to_datetime(df['time'], unit='ms')
        df.drop(labels=['updated', 'tz', 'url', 'detail', 'status', 'net', 'sig', 'types'], axis=1, inplace=True)
        df.sort_values(by=['time'], inplace=True)
        df.reset_index(drop=True, inplace=True)
        df.to_csv(f'./earthquake_{self.start_time[:4]+self.start_time[5:7]}.csv', encoding='utf-8')

    def run(self):
        print(f"[DEBUG] Start time: {self.start_time} | End time: {self.end_time}")
        self.get_data()
        self.make_csv()


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
      # , ('2022-03-01', '2022-03-31')
    ]
    for start, end in date_list:
        s_time = time.time()
        module = MakeCSV(start_time=start, end_time=end)
        module.run()
        print(f"[INFO] Elapsed time: {round(time.time() - s_time, 3)}")
