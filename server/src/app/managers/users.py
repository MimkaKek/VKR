from app.models import UserModel
from app.common import Callback
from app.common.logging import logger
from app.managers import RepositoryManager
from app import db
from flask import request
import sys

class UserManager():

    def __init__(self) -> None:
        pass
    

    def _IsUsernameExist(self, username: str) -> bool:
        user = UserModel.query.filter_by(username=username).first()
        
        if user is None:
            return False
        return True

    def _IsEmailExist(self, email: str) -> bool:
        user = UserModel.query.filter_by(email=email).first()
        
        if user is None:
            return False
        return True

    def AddUser(self) -> Callback:
        
        logger.info("Call AddUser()...")
        
        if "user" not in request.json:
            logger.warn("'user' field doesn't exist!")
            return Callback(status=False)
        
        if "mail" not in request.json["user"] or "name" not in request.json["user"] or "pass" not in request.json["user"]:
            logger.warn("'user' field doesn't have some subfields!")
            return Callback(status=False)
        
        email    = request.json["user"]["mail"]
        username = request.json["user"]["name"]
        password = request.json["user"]["pass"]
        
        if self._IsEmailExist(email):
            logger.error("Email already exists...")
            return Callback(status=False)
        
        if self._IsUsernameExist(username):
            logger.error("Username already exists...")
            return Callback(status=False)

        manager = RepositoryManager()
        if not manager.RepUserCreate(username):
            logger.error("Create user repository for {name} failed".format(name=username))
            return Callback(status=False)
        
        u = UserModel(email, username, password)
        db.session.add(u)
        db.session.commit()
        
        logger.info("User registered...")

        return Callback()

    def RemoveUser(self) -> Callback:
        
        logger.info("Call RemoveUser()...")
        
        targetUser = request.json["user"]["name"]
        
        if not self._IsUsernameExist(targetUser):
            logger.warn("Username doesn't exist")
            return Callback(status=False)
        
        manager = RepositoryManager()
        if not manager.RepUserRemove(targetUser):
            logger.error("Remove user repository for {name} failed".format(name=targetUser))
            return Callback(status=False)
        
        user = UserModel.query.filter_by(username=targetUser).one()
        db.session.delete(user)
        db.session.commit()

        logger.info("User removed...")
        
        return Callback()

    def ListUsers(self) -> Callback:
        
        logger.info("Call ListUsers()...")
        manager = RepositoryManager()
        users = manager.RepUsersList()
        return Callback(data=users)

    def ValidateUser(self) -> Callback:
        
        logger.info("Call ValidateUser()...")
        
        if "user" not in request.json:
            logger.error("'user' field doesn't exist")
            return Callback(status=False)
        
        if "name" not in request.json["user"] or "mail" not in request.json["user"] or "pass" not in request.json["user"]:
            logger.error("'user' field doesn't have subfields")
            return Callback(status=False)
        
        name     = request.json["user"]["name"]
        email    = request.json["user"]["mail"]
        password = request.json["user"]["pass"]
        
        if name == None or email == None or password == None:
            logger.warn("Some of fields empty")
            return Callback(status=False)
        
        user = UserModel.query.filter_by(email=email, username=name).first()
        if user is None:
            logger.warn("User doesn't exists!")
            return Callback(status=False)
        else:
            logger.info("Checking password")
            return Callback(status=user.CheckPassword(password))