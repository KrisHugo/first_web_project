from .auth import register_auth_routes
from .messages import register_message_routes
from .errors import register_jwt_errors
from .user import register_userinfo_routes

def init_routes(app, jwt):
    register_auth_routes(app)
    register_message_routes(app)
    register_jwt_errors(jwt)
    register_userinfo_routes(app)