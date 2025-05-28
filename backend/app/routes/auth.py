from flask import request, jsonify
from flask_jwt_extended import create_access_token, jwt_required
from ..models.userModel import User
from ..extensions import db
from ..utils.validators import validate_registration


def register_auth_routes(app):
    @app.route('/api/register', methods=['POST'])
    def register():
        # 1. 获取请求数据
        data = request.get_json()
        
        # 2. 验证必填字段
        required_fields = ['username', 'password', 'email']
        if not all(field in data for field in required_fields):
            return jsonify({
                "error": "缺少必填字段",
                "required": required_fields
            }), 400

        # 3. 验证字段格式
        validation = validate_registration(data)
        errors = {}
        if validation.get('errors'):
            errors = validation['errors']
            return jsonify({
                "error": "验证失败",
                "details": errors
            }), 400
            
        # # 用户名验证 (4-20位字母数字)
        username = data['username'].strip()
        # # 邮箱验证
        email = data['email'].strip()
        password = data['password']
        if User.query.filter_by(username=username).first():
            return jsonify({
                "error": "用户名已存在"
            }), 409
            
        if User.query.filter_by(email=email).first():
            return jsonify({
                "error": "邮箱已被注册"
            }), 409

        try:
            # 5. 创建新用户
            new_user = User(
                username=username,
                email=email
            )
            new_user.set_password(password)  # 使用 bcrypt 加密密码
            new_user.created_at = db.func.now()  # 设置创建时间
            
            # 6. 保存到数据库
            db.session.add(new_user)
            db.session.commit()
            
            # 7. 返回成功响应
            return jsonify({
                "message": "注册成功",
                "user": {
                    "id": new_user.id,
                    "username": new_user.username,
                    "email": new_user.email
                }
            }), 201
            
        except Exception as e:
            # 8. 数据库错误处理
            db.session.rollback()
            app.logger.error(f"注册失败: {str(e)}")
            return jsonify({
                "error": "服务器内部错误",
                "message": "注册失败，请稍后重试"
            }), 500

    @app.route('/api/login', methods=['POST'])
    def login():
        data = request.json
        user = User.query.filter_by(username=data['username']).first()
        if not user or not user.check_password(data['password']):
            return jsonify({"error": "用户名或密码错误"}), 401
        
        token = create_access_token(identity=user.username)
        return jsonify({
            "token": token,
            "user": {
                "username": user.username
            }
        })

    @app.route("/api/protected", methods=["GET"])
    @jwt_required()
    def protected():
        return jsonify({"message": "已登录用户才能看到"})
