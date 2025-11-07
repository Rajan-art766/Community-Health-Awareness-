from flask import Flask, render_template, request, redirect, url_for, flash, session
import sqlite3
import os

app = Flask(__name__)
app.secret_key = 'secret_key'  # Required for session and flash messages

DB_PATH = "database.db"
os.makedirs("database", exist_ok=True)

# Initialize database
def init_db():
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS event_registration (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT, email TEXT, event TEXT, role TEXT
        )''')
        cursor.execute('''CREATE TABLE IF NOT EXISTS contact_messages (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT, email TEXT, message TEXT
        )''')
        cursor.execute('''CREATE TABLE IF NOT EXISTS community_stories (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT, email TEXT, title TEXT, story TEXT
        )''')
        cursor.execute('''CREATE TABLE IF NOT EXISTS admin_events (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT, date TEXT, location TEXT, description TEXT
        )''')
        cursor.execute('''
                    CREATE TABLE IF NOT EXISTS community_stories (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        name TEXT,
                        email TEXT,
                        title TEXT,
                        story TEXT
                    )
                ''')

init_db()

# Admin credentials
ADMIN_USERNAME = "Community"
ADMIN_PASSWORD = "COE2025"

@app.route('/admin', methods=['GET', 'POST'])
def admin():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if username == ADMIN_USERNAME and password == ADMIN_PASSWORD:
            session['admin_logged_in'] = True
            return redirect(url_for('admin'))
        else:
            flash("Invalid username or password", "danger")
            return redirect(url_for('admin'))

    if not session.get('admin_logged_in'):
        return render_template('admin.html', login=True)

    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT name, email, title, story FROM community_stories")
        stories = cursor.fetchall()
        cursor.execute("SELECT name, email, event, role FROM event_registration")
        registrations = cursor.fetchall()
        cursor.execute("SELECT name, email, message FROM contact_messages")
        messages = cursor.fetchall()
        cursor.execute("SELECT title, date, location, description FROM admin_events")
        event_list = cursor.fetchall()

    return render_template('admin.html', login=False, stories=stories, registrations=registrations, messages=messages, event_list=event_list)

@app.route('/logout')
def logout():
    session.pop('admin_logged_in', None)
    flash("Logged out successfully", "info")
    return redirect(url_for('admin'))

# @app.route('/add_story_admin', methods=['POST'])
# def add_story_admin():
#     name = request.form['name']
#     email = request.form['email']
#     title = request.form['title']
#     story = request.form['story']
#     with sqlite3.connect(DB_PATH) as conn:
#         cursor = conn.cursor()
#         cursor.execute("INSERT INTO community_stories (name, email, title, story) VALUES (?, ?, ?, ?)", (name, email, title, story))
#         conn.commit()
#     flash("Story added successfully", "success")
#     return redirect(url_for('admin'))
#
# @app.route('/delete_story', methods=['POST'])
# def delete_story():
#     email = request.form['email']
#     title = request.form['title']
#     with sqlite3.connect(DB_PATH) as conn:
#         cursor = conn.cursor()
#         cursor.execute("DELETE FROM community_stories WHERE email=? AND title=?", (email, title))
#         conn.commit()
#     flash("Story deleted", "info")
#     return redirect(url_for('admin'))
@app.route('/stories', methods=['GET', 'POST'])
def stories():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        title = request.form['title']
        story = request.form['story']

        with sqlite3.connect(DB_PATH) as conn:
            cursor = conn.cursor()
            cursor.execute("INSERT INTO community_stories (name, email, title, story) VALUES (?, ?, ?, ?)",
                           (name, email, title, story))
            conn.commit()
        flash("Your story has been submitted!", "success")
        return redirect(url_for('stories'))

    # GET method - show all stories
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT name, email, title, story FROM community_stories")
        stories = cursor.fetchall()
    return render_template('stories.html', stories=stories)

@app.route('/add_contact_admin', methods=['POST'])
def add_contact_admin():
    name = request.form['name']
    email = request.form['email']
    message = request.form['message']
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        cursor.execute("INSERT INTO contact_messages (name, email, message) VALUES (?, ?, ?)", (name, email, message))
        conn.commit()
    flash("Message added", "success")
    return redirect(url_for('admin'))

@app.route('/delete_contact', methods=['POST'])
def delete_contact():
    email = request.form['email']
    message = request.form['message']
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM contact_messages WHERE email=? AND message=?", (email, message))
        conn.commit()
    flash("Message deleted", "info")
    return redirect(url_for('admin'))

@app.route('/add_event_admin', methods=['POST'])
def add_event_admin():
    title = request.form['title']
    date = request.form['date']
    location = request.form['location']
    description = request.form['description']
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        cursor.execute("INSERT INTO admin_events (title, date, location, description) VALUES (?, ?, ?, ?)", (title, date, location, description))
        conn.commit()
    flash("Event added successfully", "success")
    return redirect(url_for('admin'))

@app.route('/delete_event', methods=['POST'])
def delete_event():
    title = request.form['title']
    date = request.form['date']
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM admin_events WHERE title=? AND date=?", (title, date))
        conn.commit()
    flash("Event deleted", "info")
    return redirect(url_for('admin'))

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/topics')
def topics():
    return render_template('topics.html')

@app.route('/add_story_admin', methods=['POST'])
def add_story_admin():
    if not session.get('admin_logged_in'):
        return redirect(url_for('admin'))

    name = request.form['name']
    email = request.form['email']
    title = request.form['title']
    story = request.form['story']

    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        cursor.execute("INSERT INTO community_stories (name, email, title, story) VALUES (?, ?, ?, ?)",
                       (name, email, title, story))
        conn.commit()

    flash("Story added successfully!", "success")
    return redirect(url_for('admin'))

@app.route('/delete_story', methods=['POST'])
def delete_story():
    if not session.get('admin_logged_in'):
        return redirect(url_for('admin'))

    email = request.form['email']
    title = request.form['title']

    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM community_stories WHERE email=? AND title=?", (email, title))
        conn.commit()

    flash("Story deleted successfully!", "info")
    return redirect(url_for('admin'))

@app.route('/events', methods=['GET', 'POST'])
def events():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        event = request.form['event']
        role = request.form['role']
        with sqlite3.connect(DB_PATH) as conn:
            cursor = conn.cursor()
            cursor.execute("INSERT INTO event_registration (name, email, event, role) VALUES (?, ?, ?, ?)", (name, email, event, role))
            conn.commit()
        flash("Event registration successful!", "success")
        return redirect(url_for('events'))

    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT title, date, location, description FROM admin_events")
        events = cursor.fetchall()
    return render_template('events.html', events=events)

@app.route('/contact', methods=['GET', 'POST'])
def contact():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        message = request.form['message']
        with sqlite3.connect(DB_PATH) as conn:
            cursor = conn.cursor()
            cursor.execute("INSERT INTO contact_messages (name, email, message) VALUES (?, ?, ?)", (name, email, message))
            conn.commit()
        flash("Your message has been sent!", "success")
        return redirect(url_for('contact'))
    return render_template('contact.html')

if __name__ == '__main__':
    app.run(debug=True)

