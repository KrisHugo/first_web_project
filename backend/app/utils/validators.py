def validate_registration(data):
    errors = {}
    required_fields = ['username', 'password', 'email']
    
    # 检查必填字段
    if not all(field in data for field in required_fields):
        return {'errors': {"general": "缺少必填字段"}}
    
    username = data['username'].strip()
    email = data['email'].strip()
    
    # 用户名验证
    if len(username) < 4 or len(username) > 20:
        errors['username'] = "用户名必须为4-20个字符"
    elif not username.isalnum():
        errors['username'] = "只能包含字母和数字"
    
    # 邮箱验证
    if '@' not in email or '.' not in email.split('@')[1]:
        errors['email'] = "无效的邮箱格式"
    
    # 密码验证
    password = data['password']
    if len(password) < 6:
        errors['password'] = "密码至少需要6个字符"
    
    return {'username': username, 'email': email, 'errors': errors}