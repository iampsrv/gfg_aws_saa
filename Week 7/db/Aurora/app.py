from flask import Flask, jsonify, request
import psycopg2
from psycopg2 import sql
import os

app = Flask(__name__)

# Aurora (PostgreSQL) Database Configuration
AURORA_HOST = ''
AURORA_PORT = '5432'
AURORA_DBNAME = 'database1'          
AURORA_USER = 'pranjal'                
AURORA_PASSWORD = 'pranjal123'             

# Database Connection
def get_db_connection():
    return psycopg2.connect(
        host=AURORA_HOST,
        port=AURORA_PORT,
        dbname=AURORA_DBNAME,
        user=AURORA_USER,
        password=AURORA_PASSWORD
    )

# Create items table if it does not exist
def create_items_table():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS items (
            id SERIAL PRIMARY KEY,
            key TEXT NOT NULL UNIQUE,
            value TEXT NOT NULL
        )
    ''')
    conn.commit()
    cursor.close()
    conn.close()

# Fetch all items
def get_all_items_from_db():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT key, value FROM items')
    items = cursor.fetchall()
    cursor.close()
    conn.close()
    return [{'key': item[0], 'value': item[1]} for item in items]

# Fetch a single item by key
def get_item_from_db(key):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT key, value FROM items WHERE key = %s', (key,))
    item = cursor.fetchone()
    cursor.close()
    conn.close()
    if item:
        return {'key': item[0], 'value': item[1]}
    return None

# Insert a new item
def create_item_in_db(key, value):
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute('INSERT INTO items (key, value) VALUES (%s, %s)', (key, value))
        conn.commit()
        return True
    except psycopg2.Error as e:
        print(f"Error inserting item: {e}")
        return False
    finally:
        cursor.close()
        conn.close()

# Update an existing item
def update_item_in_db(key, value):
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute('UPDATE items SET value = %s WHERE key = %s', (value, key))
        conn.commit()
        return True
    except psycopg2.Error as e:
        print(f"Error updating item: {e}")
        return False
    finally:
        cursor.close()
        conn.close()

# Delete an item
def delete_item_from_db(key):
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute('DELETE FROM items WHERE key = %s', (key,))
        conn.commit()
        return True
    except psycopg2.Error as e:
        print(f"Error deleting item: {e}")
        return False
    finally:
        cursor.close()
        conn.close()

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
    create_items_table()
    app.run(host='0.0.0.0', port=5001, debug=True)
