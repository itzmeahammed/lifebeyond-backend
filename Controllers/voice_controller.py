from flask import request, jsonify, current_app
import speech_recognition as sr
import openai
from gtts import gTTS
import os
import logging
from Utils.CommonExceptions import CommonException
from pydub import AudioSegment
from pydub.playback import play

AudioSegment.converter = "/usr/bin/ffmpeg" 
AudioSegment.ffprobe = "/usr/bin/ffprobe"
openai_client = openai.OpenAI(api_key=os.getenv('OPENAI_API_KEY'))

class VoiceAssistantController:
    @staticmethod
    def recognize_speech(audio_file_path):
        recognizer = sr.Recognizer()
        with sr.AudioFile(audio_file_path) as source:
            audio = recognizer.record(source)
        try:
            text = recognizer.recognize_google(audio)
            return text
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
    def speak_text(text):
        tts = gTTS(text=text, lang='en')
        filename = "response.mp3"
        tts.save(filename)
        
        sound = AudioSegment.from_mp3(filename)
        sound.export("response.wav", format="wav")
        play(AudioSegment.from_wav("response.wav"))

    @staticmethod
    def recognize():
        try:
            if 'file' not in request.files:
                return jsonify({"error": "No file uploaded"}), 400

            file = request.files['file']
            temp_file_path = os.path.join(os.getcwd(), "temp.wav")
            file.save(temp_file_path)

            recognized_text = VoiceAssistantController.recognize_speech(temp_file_path)
            ai_response = VoiceAssistantController.get_ai_response(recognized_text)
            VoiceAssistantController.speak_text(ai_response)
            return jsonify({"Response":ai_response}),200
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

            VoiceAssistantController.speak_text(ai_response)
            return jsonify({"Response":ai_response}),200
        except Exception as e:
            logging.error(f"Error in get_response: {str(e)}")
            return CommonException.handleException(e)
