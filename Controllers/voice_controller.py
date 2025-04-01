from flask import request, jsonify, send_file
import speech_recognition as sr
import openai
from gtts import gTTS
import os
import logging
from Utils.CommonExceptions import CommonException

openai_client = openai.OpenAI(api_key=os.getenv('OPENAI_API_KEY'))

class VoiceAssistantController:
    @staticmethod
    def recognize_speech(audio_file_path):
        recognizer = sr.Recognizer()
        with sr.AudioFile(audio_file_path) as source:
            audio = recognizer.record(source)
        try:
            return recognizer.recognize_google(audio)
        except sr.UnknownValueError:
            return "I couldn't understand that."
        except sr.RequestError:
            return "Could not request results. Check your internet connection."

    @staticmethod
    def get_ai_response(prompt):
        response = openai_client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You are a helpful AI assistant."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=40,
            temperature=0.7
        )
        return response.choices[0].message.content.strip()

    @staticmethod
    def generate_audio(text):
        """Generates an MP3 file from text and returns the filename."""
        filename = "response.mp3"
        tts = gTTS(text=text, lang='en')
        tts.save(filename)
        return filename

    @staticmethod
    def recognize():
        try:
            if 'file' not in request.files:
                return jsonify({"error": "No file uploaded"}), 400

            file = request.files['file']
            temp_file_path = "temp.wav"
            file.save(temp_file_path)

            recognized_text = VoiceAssistantController.recognize_speech(temp_file_path)
            ai_response = VoiceAssistantController.get_ai_response(recognized_text)
            audio_filename = VoiceAssistantController.generate_audio(ai_response)

            return send_file(audio_filename, mimetype="audio/mp3", as_attachment=True)
        except Exception as e:
            logging.error(f"Error in recognize: {str(e)}")
            return CommonException.handleException(e)

    @staticmethod
    def get_response():
        try:
            data = request.get_json()
            user_text = data.get("text", "")
            if not user_text:
                return jsonify({"error": "No text provided"}), 400

            ai_response = VoiceAssistantController.get_ai_response(user_text)
            logging.info(f"AI Response: {ai_response}")

            if not ai_response.strip():
                return jsonify({"error": "Received empty response from AI"}), 500

            audio_filename = VoiceAssistantController.generate_audio(ai_response)
            return send_file(audio_filename, mimetype="audio/mp3", as_attachment=True)
        except Exception as e:
            logging.error(f"Error in get_response: {str(e)}")
            return CommonException.handleException(e)
