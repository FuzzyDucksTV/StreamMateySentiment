import asyncio
import logging
import os
from sqlite3 import DatabaseError
from chat_connector import ChatConnector
from sentiment_analyzer import SentimentAnalyzer
from sentiment_meter import SentimentMeter
from database import Database

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Sentiment analyzer parameters
SENTIMENT_THRESHOLD = 0.05  # positive sentiment score

# Database parameters
DATABASE_PATH = 'chat_messages.db'

async def main():
    # Initialize components
    database = Database(DATABASE_PATH)
    sentiment_analyzer = SentimentAnalyzer(database)
    sentiment_meter = SentimentMeter()

    # Connect to the chosen channel set by the user when they first ran the program.
    STREAMING_SERVICE = os.getenv('STREAMING_SERVICE', 'Youtube')
    STREAMING_SERVICE = os.getenv('STREAMING_SERVICE', 'fuzzyduckstv')

    chat_connector = ChatConnector(STREAMING_SERVICE, STREAMING_SERVICE)
    chat_connector.connect_to_chat()

    # Main loop
    while True:
        try:
            # Get a chat message
            #message, user, timestamp = chat_connector.get_message()
            for message in chat_connector.get_message():
                timestamp = message['timestamp']
                author = message['author']
                text = message['message']
            # Analyze the sentiment of the message
            sentiment_score = sentiment_analyzer.analyze_sentiment(text, author, timestamp)

            # Update the sentiment meter with the new sentiment score
            sentiment_meter.update(sentiment_score)

            # Wait a bit before the next iteration
            await asyncio.sleep(0.1)
        except DatabaseError as e:
            logger.error(f"A database error occurred: {e}")
            logger.info("Attempting to reconnect to the database...")
            database.reconnect()
        except Exception as e:
            logger.error(f"An error occurred: {e}")
            continue
        except KeyboardInterrupt:
            logger.info("Stopping application...")
            break

if __name__ == '__main__':
    asyncio.run(main())
