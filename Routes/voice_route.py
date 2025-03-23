from flask import Blueprint
from Controllers.voice_controller import VoiceAssistantController

voice_assistant_bp = Blueprint('VoiceAssistant', __name__)

voice_assistant_bp.add_url_rule('/recognize', view_func=VoiceAssistantController.recognize, methods=['POST'])
voice_assistant_bp.add_url_rule('/get-response', view_func=VoiceAssistantController.get_response, methods=['POST'])
