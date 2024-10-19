from flask import Flask, jsonify, request
import boto3
from botocore.exceptions import ClientError

app = Flask(__name__)

# Initialize DynamoDB
dynamodb = boto3.resource('dynamodb', region_name='us-east-1')  # Change region as needed
table_name = 'Items'  # DynamoDB table name
table = dynamodb.Table(table_name)

# Create Table in DynamoDB (Handles existing table scenario)
def create_dynamodb_table():
    try:
        table = dynamodb.create_table(
            TableName=table_name,
            KeySchema=[
                {'AttributeName': 'key', 'KeyType': 'HASH'}  # Partition key
            ],
            AttributeDefinitions=[
                {'AttributeName': 'key', 'AttributeType': 'S'}
            ],
            ProvisionedThroughput={
                'ReadCapacityUnits': 5,
                'WriteCapacityUnits': 5
            }
        )
        table.wait_until_exists()
        print("DynamoDB table created successfully.")
    except ClientError as e:
        if e.response['Error']['Code'] == 'ResourceInUseException':
            print(f"Table {table_name} already exists.")
        else:
            print(f"Error creating table: {e}")

# Uncomment this line to create the table once, then comment it out if not needed every time
create_dynamodb_table()

# Get all items
def get_all_items_from_db():
    try:
        response = table.scan()
        items = response.get('Items', [])
        return items
    except ClientError as e:
        print(f"Error retrieving items: {e}")
        return []

# Get a single item
def get_item_from_db(key):
    try:
        response = table.get_item(Key={'key': key})
        return response.get('Item', None)
    except ClientError as e:
        print(f"Error retrieving item: {e}")
        return None

# Create a new item
def create_item_in_db(key, value):
    try:
        table.put_item(Item={'key': key, 'value': value})
        return True
    except ClientError as e:
        print(f"Error inserting item: {e}")
        return False

# Update an existing item
def update_item_in_db(key, value):
    try:
        table.update_item(
            Key={'key': key},
            UpdateExpression="set #v = :val",
            ExpressionAttributeNames={'#v': 'value'},
            ExpressionAttributeValues={':val': value}
        )
        return True
    except ClientError as e:
        print(f"Error updating item: {e}")
        return False

# Delete an item
def delete_item_from_db(key):
    try:
        table.delete_item(Key={'key': key})
        return True
    except ClientError as e:
        print(f"Error deleting item: {e}")
        return False

@app.route('/items', methods=['GET'])
def get_all_items():
    items = get_all_items_from_db()
    return jsonify(items)

@app.route('/items/<string:key>', methods=['GET'])
def get_item(key):
    item = get_item_from_db(key)
    if item:
        return jsonify(item)
    else:
        return jsonify({'error': 'Item not found'}), 404

@app.route('/items', methods=['POST'])
def create_item():
    item = request.get_json()
    key = item.get('key')
    value = item.get('value')
    if key and value and create_item_in_db(key, value):
        return jsonify({'message': 'Item created successfully'}), 201
    else:
        return jsonify({'error': 'Error creating item'}), 500

@app.route('/items/<string:key>', methods=['PUT'])
def update_item(key):
    item = request.get_json()
    value = item.get('value')
    if value and update_item_in_db(key, value):
        return jsonify({'message': 'Item updated successfully'})
    else:
        return jsonify({'error': 'Error updating item'}), 500

@app.route('/items/<string:key>', methods=['DELETE'])
def delete_item(key):
    if delete_item_from_db(key):
        return jsonify({'message': 'Item deleted successfully'})
    else:
        return jsonify({'error': 'Error deleting item'}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001, debug=True)
