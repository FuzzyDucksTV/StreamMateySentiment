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
    StreamingService = os.getenv('STREAMING_SERVICE', 'Twitch')
    StreamingChannel = os.getenv('STREAMING_CHANNEL', 'fuzzyduckstv')

    chat_connector = ChatConnector(StreamingService, StreamingChannel)
    await chat_connector.connect()

    # Main loop
    while True:
        try:
            # Get a chat message
            message, user, timestamp = await chat_connector.get_message()

            # Analyze the sentiment of the message
            sentiment_score = sentiment_analyzer.analyze_sentiment(message, user, timestamp)

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
