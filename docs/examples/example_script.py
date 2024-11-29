import os
import datetime as dt
from rumorz.client import RumorzClient
from rumorz.enums import EntityType, Lookback, EntityMetrics


def main():
    # Initialize the Rumorz client
    rumorz_client = RumorzClient(api_key=os.environ['RUMORZ_API_KEY'])

    # Get the ranking of persons based on sentiment for the last 7 days
    ranking = rumorz_client.graph.get_ranking(
        lookback=Lookback.ONE_WEEK, 
        page=1, 
        limit=10, 
        sort_by=EntityMetrics.SENTIMENT, 
        entity_type=EntityType.PERSON.value, 
        ascending=False
    )
    
    # Extract the top 2 people with the most positive sentiment
    top_positive_entities = ranking[:2]
    
    # Extract the top 2 people with the most negative sentiment
    top_negative_entities = ranking[-2:]
    
    # Summarize information for top positive sentiment entities
    print("Top 2 People with the Most Positive Sentiment:")
    for entity in top_positive_entities:
        summary = rumorz_client.agent.summarize(
            id=entity['id'], 
            timestamp=dt.datetime.utcnow().isoformat(), 
            scores_filter="sentiment > 0.75"
        )
        print(summary)

    # Summarize information for top negative sentiment entities
    print("\nTop 2 People with the Most Negative Sentiment:")
    for entity in top_negative_entities:
        summary = rumorz_client.agent.summarize(
            id=entity['id'], 
            timestamp=dt.datetime.utcnow().isoformat(), 
            scores_filter="sentiment < -0.75"
        )
        print(summary)

    print("\nScript executed successfully.")


if __name__ == "__main__":
    main()