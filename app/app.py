import os
import subprocess
from flask import Flask, jsonify,request
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.config['upload_folder'] = '/Masaüstü/projem/mobsf./app'

@app.route('/')
def hello_world():
    return 'Hello World!'


@app.route('/upload', methods=['POST'])
def upload_file():

    if 'file' not in request.files:
        return jsonify({'error': 'Dosya bulunamadı'})
    
    upload_file = request.files['file']

    filename = secure_filename(upload_file.filename)
    upload_file.save(os.path.join(app.root_path, 'static', filename))

    if upload_file.filename == '':
        return jsonify({'error': 'Dosya adı geçersiz'})
    
    return jsonify({'message': 'Dosya başarıyla yüklendi'})


@app.route('/scan', methods=['POST'])
def scan_file():
    file_path = request.json.get('file_path')

    if file_path:
        command = ['mobsfcli' , 'scan' , '-f' , file_path]
        result = subprocess.run(command, capture_output=True, text=True , check=True)
        return jsonify({'scan_result': result.stdout})
    else:
        return jsonify({'error': 'dosya yolu bulunamadı'})


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')


