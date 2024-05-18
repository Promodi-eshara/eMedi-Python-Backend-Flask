from flask import Flask
from flask_cors import CORS, cross_origin

from routes.voice_to_text import voice_to_text_bp
from routes.predict_doctors import predict_doctors_bp

app = Flask(__name__)

CORS(app, resources={r"/voice_to_text": {"origins": "http://localhost:3000"}})

app.register_blueprint(voice_to_text_bp)
app.register_blueprint(predict_doctors_bp)

if __name__ == "__main__":
    app.run(debug=True)

