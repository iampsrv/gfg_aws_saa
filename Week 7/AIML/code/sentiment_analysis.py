
import boto3

def analyze_sentiment(text, language_code='en'):
    comprehend = boto3.client('comprehend', region_name='us-east-1')
    response = comprehend.detect_sentiment(Text=text, LanguageCode=language_code)
    sentiment = response['Sentiment']
    sentiment_score = response['SentimentScore']
    print(f"Sentiment: {sentiment}")
    print("Sentiment Scores:", sentiment_score)

# Example usage
text = "I am very sad today!"
analyze_sentiment(text)
