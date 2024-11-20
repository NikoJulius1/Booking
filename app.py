import sqlite3
from flask import Flask, request, jsonify, Response
import requests
import csv
from io import StringIO
from flask import Flask
from swagger.config import init_swagger  # Adjust the path if needed

app = Flask(__name__)
swagger = init_swagger(app)

# Connect to the SQLite database
def get_db_connection():
    return sqlite3.connect('reservation_database.db')

def notify_billing_service(booking_id, room_type, checkin, checkout):
    try:
        billing_url = f'http://billing-service:5002/bills/update/{booking_id}'
        data = {
            'room_type': room_type,
            'checkin': checkin,
            'checkout': checkout
        }
        
        # Debug output
        print(f"Sending data to billing service: {data}")  # Vis dataene, der sendes
        print(f"Billing service URL: {billing_url}")  # Vis URL'en til billing service

        response = requests.post(billing_url, json=data)
        response.raise_for_status()  # Raise an error for bad responses
        
        # Debug output for response
        print(f"Billing service response for booking {booking_id}: {response.json()}")
    except requests.exceptions.RequestException as e:
        print(f"Error contacting billing service: {e}")

# Check room availability
def isAvailable(roomnumber, checkin, checkout):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('''SELECT * FROM booking WHERE roomnumber = ? AND checkin < ? AND checkout > ?''',
                   (roomnumber, checkout, checkin))
    overlapping_bookings = cursor.fetchall()
    conn.close()
    return len(overlapping_bookings) == 0

# List all bookings
@app.route('/bookings', methods=['GET'])
@swag_from({
    'tags': ['Bookings'],
    'summary': 'List all bookings',
    'description': 'Retrieve a list of all bookings in the database.',
    'responses': {
        200: {
            'description': 'A list of bookings',
            'schema': {
                'type': 'array',
                'items': {
                    'type': 'object',
                    'properties': {
                        'id': {'type': 'integer', 'example': 1},
                        'roomnumber': {'type': 'integer', 'example': 101},
                        'category': {'type': 'string', 'example': 'Deluxe'},
                        'isbooking': {'type': 'boolean', 'example': True},
                        'checkin': {'type': 'string', 'format': 'date', 'example': '2024-11-25'},
                        'checkout': {'type': 'string', 'format': 'date', 'example': '2024-11-30'}
                    }
                }
            }
        }
    }
})
def list_bookings():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM booking')
    bookings = cursor.fetchall()
    conn.close()
    return jsonify(bookings)

# Create a new booking
@app.route('/bookings', methods=['POST'])
@swag_from({
    'tags': ['Bookings'],  # Tag grouping
    'summary': 'Create a new booking',  # Short summary
    'description': 'Create a booking by providing room details, category, and dates.',  # Detailed description
    'parameters': [  # Define the expected parameters
        {
            'in': 'body',
            'name': 'body',
            'required': True,
            'schema': {
                'type': 'object',
                'required': ['roomnumber', 'category', 'checkin', 'checkout'],  # Required fields
                'properties': {
                    'roomnumber': {'type': 'integer', 'example': 101},
                    'category': {'type': 'string', 'example': 'Deluxe'},
                    'checkin': {'type': 'string', 'format': 'date', 'example': '2024-11-25'},
                    'checkout': {'type': 'string', 'format': 'date', 'example': '2024-11-30'}
                }
            }
        }
    ],
    'responses': {  # Possible responses
        201: {'description': 'Booking created successfully.'},
        400: {'description': 'Invalid request. Missing or incorrect data.'},
        409: {'description': 'Room not available.'}
    }
})
def create_booking():
    data = request.get_json()
    roomnumber = data.get('roomnumber')
    category = data.get('category')
    checkin = data.get('checkin')
    checkout = data.get('checkout')

    if not roomnumber or not category or not checkin or not checkout:
        return jsonify({"error": "All fields are required"}), 400

    if isAvailable(roomnumber, checkin, checkout):
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''INSERT INTO booking (roomnumber, category, isbooking, checkin, checkout)
                              VALUES (?, ?, 1, ?, ?)''', (roomnumber, category, checkin, checkout))
            conn.commit()
            booking_id = cursor.lastrowid
        
        # Notify billing service with booking details
        notify_billing_service(booking_id, category, checkin, checkout)
        return jsonify({"message": "Booking created successfully"}), 201
    else:
        return jsonify({"message": "Room not available"}), 409

# Export bookings in CSV format
@app.route('/bookings/export/csv', methods=['GET'])
@app.route('/bookings/export/csv', methods=['GET'])
@swag_from({
    'tags': ['Bookings'],
    'summary': 'Export bookings as CSV',
    'description': 'Download a CSV file containing all bookings in the system.',
    'responses': {
        200: {
            'description': 'CSV file generated',
            'content': {
                'text/csv': {}
            }
        }
    }
})
def export_bookings_csv():
    output = StringIO()
    writer = csv.writer(output)
    writer.writerow(['id', 'roomnumber', 'category', 'isbooking', 'checkin', 'checkout'])
    
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM booking')
        rows = cursor.fetchall()
        writer.writerows(rows)
    
    output.seek(0)
    return Response(output.getvalue(), mimetype='text/csv', headers={"Content-Disposition": "attachment;filename=bookings.csv"})

if __name__ == '__main__':
    app.run()