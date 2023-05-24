from app.models import UserModel
from app.common import Callback, ProjectData
from app.common.logging import logger
from app.managers import RepositoryManager, ProjectManager
from app.cfg import ConfigInterface as cfg
from app import db

import uuid
class UserManager():

    def __init__(self) -> None:
        pass
    
    def CreateAdmin(self) -> None:

        username = "admin"
        password = "admin"

        if self._IsUsernameExist(username):
            return
        
        self.AddUser(username, None, password)

        user = self.GetUser(username).data
        self.SetRole(user, cfg.ROLES.ADMIN)

        mgr = ProjectManager()
        mgr.CreatePresets(username)

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

    def AddUser(self, username: str, email: str, password: str) -> Callback:
        
        if self._IsEmailExist(email):
            logger.error("Email already exists...")
            return Callback(status=1, description="Email already exists")
        
        if self._IsUsernameExist(username):
            logger.error("Username already exists...")
            return Callback(status=2, description="Username already exists")

        manager = RepositoryManager()
        if not manager.RepUserCreate(username):
            logger.error("Create user repository for {name} failed".format(name=username))
            return Callback(status=3, description="Create user repository failed")
        
        sid = uuid.uuid4().hex
        u = UserModel(email, username, password, cfg.ROLES.STUDENT, sid)
        db.session.add(u)
        db.session.commit()
        
        logger.info("User {username} registered...".format(username=username))
        return Callback(data={"sid": sid, "role": 3})

    def RemoveUser(self, user: UserModel) -> Callback:
        db.session.delete(user)
        db.session.commit()
        logger.info("User {user} removed...".format(user=user.username))
        return Callback()

    def ListUsers(self) -> Callback:
        manager = RepositoryManager()
        usersList = manager.RepUsersList()
        usersDict = dict()

        for user in usersList:
            callback = self.GetUser(user, "")
            role     = callback.data.role
            usersDict.update({user: role})

        return Callback(data=usersDict)

    def ValidateUser(self, user: UserModel, password: str) -> Callback:
        if user.CheckPassword(password):
            return Callback()
        return Callback(status=1, description="Wrong password!")
    
    def GetUser(self, username: str = None, email: str = None, sid: str = None) -> Callback:
        if username is not None:
            user = UserModel.query.filter_by(username=username).first()
            if user is not None:
                return Callback(data=user)
        if email is not None:
            user = UserModel.query.filter_by(email=email).first()
            if user is not None:
                return Callback(data=user)
            
        if sid is not None:
            user = UserModel.query.filter_by(sid=sid).first()
            if user is not None:
                return Callback(data=user)
        return Callback(status=1, description="User doesn't exists!")
            
    def CreateSID(self, user: UserModel) -> Callback:
        try:
            user.sid = uuid.uuid4().hex
            db.session.commit()
        except Exception as e:
            logger.error("Error while update user sid!")
            logger.exception(e)
            return Callback(status=1, description="Generating SID failed!")
        return Callback()

    def SetRole(self, user: UserModel, newRole: str) -> Callback:
        try:
            user.role = newRole
            db.session.commit()
        except Exception as e:
            logger.error("Error while update user role!")
            logger.exception(e)
            return Callback(status=1, description="Setting role failed!")
        return Callback()
    
    def GetRole(self, user: UserModel) -> Callback:
        try:
            callback = Callback(data=user.role)
        except Exception as e:
            logger.error("Get role failed!")
            logger.exception(e)
            return Callback(status=1, description="Get role failed!")
        return callback