from flask import Flask, render_template, request, redirect, session
import os
import sqlite3
from imageProcess import *

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
        # Set the isLoggedIn variable in the session
        session['isLoggedIn'] = True
        return redirect('/success')

    return redirect('/')

@app.route('/success', methods=['GET', 'POST'])
def success():
    # Check if isLoggedIn is True
    isLoggedIn = session.get('isLoggedIn', False)
    if request.method == 'POST' and isLoggedIn:
        # Save the uploaded PNG file to the tempImageStore folder
        image = request.files['image']
        if image and image.filename.endswith('.png'):
            image_path = os.path.join('tempImageStore', image.filename)
            image.save(image_path)

            # Send image to IMAGGA and get tags
            guesses = sendImage(image_path)

            # Check tags against keywords in database
            results = checkText(guesses)

            # Render success.html with tags and results
            return render_template('success.html', tags=guesses, results=results)
    elif isLoggedIn:
        return render_template('success.html')
    else:
        return redirect('/')

@app.route('/upload_png', methods=['POST'])
def upload_png():
    # Check if isLoggedIn is True
    isLoggedIn = session.get('isLoggedIn', False)
    if not isLoggedIn:
        return redirect('/')
    return redirect('/success')

if __name__ == '__main__':
    app.run(debug=True)
