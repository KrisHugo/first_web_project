from flask import Flask, request, jsonify
from flask_cors import CORS  # 解决跨域问题
import pymysql  # 改用 pymysql（更通用）
from flask_jwt_extended import JWTManager, create_access_token, jwt_required

app = Flask(__name__)
CORS(app)  # 允许所有域名跨域访问（生产环境需限制）

# MySQL 配置
db_config = {
    "host": "localhost",
    "user": "root",
    "password": "123456",
    "database": "test_db",
    "cursorclass": pymysql.cursors.DictCursor  # 返回字典格式数据
}

app.config["JWT_SECRET_KEY"] = "your-secret-key"  # 替换为随机字符串
jwt = JWTManager(app)


# 用户模型
users = {"admin": {"password": "123456"}}  # 临时模拟用户数据

@app.route("/api/login", methods=["POST"])
def login():
    username = request.json.get("username")
    password = request.json.get("password")
    if users.get(username) and users[username]["password"] == password:
        token = create_access_token(identity=username)
        return jsonify({"token": token})
    return jsonify({"error": "用户名或密码错误"}), 401

@app.route("/api/protected", methods=["GET"])
@jwt_required()
def protected():
    return jsonify({"message": "已登录用户才能看到"})


@app.route('/api/messages', methods=['GET', 'POST'])
def handle_messages():
    if request.method == 'POST':
        # 接收 Vue 前端发来的数据
        data = request.get_json()
        content = data['content']
        
        # 存入数据库
        connection = pymysql.connect(**db_config)
        try:
            with connection.cursor() as cursor:
                sql = "INSERT INTO messages (content) VALUES (%s)"
                cursor.execute(sql, (content,))
                connection.commit()
        finally:
            connection.close()
        
        return jsonify({"status": "success"})
    
    elif request.method == 'GET':
        # 从数据库读取留言
        connection = pymysql.connect(**db_config)
        try:
            with connection.cursor() as cursor:
                sql = "SELECT * FROM messages ORDER BY created_at DESC"
                cursor.execute(sql)
                messages = cursor.fetchall()
                return jsonify(messages)
        finally:
            connection.close()

if __name__ == '__main__':
    app.run(debug=True, port=5000)  # 后端运行在 5000 端口