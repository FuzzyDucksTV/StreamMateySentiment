import logging

class SentimentMeter:
    """
    This class is responsible for displaying a meter that changes as each message is given a sentiment score.
    """

    def __init__(self):
        """
        Initializes the SentimentMeter.
        """
        self.logger = logging.getLogger(__name__)
        self.sentiment_score = 0.0

    def update(self, sentiment_score):
        """
        Updates the sentiment meter based on the sentiment score of a message.

        Args:
            sentiment_score (float): The sentiment score of a message.

        Raises:
            TypeError: If sentiment_score is not a float.
            ValueError: If sentiment_score is not between -1 and 1.
        """
        if not isinstance(sentiment_score, float):
            raise TypeError("Sentiment score must be a float.")
        if not -1 <= sentiment_score <= 1:
            raise ValueError("Sentiment score must be between -1 and 1.")
        
        self.sentiment_score = sentiment_score
        self.display()

    def display(self):
        """
        Displays the sentiment meter.
        """
        # Convert the sentiment score to a percentage
        percentage = (self.sentiment_score + 1) / 2 * 100

        # Create a text-based meter
        meter = '[' + '=' * int(percentage / 10) + ' ' * (10 - int(percentage / 10)) + ']'

        # Display the meter
        self.logger.debug(f"Sentiment Meter: {meter} ({percentage:.1f}%)")
