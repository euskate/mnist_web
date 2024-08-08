from flask import Flask, render_template, request, jsonify
import base64
import numpy as np
from tensorflow.keras.models import load_model
from PIL import Image
import io

app = Flask(__name__)
model = load_model('mnist_model.h5')  # 사전에 학습된 모델 로드


@app.route('/')
def home():
    return render_template('index_old.html')


@app.route('/predict', methods=['POST'])
def predict():
    data = request.get_json()
    img_data = data['image'].split(",")[1]
    print(img_data)
    img = Image.open(io.BytesIO(base64.b64decode(img_data)))
    img = img.convert("L").resize((28, 28))  # 이미지를 28x28 크기로 변환
    img = np.array(img)
    img = img / 255.0  # 모델 입력에 맞게 조정
    img = img.reshape(1, 28 * 28)  # 1D 벡터로 변환

    prediction = model.predict(img)
    digit = np.argmax(prediction)

    # 예측 확률 출력 (디버깅용)
    print(f"Prediction probabilities: {prediction}")
    print(f"Predicted digit: {digit}")

    return jsonify({"digit": int(digit)})


if __name__ == '__main__':
    app.run(debug=True)
