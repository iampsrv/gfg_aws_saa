import boto3
import zipfile
import os

# AWS client for Lambda and S3
lambda_client = boto3.client('lambda')
s3_client = boto3.client('s3')
iam_client = boto3.client('iam')

# S3 Bucket where the Lambda function code will be uploaded
S3_BUCKET_NAME = 'cloudfrontdemo-oct-2024ps'

# Assume you have an IAM role with Lambda execution permissions
LAMBDA_ROLE_ARN = 'arn:aws:iam::686766985335:role/service-role/batch23lambdafx-role-cjiwzclx'

def create_lambda_function(function_name, handler_file, handler_name):
    # Zip the handler file
    zip_file = f'{function_name}.zip'
    with zipfile.ZipFile(zip_file, 'w') as z:
        z.write(handler_file)
    
    # Upload zip file to S3
    s3_client.upload_file(zip_file, S3_BUCKET_NAME, zip_file)

    # Create Lambda function using code from S3
    response = lambda_client.create_function(
        FunctionName=function_name,
        Runtime='python3.9',
        Role=LAMBDA_ROLE_ARN,
        Handler=f'{handler_file[:-3]}.{handler_name}',
        Code={'S3Bucket': S3_BUCKET_NAME, 'S3Key': zip_file},
        Timeout=15,
        MemorySize=128,
        Publish=True
    )
    
    print(f'Lambda Function {function_name} created.')
    
    # Clean up the zip file locally
    os.remove(zip_file)

    return response

# Creating the individual Lambda handler files
def create_handler_files():
    handlers = {
        'validate_order': """
def lambda_handler(event, context):
    # Dummy order validation logic
    print("Validating order...")
    return {"status": "success", "message": "Order validated"}
""",
        'process_payment': """
def lambda_handler(event, context):
    # Dummy payment processing logic
    print("Processing payment...")
    return {"status": "success", "message": "Payment processed"}
""",
        'check_inventory': """
def lambda_handler(event, context):
    # Dummy inventory check logic
    print("Checking inventory...")
    return {"status": "success", "message": "Inventory available"}
""",
        'reserve_stock': """
def lambda_handler(event, context):
    # Dummy stock reservation logic
    print("Reserving stock...")
    return {"status": "success", "message": "Stock reserved"}
""",
        'trigger_shipping': """
def lambda_handler(event, context):
    # Dummy shipping trigger logic
    print("Triggering shipping...")
    return {"status": "success", "message": "Shipping triggered"}
""",
        'notify_customer': """
def lambda_handler(event, context):
    # Dummy customer notification logic
    print("Notifying customer...")
    return {"status": "success", "message": "Customer notified"}
"""
    }
    
    # Write each handler to a file
    for handler_name, handler_code in handlers.items():
        with open(f'{handler_name}.py', 'w') as f:
            f.write(handler_code)
            print(f'Handler {handler_name}.py created.')

# Create the Lambda handler files
create_handler_files()

# Create Lambda functions
functions = ['validate_order', 'process_payment', 'check_inventory', 'reserve_stock', 'trigger_shipping', 'notify_customer']
for function_name in functions:
    create_lambda_function(function_name, f'{function_name}.py', 'lambda_handler')
