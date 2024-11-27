import os
import traceback

from rumorz.client import RumorzClient, RumorzAPIException
from rumorz.enums import Lookback, EntityType, EntityMetrics


def main():
    try:
        # Initialize RumorzClient with the API key from environment variables
        rumorz_client = RumorzClient(api_key=os.getenv('RUMORZ_API_KEY'),
                                     api_url='http://localhost:8000')

        # Define the lookback period
        lookback_period = Lookback.ONE_WEEK.value

        # Fetch the top 2 people with the most positive sentiment in the last 7 days
        positive_sentiment_ranking = rumorz_client.graph.get_ranking(
            lookback=lookback_period,
            page=1,
            limit=2,
            sort_by=EntityMetrics.SENTIMENT.value,
            entity_type=EntityType.PERSON.value,
            ascending=False
        )

        print('Top 2 People with the Most Positive Sentiment:')
        print(f"{positive_sentiment_ranking}")

        # Fetch summaries for the top 2 people with the most positive sentiment
        for person in positive_sentiment_ranking:
            summary = rumorz_client.agent.get_entity_summary(node_id=person['id'])
            print(f"Summary for {person}:")
            print(summary)

        # Fetch the top 2 people with the most negative sentiment in the last 7 days
        negative_sentiment_ranking = rumorz_client.graph.get_ranking(
            lookback=lookback_period,
            page=1,
            limit=2,
            sort_by=EntityMetrics.SENTIMENT.value,
            entity_type=EntityType.PERSON.value,
            ascending=True
        )

        print('Top 2 People with the Most Negative Sentiment:')
        print(f"{negative_sentiment_ranking}")

        # Fetch summaries for the top 2 people with the most negative sentiment
        for person in negative_sentiment_ranking:
            summary = rumorz_client.agent.get_entity_summary(node_id=person['id'])
            print(f"Summary for {person}:")
            print(summary)

        print("Script execution completed successfully.")

    except RumorzAPIException as e:
        print(f"An error occurred while calling the Rumorz API: {e}")
    except Exception as ex:
        print(f"An unexpected error occurred: {ex}")
        traceback.print_exc()


if __name__ == '__main__':
    main()
