from Models.files_model import File
from Utils.CommonExceptions import CommonException
import logging
from flask import request, jsonify

class FileController:
    def getAllFiles():
        try:
            files = File.objects()
            return jsonify([file.to_json() for file in files]), 200
        except Exception as e:
            logging.error(f"Error in getAllFiles: {str(e)}")
            return CommonException.handleException(e)

    def getFileById():
        try:
            file_id = request.args.get('id')
            if not file_id:
                return CommonException.IdRequiredException()
            file = File.objects(id=file_id).first()
            if not file:
                return jsonify({"message": "File not found"}), 404
            return jsonify(file.to_json()), 200
        except Exception as e:
            logging.error(f"Error in getFileById: {str(e)}")
            return CommonException.handleException(e)

    def createFile():
        try:
            data = request.get_json()
            if not data:
                return CommonException.DataRequiredException()
            file = File(**data)
            file.save()
            return jsonify({"message": "File created successfully", "file": file.to_json()}), 201
        except Exception as e:
            logging.error(f"Error in createFile: {str(e)}")
            return CommonException.handleException(e)

    def updateFile():
        try:
            file_id = request.args.get('id')
            if not file_id:
                return CommonException.IdRequiredException()
            data = request.get_json()
            if not data:
                return CommonException.DataRequiredException()
            file = File.objects(id=file_id).first()
            if not file:
                return jsonify({"message": "File not found"}), 404
            file.update(**data)
            return jsonify({"message": "File updated successfully"}), 200
        except Exception as e:
            logging.error(f"Error in updateFile: {str(e)}")
            return CommonException.handleException(e)

    def deleteFile():
        try:
            file_id = request.args.get('id')
            if not file_id:
                return CommonException.IdRequiredException()
            file = File.objects(id=file_id).first()
            if not file:
                return jsonify({"message": "File not found"}), 404
            file.delete()
            return jsonify({"message": "File deleted successfully"}), 200
        except Exception as e:
            logging.error(f"Error in deleteFile: {str(e)}")
            return CommonException.handleException(e)
