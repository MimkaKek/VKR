from app.managers import UserManager
from flask import jsonify

def loginRequired():
    def decorator(func):
        def wrapper(*args, **kwargs):
            mgr = UserManager()
            loggedStatus = mgr.ValidateUser()
            if loggedStatus.status == False:
                return jsonify(loggedStatus.dump())
            
            callback = func(*args, **kwargs)
            return callback
        
        wrapper.__name__ = func.__name__
        return wrapper
    return decorator