import boto3

# Initialize a Rekognition client
rekognition = boto3.client('rekognition', region_name='us-east-1')  # Specify the region

# Define the image to analyze
image_file = 'skateboard_resized.jpg'

# Load the image
with open(image_file, 'rb') as image:
    image_bytes = image.read()

# Call the detect_labels function
response = rekognition.detect_labels(
    Image={'Bytes': image_bytes},
    MaxLabels=25,          # Limit to 10 labels
    MinConfidence=30       # Only include labels with a confidence of 70% or higher
)

# Extract and print the detected labels
print("Detected labels:")
for label in response['Labels']:
    print(f"Label: {label['Name']}, Confidence: {label['Confidence']:.2f}%")
