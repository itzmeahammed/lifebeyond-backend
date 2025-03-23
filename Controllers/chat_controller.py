from Models.chat_model import Chat, Message
from Models.user_model import User
from Utils.CommonExceptions import CommonException
import logging
from flask import request, jsonify

class ChatController:
    def getAllChats():
        try:
            chats = Chat.objects()
            return jsonify([chat.to_json() for chat in chats]), 200
        except Exception as e:
            logging.error(f"Error in getAllChats: {str(e)}")
            return CommonException.handleException(e)

    def getChatsByUser():
        try:
            token = request.headers.get('Authorization')
            if not token:
                return jsonify({"Error": "Unauthorized"}), 401
            user = User.objects(auth_token=token).first()
            if not user:
                return jsonify({"Error": "User not found"}), 404
            chats = Chat.objects(person1=user.id)
            chats2 = Chat.objects(person2=user.id)
            total_chats = [chat.to_json() for chat in chats]
            [total_chats.append(chat.to_json()) for chat in chats2]
            return jsonify(total_chats), 200
        except Exception as e:
            logging.error(f"Error in getChatsByUser: {str(e)}")
            return CommonException.handleException(e)

    def createChat():
        try:
            token = request.headers.get('Authorization')
            user = User.objects(auth_token=token).first()
            data = request.get_json()
            if not data:
                return CommonException.DataRequiredException()
            person2= data.pop('person2')
            message = Message(**data)
            chat = Chat(person1=user.id,person2=person2,messages=[message])
            chat.save()
            return jsonify({"message": "Chat created successfully", "chat": chat.to_json()}), 201
        except Exception as e:
            logging.error(f"Error in createChat: {str(e)}")
            return CommonException.handleException(e)

    def addMessage():
        try:
            chat_id = request.args.get('chat_id')
            if not chat_id:
                return CommonException.IdRequiredException()
            data = request.get_json()
            if not data:
                return CommonException.DataRequiredException()
            chat = Chat.objects(id=chat_id).first()
            if not chat:
                return jsonify({"message": "Chat not found"}), 404
            message = Message(**data)
            chat.messages.append(message)
            chat.save()
            return jsonify({"message": "Message added successfully", "chat": chat.to_json()}), 200
        except Exception as e:
            logging.error(f"Error in addMessage: {str(e)}")
            return CommonException.handleException(e)

    def deleteChat():
        try:
            chat_id = request.args.get('chat_id')
            if not chat_id:
                return CommonException.IdRequiredException()
            chat = Chat.objects(id=chat_id).first()
            if not chat:
                return jsonify({"message": "Chat not found"}), 404
            chat.delete()
            return jsonify({"message": "Chat deleted successfully"}), 200
        except Exception as e:
            logging.error(f"Error in deleteChat: {str(e)}")
            return CommonException.handleException(e)

    def deleteLastMessage():
        try:
            chat_id = request.args.get('chat_id')
            if not chat_id:
                return CommonException.IdRequiredException()
            chat = Chat.objects(id=chat_id).first()
            if not chat or not chat.messages:
                return jsonify({"message": "Chat or messages not found"}), 404
            chat.messages.pop()
            chat.save()
            return jsonify({"message": "Last message deleted successfully", "chat": chat.to_json()}), 200
        except Exception as e:
            logging.error(f"Error in deleteLastMessage: {str(e)}")
            return CommonException.handleException(e)

    def updateLastMessage():
        try:
            chat_id = request.args.get('chat_id')
            if not chat_id:
                return CommonException.IdRequiredException()
            data = request.get_json()
            if not data or "text" not in data:
                return CommonException.DataRequiredException()
            chat = Chat.objects(id=chat_id).first()
            if not chat or not chat.messages:
                return jsonify({"message": "Chat or messages not found"}), 404
            chat.messages[-1].text = data["text"]
            chat.save()
            return jsonify({"message": "Last message updated successfully", "chat": chat.to_json()}), 200
        except Exception as e:
            logging.error(f"Error in updateLastMessage: {str(e)}")
            return CommonException.handleException(e)
