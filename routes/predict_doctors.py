from flask import request, jsonify, Blueprint, send_file
import pickle
import os
import nltk
from nltk.corpus import stopwords
import re
import json
import random

# Download NLTK resources
nltk.download('punkt')
nltk.download('stopwords')

predict_doctors_bp = Blueprint('predict_doctors_bp', __name__)

def preprocess(text):
    # Tokenize the text
    tokens = nltk.word_tokenize(text)
    
    # Lowercase each token and remove stop words
    stop_words = set(stopwords.words('english'))
    processed_tokens = [token.lower() for token in tokens if token.lower() not in stop_words]
    
    # Remove HTML characters using regular expressions
    processed_text = ' '.join(processed_tokens)
    processed_text = re.sub(r'<[^>]+>', '', processed_text)
    
    return processed_text

@predict_doctors_bp.route('/extract_disease', methods=['POST'])
def extract_disease():
    data = request.json
    input_text = data.get('input_text')

    model_file = 'LRmodel.pkl'
    if os.path.exists(model_file):
        with open(model_file, 'rb') as file:
            loaded_model = pickle.load(file)
            input_text_processed = preprocess(input_text)
            prediction = loaded_model.predict([input_text_processed])
            return {'prediction': prediction[0]}

    else:
        print(f"Error: File '{model_file}' not found.")
    return 'test'


@predict_doctors_bp.route('/get_doctors', methods=['POST'])
def get_doctors():
    data = request.json
    disease = data.get('disease')

    with open('doctors_list.json', 'r', encoding='utf-8') as json_file:
        doctors_data = json.load(json_file)

    filtered_doctors = [doctor for doctor in doctors_data if doctor.get('Diesease') == disease]
    selected_doctors = random.sample(filtered_doctors, min(len(filtered_doctors), 3))
    return jsonify(selected_doctors)