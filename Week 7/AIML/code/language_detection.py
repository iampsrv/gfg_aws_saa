
import boto3

def detect_language(text):
    comprehend = boto3.client('comprehend', region_name='us-east-1')
    response = comprehend.detect_dominant_language(Text=text)
    for language in response['Languages']:
        print(f"Language: {language['LanguageCode']}, Confidence: {language['Score']:.2f}%")

# Example usage
text = "Hello, how are you?"
detect_language(text)
