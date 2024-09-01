import psycopg2
import os
import json

def lambda_handler(event, context):
    # Set up database connection
    conn = psycopg2.connect(
        host=os.getenv('DB_HOST'),
        dbname=os.getenv('DB_NAME'),
        user=os.getenv('DB_USER'),
        password=os.getenv('DB_PASSWORD'),
        port=os.getenv('DB_PORT')
    )
    cur = conn.cursor()

    # Determine the operation based on the event input
    operation = event.get('operation')

    if operation == 'create':
        # Create operation
        sql = "INSERT INTO items (name, description) VALUES (%s, %s)"
        data = (event['data']['name'], event['data']['description'])
        cur.execute(sql, data)
        conn.commit()
        response = {'message': 'Record created'}

    elif operation == 'read':
        # Read operation
        cur.execute("SELECT id, name, description FROM items")
        records = cur.fetchall()
        response = {'records': [{'id': r[0], 'name': r[1], 'description': r[2]} for r in records]}

    elif operation == 'update':
        # Update operation
        sql = "UPDATE items SET name = %s, description = %s WHERE id = %s"
        data = (event['data']['name'], event['data']['description'], event['data']['id'])
        cur.execute(sql, data)
        conn.commit()
        response = {'message': 'Record updated'}

    elif operation == 'delete':
        # Delete operation
        sql = "DELETE FROM items WHERE id = %s"
        data = (event['data']['id'],)
        cur.execute(sql, data)
        conn.commit()
        response = {'message': 'Record deleted'}

    else:
        response = {'message': 'Operation not supported'}

    # Close the database connection
    cur.close()
    conn.close()

    return {
        'statusCode': 200,
        'body': json.dumps(response),
        'headers': {
            'Content-Type': 'application/json'
        }
    }
