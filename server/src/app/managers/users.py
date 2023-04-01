from app.models import UserModel
from app.common import Callback, ProjectData
from app.common.logging import logger
from app.managers import RepositoryManager, ProjectManager
from app.cfg import ConfigInterface as cfg
from app import db

class UserManager():

    def __init__(self) -> None:
        pass
    
    def CreateAdmin(self) -> None:

        username = "admin"
        password = "admin"

        if self._IsUsernameExist(username):
            return
        
        self.AddUser(username, None, password)
        self.SetRole(username, cfg.ROLES.ADMIN)

        mgr = ProjectManager()
        meta = ProjectData("DEFAULT", "Default template", username, isTemplate=True)
        callback = mgr.CreateProject(username, meta)
        mgr.InitDefault(callback.data)

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
        
        logger.info("Call AddUser()...")
        
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
        
        u = UserModel(email, username, password, cfg.ROLES["STUDENT"])
        db.session.add(u)
        db.session.commit()
        
        logger.info("User registered...")

        return Callback()

    def RemoveUser(self, username: str) -> Callback:
        
        logger.debug("Call RemoveUser()...")
        
        if not self._IsUsernameExist(username):
            logger.warn("Username doesn't exist")
            return Callback(status=1, description="Username doesn't exist")
        
        manager = RepositoryManager()
        if not manager.RepUserRemove(username):
            logger.error("Remove user repository for {name} failed".format(name=username))
            return Callback(status=2, description="Remove user repository failed")
        
        user = UserModel.query.filter_by(username=username).one()
        db.session.delete(user)
        db.session.commit()

        logger.info("User {user} removed...".format(user=username))
        return Callback()

    def ListUsers(self) -> Callback:
        
        logger.info("Call ListUsers()...")
        manager = RepositoryManager()
        users = manager.RepUsersList()
        return Callback(data=users)

    def ValidateUser(self, name: str, email: str, password: str) -> Callback:
        
        logger.info("Call ValidateUser()...")
        
        callback = self.GetUser(name, email)
        if callback.status != 0:
            return callback
        user = callback.data
        
        logger.info("Checking password")
        if user.CheckPassword(password):
            return Callback(data=user.role)
        return Callback(status=2, description="Wrong password!")
    
    def GetUser(self, name: str, email: str) -> Callback:

        logger.info("Call GetUser()...")

        user = UserModel.query.filter_by(username=name).first()
        if user is None:
            logger.warn("Can't find user by username = {username}!".format(username=name))
            user = UserModel.query.filter_by(email=email).first()
            if user is None:
                logger.warn("User doesn't exists!")
                return Callback(status=1, description="User doesn't exists!")
            
        return Callback(data=user)

    def SetRole(self, name: str, newRole: str) -> Callback:

        logger.info("Call SetRole()...")

        callback = self.GetUser(name, None)
        if callback.status != 0:
            return callback
        user = callback.data

        try:
            user.role = newRole
            db.session.commit()
        except Exception as e:
            logger.error("Error while update user role!")
            logger.exception(e)
            return Callback(status=1, description="Setting role failed")

        logger.info("End SetRole()...")
        return Callback()