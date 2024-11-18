import os
from flask import Flask, render_template, url_for, redirect, request, flash
from werkzeug.utils import secure_filename
from model_predict import img2latex

# папка для сохранения загруженных файлов
UPLOAD_FOLDER = '/uploaded/'
# расширения файлов, которые разрешено загружать
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'webp'}

app = Flask(__name__)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):
    """ Функция проверки расширения файла """
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

with app.test_request_context():
    pass

@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        # проверим, передается ли в запросе файл 

        if 'file' not in request.files:
            # После перенаправления на страницу загрузки
            # покажем сообщение пользователю 
            flash('Файл не найден в запросе!')
            return redirect(request.url)
        file = request.files['file']
        # Если файл не выбран, то браузер может
        # отправить пустой файл без имени.
        if file.filename == '':
            flash('Нет выбранного файла')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            # безопасно извлекаем оригинальное имя файла
            filename = secure_filename(file.filename)
            # сохраняем файл
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename)[1:])
            # если все прошло успешно, то перенаправляем  
            # на функцию-представление `download_file` 
            # для скачивания файла
            with app.test_request_context():
                print(os.path.join(app.config['UPLOAD_FOLDER'], filename)[1:])
            return redirect(url_for('result', filename=filename))
    
    return render_template('index.html')

@app.route('/result/<filename>')
def download_file(filename):
    return f'Функционал загрузки файла {filename} еще не реализован.'

if __name__ == '__main__':
    app.config['SECRET_KEY'] = 'secret'
    app.run(debug=True)
