from flask import Flask, request, render_template, jsonify
from tensorflow.keras.models import load_model
import numpy as np
from PIL import Image
import base64
from io import BytesIO
import os

app = Flask(__name__)
model = load_model('mnist_cnn_model.h5')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    data = request.get_json()
    image_data = data['image']
    image_data = image_data.split(',')[1]
    image_data = base64.b64decode(image_data)

    # Convert the base64 encoded image to a PIL image
    img = Image.open(BytesIO(image_data)).convert('L')

    # Resize the image to 28x28 (same as MNIST images)
    img = img.resize((28, 28))

    # Convert the image to a numpy array
    img_array = np.array(img)

    # Normalize the image to fit the model input requirements
    img_array = img_array.astype('float32') / 255.0

    # Reshape the image array to match the model input shape
    img_array = img_array.reshape(-1, 28, 28, 1)

    # Make a prediction using the model
    prediction = model.predict(img_array)
    digit = np.argmax(prediction)

    return jsonify({'prediction': int(digit)})

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)
