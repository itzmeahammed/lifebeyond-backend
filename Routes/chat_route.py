from Controllers.chat_controller import ChatController
from flask import Blueprint

chat_bp = Blueprint('Chat', __name__)

chat_bp.add_url_rule('/getAllChats', view_func=ChatController.getAllChats, methods=['GET'])
chat_bp.add_url_rule('/getChatsByUser', view_func=ChatController.getChatsByUser, methods=['GET'])
chat_bp.add_url_rule('/createChat', view_func=ChatController.createChat, methods=['POST'])
chat_bp.add_url_rule('/addMessage', view_func=ChatController.addMessage, methods=['POST'])
chat_bp.add_url_rule('/deleteChat', view_func=ChatController.deleteChat, methods=['DELETE'])
chat_bp.add_url_rule('/deleteLastMessage', view_func=ChatController.deleteLastMessage, methods=['DELETE'])
chat_bp.add_url_rule('/updateLastMessage', view_func=ChatController.updateLastMessage, methods=['PUT'])
