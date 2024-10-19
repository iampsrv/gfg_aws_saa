import boto3

# Initialize a Rekognition client
rekognition = boto3.client('rekognition', region_name='us-east-1')  # Specify the region

# Define the image to analyze
image_file = 'coffee_monday_resized.jpg'

# Load the image
with open(image_file, 'rb') as image:
    image_bytes = image.read()

# Call the detect_text function
response = rekognition.detect_text(
    Image={'Bytes': image_bytes}
)

# Extract and print the detected text
print("Detected Text:")
for text_detail in response['TextDetections']:
    detected_text = text_detail['DetectedText']
    confidence = text_detail['Confidence']
    text_type = text_detail['Type']  # WORD or LINE
    print(f"Text: {detected_text}, Confidence: {confidence:.2f}%, Type: {text_type}")
