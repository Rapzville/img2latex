import os
from flask import Flask, render_template, url_for, redirect, request, flash, make_response
from werkzeug.utils import secure_filename
from model import predict


UPLOAD_FOLDER = 'static/uploaded/'

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
            
            if not os.path.exists(app.config['UPLOAD_FOLDER']):
                os.mkdir(app.config['UPLOAD_FOLDER'])

            filename = secure_filename(file.filename)
            
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            
            return redirect(url_for('uploaded', filename=filename))
    
    return render_template('index.html')

@app.route('/uploaded/<filename>')
def uploaded(filename):
    res = predict(f'static/uploaded/{filename}')
    context = {}
    context['filename'] = "uploaded/" + filename
    context['res'] = res
    if request.cookies.get('history'):
        context['history'] = request.cookies.get('history').split()
    else:
        context['history'] = []
    page = make_response(render_template("second.html", context=context))
    if not request.cookies.get('history'):
        page.set_cookie('history', filename, max_age=60*60*24*7)
    else:
        if len(context['history']) > 2:
            a, b = context['history'][:2]
            
            page.set_cookie('history', a + ' ' + b +' '+filename, max_age=60*60*24*7)
        else:
            a = context['history'][0]
            page.set_cookie('history', a + ' ' +filename, max_age=60*60*24*7)

    return page 

if __name__ == '__main__':
    app.config['SECRET_KEY'] = 'secret'
    app.run(debug=True)
