import datetime as dt
import os
import unittest

from rumorz.client import RumorzClient

rumorz = RumorzClient(api_key='0uiWflS2MtlfxxlrNsLclz34VUtbpHmnq1H9OdM4fos=')#, api_url='http://localhost:8000')


class TestRumorz(unittest.TestCase):


    def test_search_entities(self):
        entities = rumorz.graph.search_entities(**{
            "name": "Bitcoin",
            "asset_class": "crypto",
            "entity_type": "FinancialAsset",
            "symbol_search": "BTC",
            "limit": 10
        })
        self.assertTrue(len(entities) > 0)

    def test_time_series(self):
        timeseries = rumorz.graph.get_entity_timeseries(**{
            "node_ids": [
                "7d8d81b3-0808-47ce-b459-a9fd5f74fd57"
            ],
            "metrics": [
                "price",
                "sentiment"
            ],
            "lookback": "3M",
            "page": 1,
            "limit": 100
        })
        self.assertTrue(len(timeseries) > 0)

    def test_entity_summary(self):
        entity_update = rumorz.agent.get_entity_summary(**{
            "node_id": "7d8d81b3-0808-47ce-b459-a9fd5f74fd57",
            "timestamp": dt.datetime.utcnow().isoformat(),
            "scores_filter": "sentiment > 0.75"
        })
        self.assertTrue(len(entity_update) > 0)

    def test_get_ranking(self):
        screener = rumorz.graph.get_ranking(**{
            "lookback": "1D",
            "page": 1,
            "limit": 10,
            "sort_by": "mentions",
            "entity_type": "financial_asset",
        })
        self.assertTrue(len(screener) > 0)

    def test_limit_validation(self):
        try:
            rumorz.graph.get_ranking(**{
                "lookback": "1D",
                "page": 1,
                "limit": 1000,
                "sort_by": "mentions",
                "entity_type": "financial_asset",
            })
        except Exception as e:
            self.assertTrue("limit" in str(e).lower())


    def test_posts(self):
        posts = rumorz.graph.get_entity_posts(**{
            "node_ids": ["7d8d81b3-0808-47ce-b459-a9fd5f74fd57"],
            "lookback": "30D",
            "scores_filter": "sentiment > 0.75",
            "page": 1,
            "limit": 10
        })

        self.assertTrue(len(posts) > 0)
