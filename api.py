from flask import Flask, request, jsonify
import sqlite3

app = Flask(__name__)
DATABASE = 'student_management.db'


def get_db():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn


@app.route('/students', methods=['GET', 'POST'])
def handle_students():
    conn = get_db()
    cursor = conn.cursor()

    if request.method == 'POST':
        new_student = request.get_json()
        cursor.execute('''
            INSERT INTO students (first_name, last_name, middle_name, birth_date, phone, email, address) 
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (new_student['first_name'], new_student['last_name'], new_student['middle_name'],
              new_student['birth_date'], new_student['phone'], new_student['email'], new_student['address']))
        conn.commit()
        return jsonify({'message': 'Student added successfully'}), 201

    elif request.method == 'GET':
        cursor.execute('SELECT * FROM students')
        students = cursor.fetchall()
        return jsonify([dict(ix) for ix in students]), 200


@app.route('/students/<int:id>', methods=['GET', 'PUT', 'DELETE'])
def handle_student(id):
    conn = get_db()
    cursor = conn.cursor()

    if request.method == 'GET':
        cursor.execute('SELECT * FROM students WHERE id=?', (id,))
        student = cursor.fetchone()
        if student:
            return jsonify(dict(student)), 200
        return jsonify({'message': 'Student not found'}), 404

    elif request.method == 'PUT':
        updated_student = request.get_json()
        cursor.execute('''
            UPDATE students SET first_name=?, last_name=?, middle_name=?, birth_date=?, phone=?, email=?, address=? 
            WHERE id=?
        ''', (updated_student['first_name'], updated_student['last_name'], updated_student['middle_name'],
              updated_student['birth_date'], updated_student['phone'], updated_student['email'],
              updated_student['address'], id))
        conn.commit()
        return jsonify({'message': 'Student updated successfully'}), 200

    elif request.method == 'DELETE':
        cursor.execute('DELETE FROM students WHERE id=?', (id,))
        conn.commit()
        return jsonify({'message': 'Student deleted successfully'}), 200


@app.route('/events', methods=['GET', 'POST'])
def handle_events():
    conn = get_db()
    cursor = conn.cursor()

    if request.method == 'POST':
        new_event = request.get_json()
        cursor.execute('''
            INSERT INTO events (student_id, date, title, description, category) 
            VALUES (?, ?, ?, ?, ?)
        ''', (new_event['student_id'], new_event['date'], new_event['title'], new_event['description'],
              new_event['category']))
        conn.commit()
        return jsonify({'message': 'Event added successfully'}), 201

    elif request.method == 'GET':
        cursor.execute('SELECT * FROM events')
        events = cursor.fetchall()
        return jsonify([dict(ix) for ix in events]), 200


@app.route('/events/<int:id>', methods=['GET', 'PUT', 'DELETE'])
def handle_event(id):
    conn = get_db()
    cursor = conn.cursor()

    if request.method == 'GET':
        cursor.execute('SELECT * FROM events WHERE id=?', (id,))
        event = cursor.fetchone()
        if event:
            return jsonify(dict(event)), 200
        return jsonify({'message': 'Event not found'}), 404

    elif request.method == 'PUT':
        updated_event = request.get_json()
        cursor.execute('''
            UPDATE events SET student_id=?, date=?, title=?, description=?, category=? 
            WHERE id=?
        ''', (updated_event['student_id'], updated_event['date'], updated_event['title'],
              updated_event['description'], updated_event['category'], id))
        conn.commit()
        return jsonify({'message': 'Event updated successfully'}), 200

    elif request.method == 'DELETE':
        cursor.execute('DELETE FROM events WHERE id=?', (id,))
        conn.commit()
        return jsonify({'message': 'Event deleted successfully'}), 200


if __name__ == '__main__':
    app.run(debug=True)