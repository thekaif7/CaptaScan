from flask import Flask, request, render_template, jsonify, url_for
import pytesseract
from PIL import Image
from captcha.image import ImageCaptcha
import os
import random
import string

app = Flask(__name__)

# Function to generate random strings for CAPTCHA
def random_string(length=5):
    letters = string.ascii_uppercase
    return ''.join(random.choice(letters) for i in range(length))

# Function to create and save a CAPTCHA image
def create_captcha():
    text = random_string()
    image = ImageCaptcha(width=280, height=90)
    image_path = os.path.join('static', f'{text}.png')
    image.write(text, image_path)
    return text, image_path

# Function to check allowed file extensions
def allowed_file(filename):
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'bmp', 'tif', 'tiff'}
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/refresh_captcha')
def refresh_captcha():
    text, path = create_captcha()
    return jsonify({'captcha_text': text, 'captcha_path': url_for('static', filename=path.split('/')[-1])})

@app.route('/', methods=['GET', 'POST'])
def examination_form():
    message = ''
    captcha_text, captcha_path = '', ''
    
    if request.method == 'POST':
        if 'document' not in request.files:
            return 'No file part', 400
        uploaded_file = request.files['document']
        
        if uploaded_file.filename == '':
            return 'No selected file', 400

        if uploaded_file and allowed_file(uploaded_file.filename):
            filepath = os.path.join('uploads', uploaded_file.filename)
            uploaded_file.save(filepath)
            text = pytesseract.image_to_string(Image.open(filepath))
            os.remove(filepath)  # Remove the file after processing

        captcha_response = request.form['captcha']
        original_captcha = request.form['original_captcha']

        if captcha_response.upper() == original_captcha:
            message = 'Form submitted successfully!'
        else:
            message = 'Invalid CAPTCHA!'
            captcha_text, captcha_path = create_captcha()

    if request.method == 'GET' or captcha_path == '':
        captcha_text, captcha_path = create_captcha()

    return render_template('form.html', message=message, captcha_path=captcha_path, captcha_text=captcha_text)

if __name__ == '__main__':
    app.run(debug=True, port=8080)  # Change the port as needed
