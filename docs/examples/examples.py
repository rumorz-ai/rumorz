import os
from datetime import datetime
from rumorz.client import RumorzClient
from rumorz.enums import Lookback, EntityType, EntityMetrics

# Initialize the RumorzClient
rumorz_client = RumorzClient(api_key=os.environ['RUMORZ_API_KEY'])

# Step 1: Get the entity rankings for people based on sentiment over the past 7 days.
rankings = rumorz_client.graph.get_ranking(
    lookback=Lookback.ONE_WEEK.value,
    entity_type=EntityType.PERSON.value,
    sort_by=EntityMetrics.SENTIMENT.value,
    scores_filter='mentions > 10',
    limit=10,
    ascending=False
)
print("Entity rankings (top 10 people by sentiment in the last 7 days):", rankings)

# Step 2: Identify the top 2 with the most positive sentiment and top 2 with the most negative sentiment
sorted_rankings = sorted(rankings, key=lambda x: x['sentiment'], reverse=True)
top_positive = sorted_rankings[:2]
top_negative = sorted_rankings[-2:]

# Step 3: Fetch summaries for these identified entities
all_summaries = {}
for entity in top_positive + top_negative:
    summary = rumorz_client.agent.summarize(
        id=entity['id'],
        timestamp=datetime.utcnow().isoformat()
    )
    all_summaries[entity['name']] = summary
    print(f"Summary for {entity['name']}:", summary)

print("Script executed successfully with summaries obtained.")

