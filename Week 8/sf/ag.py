import boto3
import zipfile
import os

# AWS Lambda client
lambda_client = boto3.client('lambda')

# 
LAMBDA_ROLE_ARN = 'arn:aws:iam::686766985335:role/service-role/batch23lambdafx-role-cjiwzclx'

# Lambda function code (lambda_stage_test.py)
lambda_code = """
def lambda_handler(event, context):
    # Read the stage variable from the event
    stage_variable = event.get('stageVariable', 'No stage variable passed')
    
    # Return the stage variable as part of the response
    return {
        'statusCode': 200,
        'body': f"Stage variable value: {stage_variable}"
    }
"""

# Create a zip package for the Lambda function
def create_lambda_zip_file(file_name, function_name):
    with open(f"{function_name}.py", 'w') as f:
        f.write(lambda_code)
    
    zip_file = f"{function_name}.zip"
    with zipfile.ZipFile(zip_file, 'w') as z:
        z.write(f"{function_name}.py")
    
    print(f"Created zip package: {zip_file}")
    return zip_file

# Create the Lambda function in AWS
def create_lambda_function(lambda_name, role_arn):
    zip_file = create_lambda_zip_file('lambda_stage_test.py', lambda_name)
    
    with open(zip_file, 'rb') as f:
        zip_data = f.read()

    response = lambda_client.create_function(
        FunctionName=lambda_name,
        Runtime='python3.9',  # Specify the Python runtime
        Role=role_arn,  # Lambda execution role ARN
        Handler='lambda_stage_test.lambda_handler',
        Code={'ZipFile': zip_data},
        Timeout=15,
        MemorySize=128,
        Publish=True
    )
    
    # Clean up the zip and handler file
    os.remove(zip_file)
    os.remove(f"{lambda_name}.py")
    
    print(f"Lambda Function {lambda_name} created.")
    return response

# Main execution
if __name__ == "__main__":
    lambda_name = 'lambda_stage_test'
    create_lambda_function(lambda_name, LAMBDA_ROLE_ARN)
