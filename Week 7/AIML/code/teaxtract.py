import boto3

def detect_text_in_document(file_path):
    # Initialize the Textract client
    textract = boto3.client('textract', region_name='us-east-1')

    # Load the document
    with open(file_path, 'rb') as document:
        image_bytes = document.read()

    # Call Textract to detect text
    response = textract.detect_document_text(Document={'Bytes': image_bytes})

    # Extract and print detected text
    print("Detected Text:")
    for item in response['Blocks']:
        if item['BlockType'] == 'LINE':
            print(item['Text'])

# Example usage
file_path = 'sample.pdf'  # Use .jpg, .png, or .pdf
detect_text_in_document(file_path)
