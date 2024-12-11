import os
from datetime import datetime
from rumorz.client import RumorzClient
from rumorz.enums import EntityType, EntityMetrics, Lookback


def main():
    # Initialize the RumorzClient
    rumorz_client = RumorzClient(api_key=os.environ['RUMORZ_API_KEY'])

    # Get top 2 people with the most positive sentiment in the last 7 days
    print("Fetching top 2 people with the most positive sentiment in the last 7 days...")
    top_positive_people = rumorz_client.graph.get_ranking(
        lookback=Lookback.ONE_WEEK,
        entity_type=EntityType.PERSON,
        sort_by=EntityMetrics.SENTIMENT,
        ascending=False,
        limit=2
    )
    for person in top_positive_people:
        print(f"Positive Sentiment - Person: {person['name']}, Sentiment: {person['sentiment']}")

    # Get top 2 people with the most negative sentiment in the last 7 days
    print("\nFetching top 2 people with the most negative sentiment in the last 7 days...")
    top_negative_people = rumorz_client.graph.get_ranking(
        lookback=Lookback.ONE_WEEK,
        entity_type=EntityType.PERSON,
        sort_by=EntityMetrics.SENTIMENT,
        ascending=True,
        limit=2
    )
    for person in top_negative_people:
        print(f"Negative Sentiment - Person: {person['name']}, Sentiment: {person['sentiment']}")

    # Generate summaries for top 2 positive sentiment people
    print("\nGenerating summaries for top positive sentiment people...")
    for person in top_positive_people:
        summary = rumorz_client.agent.summarize(id=person['id'], timestamp=datetime.utcnow().isoformat())
        print(f"Summary for {person['name']}: {summary}")

    # Generate summaries for top 2 negative sentiment people
    print("\nGenerating summaries for top negative sentiment people...")
    for person in top_negative_people:
        summary = rumorz_client.agent.summarize(id=person['id'], timestamp=datetime.utcnow().isoformat())
        print(f"Summary for {person['name']}: {summary}")

    print("\nScript execution completed successfully!")


if __name__ == '__main__':
    main()
