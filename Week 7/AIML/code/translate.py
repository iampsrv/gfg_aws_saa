import boto3

# Initialize a Translate client
translate = boto3.client('translate', region_name='us-east-1')  # Specify the region

# Define the text to translate and the languages
text_to_translate = "Hello, how are you?"
source_language = "en"  # English
target_language = "es"  # Spanish

# Call the translate_text function
response = translate.translate_text(
    Text=text_to_translate,
    SourceLanguageCode=source_language,
    TargetLanguageCode=target_language
)

# Extract and print the translated text
translated_text = response['TranslatedText']
print(f"Translated Text: {translated_text}")
