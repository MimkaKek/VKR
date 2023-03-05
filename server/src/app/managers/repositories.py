import os
import shutil
import uuid
from datetime import datetime

from app import db
from app.cfg import ConfigInterface
from app.models import TemplateModel, SessionModel
from app.common import UserData, SessionData, TemplateData
from app.common.logging import logger

class RepositoryManager():

    #=============================== COMMON ========================================
    
    def __init__(self) -> None:
        pass
    
    def RepositoryCopy(self, dstPath: str, srcPath: str) -> bool:
        logger.info("Call CopyRepository()...")
        logger.info("Copy from {src} to {dst}".format(src=srcPath, dst=dstPath))
        
        if not os.path.exists(srcPath):
            logger.error("Src rep doesn't exist")
            return False
        
        if not os.path.exists(dstPath):
            os.makedirs(dstPath)
        
        for item in os.listdir(srcPath):
            s = os.path.join(srcPath, item)
            d = os.path.join(dstPath, item)
            if os.path.isdir(s):
                shutil.copytree(s, d)
            else:
                shutil.copy2(s, d)
                
        return True
    
    def Init(self) -> None:
        
        if not os.path.exists(ConfigInterface.GL_SESSION_PATH):
            os.makedirs(ConfigInterface.GL_SESSION_PATH)
            
        if not os.path.exists(ConfigInterface.GL_TEMPLATE_PATH):
            os.makedirs(ConfigInterface.GL_TEMPLATE_PATH)
            
        if not os.path.exists(ConfigInterface.GL_USERS_PATH):
            os.makedirs(ConfigInterface.GL_USERS_PATH)
    
    # ==================================== USER =======================================
    
    def RepUserCreate(self, username: str) -> bool:
        logger.info("Call CreateUserRep()...")
        usrPath = os.path.join(ConfigInterface.GL_USERS_PATH, username)
        
        os.makedirs(usrPath)
        
        for dir in ConfigInterface.USER_REPOS:
            contentPath = os.path.join(usrPath, ConfigInterface.USER_REPOS[dir])
            os.makedirs(contentPath)
        
        usrDataPath = os.path.join(usrPath, ConfigInterface.USER_DATA)
        usrData     = UserData()
        usrData.registered = datetime.now().strftime('%Y.%m.%d')
        
        with open(usrDataPath, "w") as file:
            file.write(usrData.dump())
        
        templatesPath = os.path.join(usrPath, ConfigInterface.USER_REPOS["t_repo"])
        
        presetsList = os.listdir(ConfigInterface.PRESETS_PATH)
        for preset in presetsList:
            os.symlink(os.path.join(ConfigInterface.PRESETS_PATH, preset), os.path.join(templatesPath, preset))
        
        logger.info("User repo created")
        
        return True
    
    def RepUserRemove(self, username: str) -> bool:
        logger.info("Call RemoveUserRep()...")
        usrPath = os.path.join(ConfigInterface.GL_USERS_PATH, username)
        
        if not os.path.exists(usrPath):
            logger.error("User already removed")
            return False
        
        sList = os.listdir(os.path.join(usrPath, ConfigInterface.USER_REPOS["s_repo"]))
        sData = SessionData()
        
        for sid in sList:
            sDataFile = os.path.join(usrPath, ConfigInterface.USER_REPOS["s_repo"], sid, ConfigInterface.SESSION_DATA)
            with open(sDataFile, "r") as file:
                sData.load(file.read())
                
            if sData.owner == username:
                self.ProjectRemove(username, sid)
                
        tList = os.listdir(os.path.join(usrPath, ConfigInterface.USER_REPOS["t_repo"]))
        tData = TemplateData()
        
        for tid in tList:
            tDataFile = os.path.join(usrPath, ConfigInterface.USER_REPOS["t_repo"], tid, ConfigInterface.TEMPLATE_DATA)
            with open(tDataFile, "r") as file:
                tData.load(file.read())
                
            if tData.owner == username:
                self.RemoveTemplateRep(username, tid)
                
        shutil.rmtree(usrPath)
        
        return True
    
    def RepUserExist(self, username: str) -> bool:
        uList = os.listdir(ConfigInterface.GL_USERS_PATH)
        return username in uList
    
    def RepUsersList(self) -> list:
        return os.listdir(ConfigInterface.GL_USERS_PATH)
        
    #======================================= PROJECT ===============================================
    
    def ProjectCreate(self, username: str, sid: str, repName: str, template: str = "DEFAULT_PRESET") -> bool:
        
        logger.info("Call CreateSessionRep()...")
        
        link = uuid.uuid4().hex
        s = SessionModel(sid, link)
        db.session.add(s)
        db.session.commit()
        
        usrPath = os.path.join(ConfigInterface.GL_USERS_PATH, username)
        glSessionPath = os.path.join(ConfigInterface.GL_SESSION_PATH, sid)
        lSessionPath  = os.path.join(usrPath, ConfigInterface.USER_REPOS["s_repo"], sid)
        
        os.makedirs(glSessionPath)
        os.symlink(glSessionPath, lSessionPath)
        
        logger.info("Symlink for {sid} of {user} from {link} created".format(sid=sid, user=username, link=lSessionPath))

        sData             = SessionData()
        sData.owner       = username
        sData.name        = repName
        sData.created     = datetime.now().strftime('%Y.%m.%d')
        sData.lastUpdated = datetime.now().strftime('%Y.%m.%d')
        
        self.ProjectSetData(sid, sData)
        
        if template == None:
            logger.info("Repository created")
            return True
            
        lSessionSrcPath = os.path.join(lSessionPath, ConfigInterface.SESSION_REPOS["src"])
        templateSrcPath = os.path.join(ConfigInterface.GL_USERS_PATH, username, ConfigInterface.USER_REPOS["t_repo"], template, ConfigInterface.TEMPLATE_REPOS["src"])
        
        if not os.path.exists(templateSrcPath):
            logger.error("Template src path {path} doesn't exists".format(path=templateSrcPath))
            os.unlink(lSessionPath)
            os.rmdir(glSessionPath)
            return False
        
        self.RepositoryCopy(lSessionSrcPath, templateSrcPath)

        logger.info("Repository created")
        
        return True
        
    def ProjectRemove(self, username: str, sid: str) -> bool:
        
        logger.info("Call RemoveSessionRep()...")
        
        s = SessionModel.query.filter_by(sid=sid).one()
        if s == None:
            logger.error("Session {sid} doesn't exists".format(sid=sid))
            return False
        
        db.session.delete(s)
        db.session.commit()
        
        usrPath       = os.path.join(ConfigInterface.GL_USERS_PATH, username)
        glSessionPath = os.path.join(ConfigInterface.GL_SESSION_PATH, sid)
        lSessionPath  = os.path.join(usrPath, ConfigInterface.USER_REPOS["s_repo"], sid)
        
        sDataFile = os.path.join(lSessionPath, ConfigInterface.SESSION_DATA)
        
        data = SessionData()
        
        with open(sDataFile, "r") as file:
            data.load(file.read())
        
        for user in data.permitedUsers:
            pUsrPath = os.path.join(ConfigInterface.GL_USERS_PATH, user, ConfigInterface.USER_REPOS["s_repo"], sid)
            os.unlink(pUsrPath)
            
        os.unlink(lSessionPath)
        shutil.rmtree(glSessionPath)
        logger.info("Session {sid} of {user} removed".format(sid=sid, user=username))
        return True
    
    def ProjectCopy(self, username: str, sid: str, newSID: str) -> bool:
        logger.info("Call CopySession()...")
        
        sData = self.ProjectGetData(sid)
        sData.name += " (copy)"
        
        if not self.ProjectCreate(username, newSID, sData.name, None):
            return False
        
        srcPath = os.path.join(ConfigInterface.GL_SESSION_PATH, sid, ConfigInterface.SESSION_REPOS["src"])
        dstPath = os.path.join(ConfigInterface.GL_SESSION_PATH, newSID, ConfigInterface.SESSION_REPOS["src"])
        
        if not self.RepositoryCopy(dstPath, srcPath):
            return False
        
        logger.info("Session {sid} copied to {newsid} for user {user}".format(sid=sid, newsid=newSID, user=username))
        return True
        
    
    def ProjectsGetAll(self) -> dict:
        logger.info("Call GetAllSessions()...")

        result = {}
        
        sessions = os.listdir(ConfigInterface.GL_SESSION_PATH)
        for sid in sessions:
            sData = self.ProjectGetData(sid)
            result.update({sid: {"name": sData.name, "owner": sData.owner, "created": sData.created}})
        
        logger.info("List of all sessions getted")
        
        return result
    
    def ProjectsGetByUser(self, username: str) -> dict:
        logger.info("Call GetUserSessions()...")

        result = {}
        
        sPath = os.path.join(ConfigInterface.GL_USERS_PATH, username, ConfigInterface.USER_REPOS["s_repo"])
        
        sessions = os.listdir(sPath)
        for sid in sessions:
            sData = self.ProjectGetData(sid)
            result.update({sid: {"name": sData.name, "created": sData.created, "last_updated": sData.lastUpdated}})
        
        logger.info("List of all sessions getted")
        
        return result
    
    def IsUserProject(self, username: str, sid: str) -> bool:
        logger.info("Call IsUserSession()...")
        sPath = os.path.join(ConfigInterface.GL_USERS_PATH, username, ConfigInterface.USER_REPOS["s_repo"])
        sessions = os.listdir(sPath)        
        return sid in sessions
        
    def ProjectGetSrc(self, sid: str) -> dict:
        logger.info("Call GetSessionSrc()...")
        result = {}
        srcPath = os.path.join(ConfigInterface.GL_SESSION_PATH, sid, ConfigInterface.SESSION_REPOS["src"])
        
        for filename in os.listdir(srcPath):
            filePath = os.path.join(srcPath, filename)
            if os.path.isfile(filePath):
                with open(filePath, "r") as file:
                    result[filename] = file.read()
                    
        logger.info("Src of session {sid} getted".format(sid=sid))
                    
        return result
    
    def ProjectGetFile(self, sid: str, filename: str) -> (str | None):
        logger.info("Call ProjectGetFile()...")
        result = None
        filePath = os.path.join(ConfigInterface.GL_SESSION_PATH, sid, ConfigInterface.SESSION_REPOS["src"], filename)
        
        if os.path.isfile(filePath):
            with open(filePath, "r") as file:
                result = file.read()
                    
        logger.info("File {filename} of session {sid} getted".format(filename=filename, sid=sid))
                    
        return result
    
    def ProjectSetFile(self, sid: str, filename: str, data: str) -> bool:
        logger.info("Call ProjectGetFile()...")
        filePath = os.path.join(ConfigInterface.GL_SESSION_PATH, sid, ConfigInterface.SESSION_REPOS["src"], filename)
        with open(filePath, "w") as file:
            file.write(data)
        logger.info("File {filename} of session {sid} setted".format(filename=filename, sid=sid))
        return True
    
    def ProjectRemoveFile(self, sid: str, filename: str) -> bool:
        logger.info("Call ProjectRemoveFile()...")
        filePath = os.path.join(ConfigInterface.GL_SESSION_PATH, sid, ConfigInterface.SESSION_REPOS["src"], filename)
        if os.path.exists(filePath):
            os.remove(filePath)   
        logger.info("File {filename} of session {sid} removed".format(filename=filename, sid=sid))
        return True
    
    def ProjectCreateFile(self, sid: str, filename: str) -> bool:
        logger.info("Call ProjectCreateFile()...")
        filePath = os.path.join(ConfigInterface.GL_SESSION_PATH, sid, ConfigInterface.SESSION_REPOS["src"], filename)
        if not os.path.exists(filePath):
            with open(filePath, "w") as f:
                pass
        logger.info("File {filename} of session {sid} created".format(filename=filename, sid=sid))
        return True
    
    def ProjectSetSrc(self, sid: str, sessionSrc: dict) -> bool:
        
        logger.info("Call SetSessionSrc()...")
        
        srcPath = os.path.join(ConfigInterface.GL_SESSION_PATH, sid, ConfigInterface.SESSION_REPOS["src"])
        
        if not os.path.exists(srcPath):
            os.makedirs(srcPath)
        
        for filename in sessionSrc:
            filePath = os.path.join(srcPath, filename)
            if sessionSrc[filename]["action"] == "DEL":
                if os.path.exists(filePath):
                    os.remove(filePath)
            else:
                with open(filePath, "w") as file:
                    file.write(sessionSrc[filename]["src"])
        
        logger.info("Src of session {sid} updated".format(sid=sid))
        
        return True
    
    def ProjectSetData(self, sid: str, sData: SessionData) -> bool:
        
        logger.info("Call SetSessionData()...")
        
        sDataPath = os.path.join(ConfigInterface.GL_SESSION_PATH, sid, ConfigInterface.SESSION_DATA)
            
        with open(sDataPath, "w") as file:
            file.write(sData.dump())
            
        logger.info("Session data for {sid} updated".format(sid=sid))
            
        return True
    
    def ProjectGetData(self, sid: str) -> SessionData:
        logger.info("Call GetSessionData()... global")
        
        result   = SessionData()
        dataPath = os.path.join(ConfigInterface.GL_SESSION_PATH, sid, ConfigInterface.SESSION_DATA)
        
        with open(dataPath, "r") as file:
            result.load(file.read())
        
        logger.info("Session data get")
        
        return result
    
    def ProjectGetPage(self, sid: str, filename: str) -> str:
        
        logger.info("Call ProjectGetPage()...")
        result = ""
        pagePath = os.path.join(ConfigInterface.GL_SESSION_PATH, sid, ConfigInterface.SESSION_REPOS["src"], filename)
        
        if not os.path.exists(pagePath):
            logger.error("File {filename} in {sid} doesn't exists".format(sid=sid, filename=filename))
            return ""
        
        with open(pagePath, "r") as file:
            result = file.read()
            
        return result
    
    def ProjectShare(self, sid: str) -> str:
        
        logger.info("Call ShareSession()...")
        
        sData = self.ProjectGetData(sid)
        sData.link = uuid.uuid4().hex
        
        session = SessionModel.query.filter_by(sid=sid).first()
        if session == None:
            logger.error("Session doesn't exists")
            return None
        
        session.reflink = sData.link
        db.session.commit()
        
        if not self.ProjectSetData(sid, sData):
            logger.error("Creation of new share link failed")
            return None

        logger.info("New share link {link}".format(link=sData.link))
        return sData.link
    
    def ProjectUseShareLink(self, username: str, link: str) -> bool:
        
        logger.info("Call UseSessionShareLink()...")
        
        session = SessionModel.query.filter_by(reflink=link).first()
        if session == None:
            logger.warn("Link is outdated")
            return False
        
        sid = session.sid
        
        glSessionPath = os.path.join(ConfigInterface.GL_SESSION_PATH, sid)
        lSessionPath = os.path.join(ConfigInterface.GL_USERS_PATH, username, ConfigInterface.USER_REPOS["s_repo"], sid)
        
        os.symlink(glSessionPath, lSessionPath)
        
        sData = self.ProjectGetData(sid)
        sData.permitedUsers.append(username)
        
        self.ProjectSetData(sid, sData)
        
        logger.info("User {user} added to permitted users in session {sid}".format(user=username, sid=sid))
        
        return True
