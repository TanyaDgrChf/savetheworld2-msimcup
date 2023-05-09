from flask import Flask, render_template, request, redirect, session
import os
import sqlite3
# from imageProcess import sendImage, checkText
# import tensorflow as tf
# from tensorflow.keras.models import load_model
import numpy as np
from PIL import Image

# Load the trained model
# model = load_model('trashnet_model.h5')

app = Flask(__name__)
secret = os.environ['secret_key']
app.secret_key = secret

def init_db():
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()

    cursor.execute('''
                  CREATE TABLE IF NOT EXISTS users
                  (id INTEGER PRIMARY KEY AUTOINCREMENT,
                  username TEXT NOT NULL UNIQUE,
                  password TEXT NOT NULL)
                  ''')
  
    conn.commit()
    conn.close()

@app.route('/')
def index():
  return render_template('login.html')

@app.route('/login', methods=['POST'])
def login():
  # Check if user wants to register
  value = request.form.get('button_value')
  if value == 'yes':
    return render_template('register.html')
  else:
    # Check if user entered username/ password
    enter_user = True
    enter_pass = True
    error_pass = 'Please enter password'
    error_user = 'Please enter username'
    
    username = request.form['username']
    password = request.form['password']
  
    if not username:
      enter_user = False
    if not password:
      enter_pass = False

    if enter_user == False and enter_pass == True:
      return render_template('login.html', error_user=error_user)
    elif enter_pass == False and enter_user == True:
      return render_template('login.html', error_pass=error_pass)
    elif enter_pass == False and enter_user == False:
      return render_template('login.html', error_user=error_user, error_pass=error_pass)
    else:
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
      else:
        return redirect('/')

@app.route('/register', methods=['POST'])
def register():
  # Check if user wants to login
  value = request.form.get('button_value')
  if value == 'yes':
    return render_template('login.html')
  else:
    enter_user = True
    enter_pass = True
    error_pass = 'Please enter password'
    error_user = 'Please enter username'

    username = request.form['username']
    password = request.form['password']
    
    if not username:
      enter_user = False
    if not password:
      enter_pass = False

    if enter_user == False and enter_pass == True:
      return render_template('register.html', error_user=error_user)
    elif enter_pass == False and enter_user == True:
      return render_template('register.html', error_pass=error_pass)
    elif enter_pass == False and enter_user == False:
      return render_template('register.html', error_user=error_user, error_pass=error_pass)
    else:
      # Save the user details to a database or perform other necessary actions
      conn = sqlite3.connect('database.db')
      cursor = conn.cursor()
      cursor.execute('INSERT INTO users (username, password) VALUES (?, ?)', (username, password))
      conn.commit()
      message = 'Registration Successful!'
      # Redirect to a success page or login page
      return render_template('login.html', message=message)

@app.route('/success', methods=['GET', 'POST'])
def success():
  # Check if isLoggedIn is True
  isLoggedIn = session.get('isLoggedIn', False)
  if request.method == 'POST' and isLoggedIn:
    # Save the uploaded PNG file to the tempImageStore folder
    image = request.files['image']
    if image and image.filename.endswith('.png'):
      class_labels = ['Cardboard', 'Glass', 'Metal', 'Paper', 'Plastic', 'Trash']
      # Load and preprocess the image
      image = image.resize((224, 224))  # Resize the image to match the input size of the model
      image_array = np.array(image) / 255.0  # Normalize the pixel values

# Expand dimensions to match the input shape of the model
      input_image = np.expand_dims(image_array, axis=0)

# Make predictions
      predictions = model.predict(input_image)

# Get the predicted class index
      predicted_class_index = np.argmax(predictions[0])

# Map the predicted class index to the corresponding label
      predicted_class = class_labels[predicted_class_index]

      # Render success.html with tags and results
      return render_template('success.html', predicted_class=results)
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
    init_db()
    app.run(debug=True, host='0.0.0.0', port=81)