from flask import Flask, jsonify, request
import boto3
import psycopg2
import os

app = Flask(__name__)

# AWS RDS database configuration
RDS_HOST = 'database-1.cakxb5zzw0ie.us-east-1.rds.amazonaws.com'
RDS_PORT = '5432'
DB_NAME = 'database1'
DB_USER = 'postgres'
DB_PASSWORD = 'pranjal123'

# Establish connection to AWS RDS PostgreSQL database
def get_db_connection():
    return psycopg2.connect(
        host=RDS_HOST,
        port=RDS_PORT,
        database=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD
    )

# Create table in PostgreSQL if it does not exist
def create_items_table():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS items (
            id SERIAL PRIMARY KEY,
            key TEXT NOT NULL,
            value TEXT NOT NULL
        )
    ''')
    conn.commit()
    cursor.close()
    conn.close()

# Fetch all items from the database
def get_all_items_from_db():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT key, value FROM items')
    items = cursor.fetchall()
    cursor.close()
    conn.close()
    return items

# Fetch a single item by key
def get_item_from_db(key):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT key, value FROM items WHERE key = %s', (key,))
    item = cursor.fetchone()
    cursor.close()
    conn.close()
    return item

# Insert a new item into the database
def create_item_in_db(key, value):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('INSERT INTO items (key, value) VALUES (%s, %s)', (key, value))
    conn.commit()
    cursor.close()
    conn.close()

# Update an existing item in the database
def update_item_in_db(key, value):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('UPDATE items SET value = %s WHERE key = %s', (value, key))
    conn.commit()
    cursor.close()
    conn.close()

# Delete an item from the database
def delete_item_from_db(key):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('DELETE FROM items WHERE key = %s', (key,))
    conn.commit()
    cursor.close()
    conn.close()

# Flask route to get all items
@app.route('/items', methods=['GET'])
def get_all_items():
    items = get_all_items_from_db()
    return jsonify(items)

# Flask route to get a single item by key
@app.route('/items/<string:key>', methods=['GET'])
def get_item(key):
    item = get_item_from_db(key)
    if item:
        return jsonify(item)
    else:
        return jsonify({'error': 'Item not found'}), 404

# Flask route to create a new item
@app.route('/items', methods=['POST'])
def create_item():
    item = request.get_json()
    if 'key' not in item or 'value' not in item:
        return jsonify({'error': 'Invalid item data'}), 400
    create_item_in_db(item['key'], item['value'])
    return jsonify({'message': 'Item created successfully'}), 201

# Flask route to update an existing item
@app.route('/items/<string:key>', methods=['PUT'])
def update_item(key):
    item = request.get_json()
    if 'value' not in item:
        return jsonify({'error': 'Invalid item data'}), 400
    if get_item_from_db(key):
        update_item_in_db(key, item['value'])
        return jsonify({'message': 'Item updated successfully'})
    else:
        return jsonify({'error': 'Item not found'}), 404

# Flask route to delete an item
@app.route('/items/<string:key>', methods=['DELETE'])
def delete_item(key):
    if get_item_from_db(key):
        delete_item_from_db(key)
        return jsonify({'message': 'Item deleted successfully'})
    else:
        return jsonify({'error': 'Item not found'}), 404

if __name__ == '__main__':
    create_items_table()
    app.run(host='0.0.0.0', port=5001, debug=True)
