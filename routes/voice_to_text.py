from flask import request, jsonify, Blueprint , send_file
import speech_recognition as sr
import requests
import os

voice_to_text_bp = Blueprint('voice_to_text_bp', __name__)

@voice_to_text_bp.route('/download_voice', methods=['POST'])
def download_voice():
    try:
        data = request.json

        voice_file_url = data.get('voice_link')

        if not voice_file_url:
            return "No voice link provided", 400

        response = requests.get(voice_file_url)

        if response.status_code == 200:
            file_name = os.path.basename(voice_file_url)

            save_directory = "downloads"
            if not os.path.exists(save_directory):
                os.makedirs(save_directory)

            save_path = os.path.join(save_directory, file_name)

            with open(save_path, 'wb') as f:
                f.write(response.content)

            return f"File saved successfully at: {save_path}", 200
        else:
            return f"Error downloading file: {response.status_code}", 500
    except Exception as e:
        print(f"Error: {str(e)}")
        return f"Error: {str(e)}", 500

@voice_to_text_bp.route('/voice_to_text', methods=['POST'])
def voice_to_text():
    try:
        data = request.json

        voice_file_url = data.get('voice_link')

        if not voice_file_url:
            return "No voice link provided", 400

        response = requests.get(voice_file_url)

        if response.status_code == 200:
            save_directory = "downloads"
            if not os.path.exists(save_directory):
                os.makedirs(save_directory)

            file_name = os.path.basename(voice_file_url)
            save_path = os.path.join(save_directory, file_name)

            with open(save_path, 'wb') as f:
                f.write(response.content)

            print(save_path)
            
            recognizer = sr.Recognizer()
            with sr.AudioFile(save_path) as source:
                audio_data = recognizer.record(source)
                text = recognizer.recognize_google(audio_data)

            return text, 200
        else:
            return f"Error downloading file: {response.status_code}", 500
    except Exception as e:
        print(f"Error: {str(e)}")
        return f"Error: {str(e)}", 500
         
@voice_to_text_bp.route('/hello', methods=['POST'])
def hello():
    data = request.json
    print(data)

    return 'Hello'