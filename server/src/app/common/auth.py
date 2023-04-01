from app.managers import UserManager
from app.common import Callback
from app.cfg import ConfigInterface as cfg
from app.common.logging import logger
from flask import jsonify, request

def loginRequired(requiredRole = cfg.ROLES.STUDENT):
    def decorator(func):
        def wrapper(*args, **kwargs):
            
            if "user" not in request.json:
                logger.error("'user' field doesn't exist")
                return jsonify(Callback(status=1, description="'user' field doesn't exist").dict())
            
            if "name" not in request.json["user"] or "mail" not in request.json["user"] or "pass" not in request.json["user"]:
                logger.error("'user' field doesn't have subfields")
                return jsonify(Callback(status=2, description="'user' field doesn't have subfields").dict())
            
            username = request.json["user"]["name"]
            email    = request.json["user"]["mail"]
            password = request.json["user"]["pass"]

            mgr = UserManager()
            loggedStatus = mgr.ValidateUser(username, email, password)
            if loggedStatus.status != 0:
                return jsonify(loggedStatus.dict())

            if loggedStatus.data > requiredRole:
                loggedStatus.data        = None
                loggedStatus.status      = 2
                loggedStatus.description = "Role required!"
                return jsonify(loggedStatus.dict())

            callback = func(*args, **kwargs)
            return callback
        
        wrapper.__name__ = func.__name__
        return wrapper
    return decorator