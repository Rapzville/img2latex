import os
from flask import Flask, render_template, url_for, redirect, request, flash
from werkzeug.utils import secure_filename
from model import predict


UPLOAD_FOLDER = '/uploaded/'

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'webp'}

app = Flask(__name__)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):
    
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        if 'file' not in request.files:    
            return redirect(request.url)

        file = request.files['file']

        # Если файл не выбран, то браузер может
        # отправить пустой файл без имени.
        if file.filename == '':
            flash('Нет выбранного файла')
            return redirect(request.url)
        
        if file and allowed_file(file.filename):

            filename = secure_filename(file.filename)
            
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename)[1:])
            
            return redirect(url_for('uploaded', filename=filename))
    
    return render_template('index.html')

@app.route('/uploaded/<filename>')
def uploaded(filename):
    res = predict(f'uploaded/{filename}')
    os.remove(f'uploaded/{filename}')
    return f'{res}'

if __name__ == '__main__':
    app.config['SECRET_KEY'] = 'secret'
    app.run(debug=True)
