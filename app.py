from flask import Flask, render_template, request, jsonify, redirect, url_for
from tensorflow.keras.models import load_model
import numpy as np
from PIL import Image
import os
import matplotlib.pyplot as plt

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/im')
def im(result=None):
    return render_template('im.html', result=result)

# 설정: 업로드된 파일을 저장할 디렉토리
app.config['UPLOAD_FOLDER'] = 'uploads/'
app.config['ALLOWED_EXTENSIONS'] = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}

# 파일 확장자가 허용된 것인지 확인하는 함수
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']
def process_file(file_path):
    try:
        with Image.open(file_path) as img:
            if img.mode != 'L':
                img = img.convert('L')
            # img = img.resize((28, 28))
            img_array = np.array(img)
            model = load_model('mnist_model.h5')
            test_data = img_array.reshape(1, 784)
            yhat_test = model.predict(test_data)
            print(np.argmax(yhat_test))
            processed_data = np.argmax(yhat_test)

            return str(processed_data)
    except Exception as e:
        return f"Error processing file: {e}"

@app.route('/upload', methods=['POST'])
def upload():
    data = request.json
    image_data = data.get('image')
    # 이미지 데이터를 처리하는 코드 추가
    # 예: image_data를 리스트로 변환
    image_list = list(map(int, image_data.split(',')))


    model = load_model('mnist_model.h5')
    test_data = np.array(image_list)
    test_data = test_data.reshape(1, 784)
    yhat_test = model.predict(test_data)
    print(np.argmax(yhat_test))

    # 필요한 추가 처리 수행
    processed_data = np.argmax(yhat_test)

    return jsonify({'status': 'success', 'processed_data': int(processed_data)})


@app.route('/upload2', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return im("No file part")
    file = request.files['file']

    # 파일이 없거나 파일명이 비어있는 경우
    if file.filename == '':
        return im("No selected file")

    # 파일이 허용된 형식인지 확인
    if file and allowed_file(file.filename):
        filename = file.filename
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(file_path)

        # 파일을 읽어 처리
        result = process_file(file_path)

        return im(result)

    return im("File type is not allowed")


if __name__ == '__main__':
    app.run(debug=True)




# from flask import Flask, render_template
#
# app = Flask(__name__)
#
# @app.route('/')
# def home():
#     name = "Alice"
#     value = 42
#     return render_template('index.html', name=name, value=value)
#
# if __name__ == '__main__':
#     app.run(debug=True)

