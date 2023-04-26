from app.managers import UserManager
from app.common import Callback
from app.cfg import ConfigInterface as cfg
from app.common.logging import logger
from flask import jsonify, request

def loginRequired(requiredRole = cfg.ROLES.STUDENT):
    def decorator(func):
        def wrapper(*args, **kwargs):
            
            sid = request.args.get('sid', "")

            mgr = UserManager()
            userStatus = mgr.GetUser(sid=sid)
            if userStatus.status != 0:
                return jsonify(userStatus.dict())
            user = userStatus.data

            role = user.role
            if role > requiredRole:
                logStatus = Callback(status=2, description="Role required!")
                return jsonify(logStatus.dict())

            callback = func(*args, **kwargs)
            return callback
        
        wrapper.__name__ = func.__name__
        return wrapper
    return decorator