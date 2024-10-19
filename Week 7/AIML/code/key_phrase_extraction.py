
import boto3

def extract_key_phrases(text, language_code='en'):
    comprehend = boto3.client('comprehend', region_name='us-east-1')
    response = comprehend.detect_key_phrases(Text=text, LanguageCode=language_code)
    print("Key Phrases:")
    for phrase in response['KeyPhrases']:
        print(f"  - {phrase['Text']}, Confidence: {phrase['Score']:.2f}%")

# Example usage
text = "AWS Comprehend is a natural language processing service."
extract_key_phrases(text)
