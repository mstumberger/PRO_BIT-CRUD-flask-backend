from run import app
from flask import jsonify, send_from_directory, flash, request, redirect, url_for
from werkzeug.utils import secure_filename
import os


@app.route('/')
def index():
    return jsonify({'message': 'Hello, World!'})


@app.route('/static/<path:path>')
def repository(path):
    print("File {} was downloaded.".format(path))
    return send_from_directory(app.config['UPLOAD_FOLDER'], path)


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']


@app.route('/upload', methods=['POST'])
def upload_file():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        # if user does not select file, browser also
        # submit an empty part without filename
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            return redirect(url_for('uploaded_file', filename=filename))
    return
