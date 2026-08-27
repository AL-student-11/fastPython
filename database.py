import sqlite3
from datetime import datetime

DATABASE = "events.db"

def get_connection():
    connection = sqlite3.connect(DATABASE)
    connection.row_factory = sqlite3.Row
    return connection

def get_all_events():
    connection = get_connection()
    events = connection.execute(
        "SELECT * FROM events"
    ).fetchall()
    connection.close()
    return [dict(event) for event in events]

def get_event(event_id):
    connection = get_connection()
    event = connection.execute(
        "SELECT * FROM events WHERE id = ?",
        (event_id,)
    ).fetchone()
    connection.close()
    if event is None:
        return None
    return dict(event)

def get_event_registrations(event_id):
    connection = get_connection()
    registrations = connection.execute(
        "SELECT * FROM registrations WHERE event_id = ?",
        (event_id,)
    ).fetchall()
    connection.close()
    return [dict(registration) for registration in registrations]

def get_upcoming_events(location):
    now = datetime.today().strftime('%Y-%m-%d %H:%M:S')
    connection = get_connection()
    events = connection.execute(
        "SELECT * FROM events WHERE date > ? AND location = ?",
        (now, location)
    ).fetchall()
    connection.close()
    if events is None:
        return None
    return [dict(event) for event in events]

def delete_event(event_id):
    connection = get_connection()
    connection.execute(
        "DELETE FROM events WHERE id = ?",
        (event_id,)
    )
    connection.commit()
    connection.close()

def create_event(name, description, location, date, capacity):
    connection = get_connection()
    connection.execute(
        "INSERT INTO events (name, description, location, date, capacity) VALUES (?,?,?,?,?)",
        (name, description, location, date, capacity)
    )
    connection.commit()
    event_id = connection.execute("SELECT last_insert_rowid()").fetchone()[0]
    connection.close()
    return event_id

def update_event(event_id, name, description, location, date, capacity):
    connection = get_connection()
    connection.execute(
        "UPDATE events SET name = ?, description = ?, location = ?, date = ?, capacity = ? WHERE id = ?",
        (name, description, location, date, capacity, event_id)
    )
    connection.commit()
    connection.close()

def get_registration(registration_id):
    connection = get_connection()
    registration = connection.execute(
        "SELECT * FROM registrations WHERE id = ?",
        (registration_id,)
    ).fetchone()
    connection.close()
    if registration is None:
        return None
    return dict(registration)

def create_registration(event_id, name, email):
    now = datetime.today().strftime('%Y-%m-%d %H:%M:%S')
    connection = get_connection()
    connection.execute(
        "INSERT INTO registrations (event_id, name, email, created_at) VALUES (?,?,?,?)",
        (event_id, name, email, now)
    )
    connection.commit()
    event_id = connection.execute("SELECT last_insert_rowid()").fetchone()[0]
    connection.close()
    return event_id

def update_registration(registration_id, name, email):
    connection = get_connection()
    connection.execute(
        "UPDATE registrations SET name = ?, email = ? WHERE id = ?",
        (name, email, registration_id)
    )
    connection.commit()
    connection.close()
    
def delete_registration(registration_id):
    connection = get_connection()
    connection.execute(
        "DELETE FROM registrations WHERE id = ?",
        (registration_id,)
    )
    connection.commit()
    connection.close()

def get_capacity(event_id):
    connection = get_connection()
    result = connection.execute(
        "SELECT capacity FROM events WHERE id = ?",
        (event_id,)
    ).fetchone()
    connection.close()
    if result is None:
        return None
    capacity = result[0]
    return capacity

def get_number_of_registrations(event_id):
    connection = get_connection()
    result = connection.execute(
        "SELECT COUNT(event_id) FROM registrations WHERE event_id = ?",
        (event_id,)
    ).fetchone()
    connection.close()
    number_of_registrations = result[0]
    return number_of_registrations
