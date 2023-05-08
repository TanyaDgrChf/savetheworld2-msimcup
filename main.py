from flask import Flask, render_template, request, redirect, session
from datetime import datetime, timedelta
import pytz
import os
import sqlite3
print(os.getcwd())
app = Flask(__name__)
app.secret_key = 'some_secret_key'

@app.route('/')
def index():
    return render_template('login.html')

@app.route('/login', methods=['POST'])
def login():
    username = request.form['username']
    password = request.form['password']

    # Retrieve password from database
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute("SELECT password FROM users WHERE username=?", (username,))
    result = c.fetchone()
    conn.close()

    if result and password == result[0]:
        # Set the isLoggedIn variable and its expiration time in the session
        session['isLoggedIn'] = True
        session['expires_at'] = datetime.now(pytz.utc) + timedelta(minutes=1)
        return redirect('/success')

    return redirect('/')

@app.route('/success')
def success():
    # Check if isLoggedIn is True and not expired
    isLoggedIn = session.get('isLoggedIn', False)
    expires_at = session.get('expires_at')
    if isLoggedIn and expires_at and expires_at > datetime.now(pytz.utc):
        # Record the login time and IP address
        login_time = datetime.now(pytz.utc).strftime('%Y-%m-%d %H:%M:%S')
        ip_address = request.remote_addr
        with open('textFiles/login_logs.txt', 'a') as f:
            f.write(f'{login_time} - {ip_address}\n')
        return render_template('success.html')
    else:
        return redirect('/')

@app.route('/display_text', methods=['POST'])
def display_text():
    selected_option = request.form.get('option')
    if selected_option:
        # Retrieve text based on the selected option from a text file
        with open(f'textFiles/{selected_option}.txt', 'r') as f:
            text = f.read()
        return render_template('success.html', selected_option=selected_option, text=text)
    else:
        return redirect('/')

if __name__ == '__main__':
    app.run(debug=True)
