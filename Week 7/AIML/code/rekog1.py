import boto3

# Initialize a Rekognition client
rekognition = boto3.client('rekognition', region_name='us-east-1')  # Specify the region

# Define the image to analyze
image_file = 'drive_resized.jpg'

# Load the image
with open(image_file, 'rb') as image:
    image_bytes = image.read()

# Call the detect_faces function
response = rekognition.detect_faces(
    Image={'Bytes': image_bytes},
    Attributes=['ALL']  # Request all facial attributes
)

# Extract and print the detected facial attributes
for face_detail in response['FaceDetails']:
    print("Face details:")
    print(f"  - Age Range: {face_detail['AgeRange']['Low']} - {face_detail['AgeRange']['High']}")
    print(f"  - Emotions:")
    for emotion in face_detail['Emotions']:
        print(f"    * {emotion['Type']} : {emotion['Confidence']:.2f}%")
    print(f"  - Gender: {face_detail['Gender']['Value']}")
    print(f"  - Smile: {face_detail['Smile']['Value']}, Confidence: {face_detail['Smile']['Confidence']:.2f}%")
    print(f"  - Eyeglasses: {face_detail['Eyeglasses']['Value']}, Confidence: {face_detail['Eyeglasses']['Confidence']:.2f}%")
    print(f"  - Sunglasses: {face_detail['Sunglasses']['Value']}, Confidence: {face_detail['Sunglasses']['Confidence']:.2f}%")
    print(f"  - Beard: {face_detail['Beard']['Value']}, Confidence: {face_detail['Beard']['Confidence']:.2f}%")
    print(f"  - Mustache: {face_detail['Mustache']['Value']}, Confidence: {face_detail['Mustache']['Confidence']:.2f}%")
    print(f"  - Eyes Open: {face_detail['EyesOpen']['Value']}, Confidence: {face_detail['EyesOpen']['Confidence']:.2f}%")
    print(f"  - Mouth Open: {face_detail['MouthOpen']['Value']}, Confidence: {face_detail['MouthOpen']['Confidence']:.2f}%")
