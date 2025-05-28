from flask import jsonify
from flask_jwt_extended import JWTManager

def register_jwt_errors(jwt: JWTManager):
    @jwt.unauthorized_loader
    def handle_unauthorized_error(err):
        return jsonify({"error": "缺少访问令牌1"}), 401

    @jwt.invalid_token_loader
    def handle_invalid_token_error(err):
        return jsonify({"error": "无效令牌2"}), 401

    @jwt.expired_token_loader
    def handle_expired_token_error(jwt_header, jwt_payload):
        return jsonify({"error": "令牌已过期3"}), 401