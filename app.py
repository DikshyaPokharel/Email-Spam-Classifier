from flask import Flask, render_template, request, jsonify
from model.preprocessor import preprocess_text
import tensorflow as tf
import numpy as np
from tensorflow.keras.preprocessing.sequence import pad_sequences
import pickle

app = Flask(__name__)

# Load the saved model and tokenizer
model = tf.keras.models.load_model('spam_model.keras')  # Changed from .h5 to .keras
with open('tokenizer.pickle', 'rb') as handle:
    tokenizer = pickle.load(handle)

maxlength = 1000  # Use the same maxlength as during training

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    try:
        # Get the text from the POST request
        text = request.form['message']
        
        # Preprocess the text
        processed_text = preprocess_text(text)
        
        # Convert text to sequence and pad it
        sequence = tokenizer.texts_to_sequences([processed_text])
        padded = pad_sequences(sequence, maxlen=maxlength, padding='post')
        
        # Make prediction
        prediction = model.predict(padded)
        probability = float(prediction[0][0])
        
        # Convert probability to classification
        is_spam = probability > 0.5
        
        result = {
            'is_spam': bool(is_spam),
            'probability': round(probability * 100, 2),
            'processed_text': processed_text
        }
        
        return render_template('result.html', result=result)
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)