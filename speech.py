from flask import Flask, request, jsonify, send_file
import google.generativeai as genai
import speech_recognition as sr
import pyttsx3
from dotenv import load_dotenv
import os
load_dotenv()

app = Flask(__name__)

api_key = os.getenv('GEMINI_AI_API_KEY')
genai.configure(api_key=api_key) 

tts_engine = pyttsx3.init()

@app.route('/voice', methods=['POST'])
def process_voice():
    if 'file' not in request.files:
        return jsonify({"error": "No file uploaded"}), 400

    audio_file = request.files['file']

    recognizer = sr.Recognizer()
    with sr.AudioFile(audio_file) as source:
        audio_data = recognizer.record(source)
        try:
            user_text = recognizer.recognize_google(audio_data)
        except sr.UnknownValueError:
            return jsonify({"error": "Could not understand audio"}), 400

    print(f"User Said: {user_text}")

    model = genai.GenerativeModel("gemini-pro")
    response = model.generate_content(user_text)

    response_text = response.text
    print(f"AI Response: {response_text}")

    tts_engine.save_to_file(response_text, "response.wav")
    tts_engine.runAndWait()

    return send_file("response.wav", mimetype="audio/wav")

if __name__ == '__main__':
    app.run(debug=True)
