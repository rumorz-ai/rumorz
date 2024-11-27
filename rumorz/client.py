import os
import traceback
from enum import Enum

import litellm
import pandas as pd
import requests

litellm.set_verbose = False


class RumorzAPIException(Exception):
    pass


class RumorzClient:
    def __init__(self,
                 api_key=os.environ['RUMORZ_API_KEY'],
                 api_url='http://rumorz-api.eastus2.azurecontainer.io'):
        self.api_url = api_url
        self.headers = {
            'accept': 'application/json',
            'Content-Type': 'application/json',
            'X-API-Key': api_key
        }
        self.graph = self.Graph(self)
        self.agent = self.Agent(self)

    def call_function(self, function_name, params):
        url = f"{self.api_url}/api/{function_name}"
        params = self._format_params(params)
        response = requests.post(url, json=params, headers=self.headers, timeout=30)
        try:
            response.raise_for_status()
            return response.json()['data']
        except Exception as e:
            raise RumorzAPIException(response.text)

    def _format_params(self, data):
        for key, value in data.items():
            if isinstance(value, Enum):
                data[key] = value.value

        todrop = []
        for key, value in data.items():
            if value is None:
                todrop.append(key)
        for key in todrop: data.pop(key)
        return data

    class Graph:

        def __init__(self, api):
            self.api = api

        def get_entity_posts(self,
                             **kwargs):
            return self.api.call_function('get_entity_posts', params=kwargs)

        def search_entities(self,
                            **kwargs):
            """
            Search for entities in the database based on the given parameters.
            Example:
            entities = rumorz.graph.search_entities(name=entity_name, symbol_search=symbol, asset_class=AssetClass.CRYPTO.value, entity_type=EntityType.FINANCIAL_ASSET.value, limit=1)

            Returns a list of json entities like {id, type, name, symbol}
            """
            return self.api.call_function('search_entities', params=kwargs)

        def get_ranking(self,
                        **kwargs):
            """
            Returns a ranking of every single entity in the Graph based on the given parameters.
            """
            return self.api.call_function('get_ranking', params=kwargs)

        def get_entity_timeseries(self,
                                  as_df=True,
                                  **kwargs):
            timeseries = self.api.call_function('get_entity_timeseries', params=kwargs)
            if as_df:
                dfs = {}
                for node_ts in timeseries:
                    df = pd.DataFrame()
                    df['timestamp'] = [v[0] for v in node_ts['time_series'][0]['values']]
                    df['timestamp'] = pd.to_datetime(df['timestamp'])
                    df.set_index('timestamp', inplace=True)
                    for ts in node_ts['time_series']:
                        metric = ts['metric']
                        values = ts['values']
                        df[metric] = [v[1] for v in values]
                        dfs[node_ts['node_id']] = df
                return dfs


    class Agent:
        def __init__(self, api):
            self.api = api

        def get_entity_summary(self,
                               **kwargs):
            return self.api.call_function('get_entity_summary', params=kwargs)

        def get_state(self,
                      **kwargs):
            return self.api.call_function('get_state', params=kwargs)

        def get_logs(self,
                     **kwargs):
            return self.api.call_function('get_logs', params=kwargs)