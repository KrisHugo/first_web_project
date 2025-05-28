from flask import request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from ..models.userModel import User
from ..models.messageModel import Message
from ..extensions import db


def register_message_routes(app):
    @app.route('/api/messages', methods=['GET', 'POST'])
    @jwt_required()
    def handle_messages():
        current_user = get_jwt_identity()
        user = User.query.filter_by(username=current_user).first()


        if request.method == 'POST':
            data = request.get_json()
            message = Message(content=data['content'], user_id=user.id)
            db.session.add(message)
            db.session.commit()
            return jsonify({"message":"发送成功"}), 201
        
        elif request.method == 'GET':
            messages = Message.query.join(User).order_by(Message.created_at.desc()).all()
            return jsonify([{
                'id': msg.id,
                'content': msg.content,
                'created_at': msg.created_at.isoformat(),
                'user': {
                    'username': msg.user.username,
                    'avatar': msg.user.avatar or '/icons/default-avatar.svg'
                }
            } for msg in messages])
        
    @app.route('/api/messages/<int:message_id>', methods=['DELETE'])
    @jwt_required()
    def delete_message(message_id):
        current_user = get_jwt_identity()
        message = Message.query.get_or_404(message_id)
        
        if message.user.username != current_user:
            return jsonify({"error": "无权删除此留言"}), 403
            
        db.session.delete(message)
        db.session.commit()
        return jsonify({"success": True})