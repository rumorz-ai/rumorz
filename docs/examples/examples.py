import datetime as dt
import os

import pandas as pd

from rumorz.client import RumorzClient
from rumorz.enums import Lookback, EntityType, AssetClass, EntityMetrics

# Initialize Rumorz Client
rumorz = RumorzClient(api_key=os.environ['RUMORZ_API_KEY'])
ranking = rumorz.graph.get_ranking(
    lookback=Lookback.ONE_DAY.value,  # Look back at the last day
    entity_type=EntityType.FINANCIAL_ASSET.value,
    asset_class=AssetClass.CRYPTO.value,
    metrics=[EntityMetrics.SENTIMENT.value]
)

# Create a DataFrame from the ranking and sort by sentiment in ascending order
ranking_df = pd.DataFrame(ranking)
ranking_df.sort_values(by=EntityMetrics.SENTIMENT.value, ascending=True, inplace=True)

# Get the bottom 5 cryptocurrencies by negative sentiment
bottom_5_crypto = ranking_df.head(5)

# Get the latest posts for the bottom 5 cryptocurrencies
entities_posts = {}
for node_id in bottom_5_crypto['id']:
    posts = rumorz.graph.get_entity_posts(node_ids=[node_id], lookback=Lookback.ONE_DAY.value, limit=1)
    entities_posts[node_id] = posts

# Get summary of the latest negative news for
summaries = {}
for node_id, posts in entities_posts.items():
    if len(posts) > 0:
        summary = rumorz.agent.get_entity_summary(
            node_id=node_id,
            timestamp=dt.datetime.utcnow().isoformat()
        )
        summaries[node_id] = summary

# Print the summaries
for node_id, summary in summaries.items():
    print(f"Summary for {node_id}: {summary}")
