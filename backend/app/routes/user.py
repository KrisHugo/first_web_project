# -*- coding: utf-8 -*-
import time
from flask import jsonify, request
from flask_jwt_extended import get_jwt_identity, jwt_required

from ..models.userModel import User
from ..extensions import db

# from werkzeug.utils import secure_filename

from flask import send_from_directory
from flask import current_app
def register_userinfo_routes(app):

    @app.route('/upload-avatar', methods=['POST'])
    @jwt_required()
    def upload_avatar():
        if 'file' not in request.files:
            return {'error': 'No file uploaded'}, 400
        
        file = request.files['file']
        if file.filename == '':
            return {'error': 'Empty filename'}, 400
        
        if file and allowed_file(file.filename):
            # 生成唯一文件名
            filename = f"{get_jwt_identity()}_{int(time.time())}.{file.filename.rsplit('.', 1)[1].lower()}"
            save_path = current_app.config['UPLOAD_FOLDER'] / filename
            
            file.save(save_path)
            
            # 更新用户头像URL（相对路径）
            user = User.query.filter_by(username=get_jwt_identity()).first()
            user.avatar = f'/uploads/avatars/{filename}'
            db.session.commit()
            
            return {'url': user.avatar}, 200
        
        return {'error': 'Invalid file type'}, 400

    @app.route('/uploads/avatars/<filename>')
    def serve_avatar(filename):
        return send_from_directory(current_app.config['UPLOAD_FOLDER'], filename)
    
    @app.route('/info', methods=['GET'])
    @jwt_required()
    def get_user_info():
        current_user = get_jwt_identity()
        # 从数据库获取用户信息
        return jsonify({"username": current_user}), 200
    
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in current_app.config['ALLOWED_EXTENSIONS']

