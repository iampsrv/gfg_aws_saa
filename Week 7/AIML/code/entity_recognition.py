
import boto3

def recognize_entities(text, language_code='en'):
    comprehend = boto3.client('comprehend', region_name='us-east-1')
    response = comprehend.detect_entities(Text=text, LanguageCode=language_code)
    print("Entities:")
    for entity in response['Entities']:
        print(f"Entity: {entity['Text']}, Type: {entity['Type']}, Confidence: {entity['Score']:.2f}%")

# Example usage
text = "Amazon Web Services is headquartered in Seattle."
recognize_entities(text)
