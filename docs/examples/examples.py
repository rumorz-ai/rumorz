import os
import datetime as dt
from rumorz.client import RumorzClient
from rumorz.enums import Lookback, EntityType, EntityMetrics


def main():
    api_key = os.environ['RUMORZ_API_KEY']
    rumorz_client = RumorzClient(api_key=api_key)

    # Get the top 2 people with the most positive sentiment in the last 7 days
    positive_sentiment_ranking = rumorz_client.graph.get_ranking(
        lookback=Lookback.ONE_WEEK,
        entity_type=EntityType.PERSON,
        sort_by=EntityMetrics.SENTIMENT,
        ascending=False,
        limit=2
    )
    print("Top 2 people with the most positive sentiment:")
    for entity in positive_sentiment_ranking:
        print(entity)

    # Get the top 2 people with the most negative sentiment in the last 7 days
    negative_sentiment_ranking = rumorz_client.graph.get_ranking(
        lookback=Lookback.ONE_WEEK,
        entity_type=EntityType.PERSON,
        sort_by=EntityMetrics.SENTIMENT,
        ascending=True,
        limit=2
    )
    print("\nTop 2 people with the most negative sentiment:")
    for entity in negative_sentiment_ranking:
        print(entity)

    # Fetch and print summaries for these entities
    print("\nSummaries for top entities:")
    for ranking_list in [positive_sentiment_ranking, negative_sentiment_ranking]:
        for entity in ranking_list:
            summary = rumorz_client.agent.summarize(
                id=entity['id'],
                timestamp=dt.datetime.utcnow().isoformat()
            )
            print(f"Summary for {entity['name']}:")
            print(summary)


if __name__ == '__main__':
    main()

    print("\nScript execution completed successfully.")