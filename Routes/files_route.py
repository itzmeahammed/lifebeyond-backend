from Controllers.files_controller import FileController
from flask import Blueprint

file_bp = Blueprint('File', __name__)

file_bp.add_url_rule('/getAllFiles', view_func=FileController.getAllFiles, methods=['GET'])
file_bp.add_url_rule('/getFileById', view_func=FileController.getFileById, methods=['GET'])
file_bp.add_url_rule('/createFile', view_func=FileController.createFile, methods=['POST'])
file_bp.add_url_rule('/updateFile', view_func=FileController.updateFile, methods=['PUT'])
file_bp.add_url_rule('/deleteFile', view_func=FileController.deleteFile, methods=['DELETE'])
