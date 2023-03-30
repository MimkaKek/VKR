import os
import shutil
import uuid
from datetime import datetime
from flask import render_template
from bs4 import BeautifulSoup
import re

from app import db
from app.cfg import ConfigInterface
from app.models import SessionModel
from app.common import UserData, SessionData
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
        
        if not os.path.exists(ConfigInterface.GL_PROJECT_PATH):
            os.makedirs(ConfigInterface.GL_PROJECT_PATH)
            
        if not os.path.exists(ConfigInterface.GL_USERS_PATH):
            os.makedirs(ConfigInterface.GL_USERS_PATH)

    def GetTemplates(self) -> dict[str, str]:

        templates = os.listdir(ConfigInterface.GL_TEMPLATES_PATH)
        tDict = {}

        for template in templates:
            meta = self.ProjectGetMeta(template)
            tDict[template] = meta.name

        return tDict
    
    def InitDefault(self, pid) -> bool:
        projectPath = os.path.join(ConfigInterface.GL_PROJECT_PATH, pid, ConfigInterface.PROJECT_REPOS["src"])
        presetPath  = os.path.join(ConfigInterface.PRESETS_PATH, "DEFAULT", ConfigInterface.PROJECT_REPOS["src"])
        return self.RepositoryCopy(projectPath, presetPath)
        

    # ==================================== USER =======================================
    
    def RepUserCreate(self, username: str) -> bool:
        logger.info("Call RepUserCreate()...")
        usrPath = os.path.join(ConfigInterface.GL_USERS_PATH, username)
        
        os.makedirs(usrPath)
        
        for dir in ConfigInterface.USER_REPOS:
            contentPath = os.path.join(usrPath, ConfigInterface.USER_REPOS[dir])
            if dir == "t_repo":
                os.symlink(ConfigInterface.GL_TEMPLATES_PATH, contentPath)
            else:
                os.makedirs(contentPath)
        
        usrDataPath = os.path.join(usrPath, ConfigInterface.USER_DATA)
        usrData     = UserData()

        usrData.registered = datetime.now().strftime('%Y.%m.%d')
        
        with open(usrDataPath, "w") as file:
            file.write(usrData.dump())
        
        logger.info("User repo created")
        
        return True
    
    def RepUserRemove(self, username: str) -> bool:
        logger.info("Call RemoveUserRep()...")
        usrPath = os.path.join(ConfigInterface.GL_USERS_PATH, username)
        
        if not os.path.exists(usrPath):
            logger.error("User already removed")
            return False
        
        sList = os.listdir(os.path.join(usrPath, ConfigInterface.USER_REPOS["p_repo"]))
        sData = SessionData()
        
        for sid in sList:
            sDataFile = os.path.join(usrPath, ConfigInterface.USER_REPOS["p_repo"], sid, ConfigInterface.PROJECT_DATA)
            with open(sDataFile, "r") as file:
                sData.load(file.read())
                
            if sData.owner == username:
                self.ProjectRemove(username, sid)

        os.unlink(usrPath, ConfigInterface.USER_REPOS["t_repo"])
        shutil.rmtree(usrPath)
        
        return True
    
    def RepUserExist(self, username: str) -> bool:
        uList = os.listdir(ConfigInterface.GL_USERS_PATH)
        return username in uList
    
    def RepUsersList(self) -> list:
        return os.listdir(ConfigInterface.GL_USERS_PATH)
        
    #======================================= PROJECT ===============================================
    
    def ProjectCreate(self, username: str, sid: str, repName: str, template: str = "DEFAULT", isPublic: bool = False, isTemplate: bool = False) -> bool:
        
        logger.info("Call CreateSessionRep()...")
        
        link = uuid.uuid4().hex
        s = SessionModel(sid, link)
        db.session.add(s)
        db.session.commit()
        
        usrPath = os.path.join(ConfigInterface.GL_USERS_PATH, username)
        glSessionPath = os.path.join(ConfigInterface.GL_PROJECT_PATH, sid)

        repo = "p_repo" if not isTemplate else "t_repo"

        lSessionPath  = os.path.join(usrPath, ConfigInterface.USER_REPOS[repo], sid)
        
        os.makedirs(glSessionPath)
        os.symlink(glSessionPath, lSessionPath)
        
        logger.info("Symlink for {sid} of {user} from {link} created".format(sid=sid, user=username, link=lSessionPath))

        sData             = SessionData()
        sData.owner       = username
        sData.name        = repName
        sData.public      = isPublic
        sData.created     = datetime.now().strftime('%Y.%m.%d %H:%M:%S')
        sData.lastUpdated = sData.created
        
        self.ProjectSetMeta(sid, sData)
        
        if template == None:
            logger.info("Repository created")
            return True
            
        templates = self.GetTemplates()
        projects  = self.ProjectsGetByUser(username)
        
        if template not in templates and template not in projects:
            if repName == "DEFAULT":
                return self.InitDefault(sid)
            
            logger.error("Template {path} doesn't exists".format(path=template))
            os.unlink(lSessionPath)
            shutil.rmtree(glSessionPath)
            return False
        
        if template in projects:
            templateSrcPath = os.path.join(usrPath, ConfigInterface.USER_REPOS["p_repo"], template, ConfigInterface.PROJECT_REPOS["src"])
        else:
            templateSrcPath = os.path.join(ConfigInterface.GL_TEMPLATES_PATH, template, ConfigInterface.PROJECT_REPOS["src"])

        lSessionSrcPath = os.path.join(lSessionPath, ConfigInterface.PROJECT_REPOS["src"])

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
        glSessionPath = os.path.join(ConfigInterface.GL_PROJECT_PATH, sid)
        lSessionPath  = os.path.join(usrPath, ConfigInterface.USER_REPOS["p_repo"], sid)
        
        sDataFile = os.path.join(lSessionPath, ConfigInterface.PROJECT_DATA)
        
        data = SessionData()
        
        with open(sDataFile, "r") as file:
            data.load(file.read())
        
        for user in data.permitedUsers:
            pUsrPath = os.path.join(ConfigInterface.GL_USERS_PATH, user, ConfigInterface.USER_REPOS["p_repo"], sid)
            os.unlink(pUsrPath)
            
        os.unlink(lSessionPath)
        shutil.rmtree(glSessionPath)
        logger.info("Session {sid} of {user} removed".format(sid=sid, user=username))
        return True
    
    def ProjectCopy(self, username: str, sid: str, newSID: str) -> bool:
        logger.info("Call CopySession()...")
        
        sData = self.ProjectGetMeta(sid)
        sData.name += " (copy)"
        
        if not self.ProjectCreate(username, newSID, sData.name, sid):
            return False
        
        logger.info("Session {sid} copied to {newsid} for user {user}".format(sid=sid, newsid=newSID, user=username))
        return True
        
    
    def ProjectsGetAll(self) -> dict:
        logger.info("Call ProjectsGetAll()...")

        result = {}
        
        sessions = os.listdir(ConfigInterface.GL_PROJECT_PATH)
        for sid in sessions:
            sData = self.ProjectGetMeta(sid)
            result.update({sid: {"name": sData.name, "owner": sData.owner, "created": sData.created}})
        
        logger.info("List of all sessions getted")
        
        return result
    
    def ProjectsGetByUser(self, username: str, isTemplate: bool = False) -> dict[str, dict]:
        logger.info("Call ProjectsGetByUser()...")

        result = {}
        
        repo = "p_repo" if not isTemplate else "t_repo"

        sPath = os.path.join(ConfigInterface.GL_USERS_PATH, username, ConfigInterface.USER_REPOS[repo])
        
        projects = os.listdir(sPath)
        for sid in projects:
            sData = self.ProjectGetMeta(sid)
            result.update({sid: {"name": sData.name, "created": sData.created, "last_updated": sData.lastUpdated, "owner": sData.owner}})
        
        logger.info("List of all projects getted")
        
        return result
    
    def IsUserProject(self, username: str, sid: str) -> bool:
        logger.info("Call IsUserProject()...")
        sPath = os.path.join(ConfigInterface.GL_USERS_PATH, username, ConfigInterface.USER_REPOS["p_repo"])
        sessions = os.listdir(sPath)        
        return sid in sessions
    
    #======================================= FILES ===============================================

    def ProjectGetFilesSrc(self, sid: str) -> dict[str, dict]:
        logger.info("Call GetSessionSrc()...")
        result = {}
        srcPath = os.path.join(ConfigInterface.GL_PROJECT_PATH, sid, ConfigInterface.PROJECT_REPOS["src"])
        for filename in os.listdir(srcPath):
            filePath = os.path.join(srcPath, filename)
            if os.path.isfile(filePath):
                with open(filePath, "r") as file:
                    result[filename] = {"src": file.read()}
                    
        logger.info("Src of session {sid} getted".format(sid=sid))
                    
        return result
    
    def ProjectGetFile(self, sid: str, filename: str) -> (str | None):
        logger.info("Call ProjectGetFile()...")
        result = None
        filePath = os.path.join(ConfigInterface.GL_PROJECT_PATH, sid, ConfigInterface.PROJECT_REPOS["src"], filename)
        
        if os.path.isfile(filePath):
            with open(filePath, "r") as file:
                result = file.read()
                    
        logger.info("File {filename} of session {sid} getted".format(filename=filename, sid=sid)) 
        return result
    
    def ProjectSetFile(self, sid: str, filename: str, data: str) -> bool:
        logger.info("Call ProjectSetFile()...")
        filePath = os.path.join(ConfigInterface.GL_PROJECT_PATH, sid, ConfigInterface.PROJECT_REPOS["src"], filename)
        with open(filePath, "w") as file:
            file.write(data)

        meta = self.ProjectGetMeta(sid)
        meta.lastUpdated = datetime.now().strftime('%Y.%m.%d %H:%M:%S')
        self.ProjectSetMeta(sid, meta)
        
        logger.info("File {filename} of session {sid} updated".format(filename=filename, sid=sid))
        return True
    
    def ProjectRemoveFile(self, sid: str, filename: str) -> bool:
        logger.info("Call ProjectRemoveFile()...")
        filePath = os.path.join(ConfigInterface.GL_PROJECT_PATH, sid, ConfigInterface.PROJECT_REPOS["src"], filename)
        if os.path.exists(filePath):
            meta = self.ProjectGetMeta(sid)
            meta.lastUpdated = datetime.now().strftime('%Y.%m.%d %H:%M:%S')
            self.ProjectSetMeta(sid, meta)
            os.remove(filePath)
        logger.info("File {filename} of session {sid} removed".format(filename=filename, sid=sid))
        return True
    
    def ProjectCreateFile(self, sid: str, filename: str) -> bool:
        logger.info("Call ProjectCreateFile()...")
        filePath = os.path.join(ConfigInterface.GL_PROJECT_PATH, sid, ConfigInterface.PROJECT_REPOS["src"], filename)
        if not os.path.exists(filePath):
            meta = self.ProjectGetMeta(sid)
            meta.lastUpdated = datetime.now().strftime('%Y.%m.%d %H:%M:%S')
            self.ProjectSetMeta(sid, meta)
            with open(filePath, "w") as f:
                pass
        logger.info("File {filename} of session {sid} created".format(filename=filename, sid=sid))
        return True
    
    #======================================= METADATA ===============================================

    def ProjectSetMeta(self, sid: str, sData: dict | SessionData) -> bool:
        
        logger.info("Call SetSessionData()...")
        
        sDataPath = os.path.join(ConfigInterface.GL_PROJECT_PATH, sid, ConfigInterface.PROJECT_DATA)
        metadata = SessionData()

        if os.path.exists(sDataPath):
            with open(sDataPath, "r") as file:
                metadata.load(file.read())

        metadata.__dict__.update(sData.__dict__)
        metadata.lastUpdated = datetime.now().strftime('%Y.%m.%d %H:%M:%S')

        with open(sDataPath, "w") as file:
            file.write(metadata.dump())
            
        logger.info("Session data for {sid} updated".format(sid=sid))
            
        return True
    
    def ProjectGetMeta(self, sid: str) -> SessionData:
        logger.info("Call GetSessionData()... global")
        
        result   = SessionData()
        dataPath = os.path.join(ConfigInterface.GL_PROJECT_PATH, sid, ConfigInterface.PROJECT_DATA)
        
        if os.path.exists(dataPath):
            with open(dataPath, "r") as file:
                result.load(file.read())
        
        logger.info("Session data get")
        
        return result
    
    #======================================= PREVIEW ===============================================

    def ProjectGetPage(self, sid: str, filename: str) -> str:
        
        logger.info("Call ProjectGetPage()...")
        repPath  = os.path.join(ConfigInterface.GL_PROJECT_PATH, sid, ConfigInterface.PROJECT_REPOS["src"])
        tempPath = os.path.join(repPath, filename)

        if not os.path.exists(tempPath):
            logger.error("File {filename} in {sid} doesn't exists".format(sid=sid, filename=filename))
            return ""

        html = ""
        with open(tempPath, "r") as f:
            html = f.read()

        parsedHtml = BeautifulSoup(html)
        try:
            for script in parsedHtml.find_all('script', {"src": re.compile(".*")}):
                src = ""
                scriptPath = os.path.join(repPath, script["src"])
                with open(scriptPath, "r") as file:
                    src = file.read()
                script.string = src
                script.attrs = None

            for style in parsedHtml.find_all('link', {"rel":"stylesheet"}):
                src = ""
                stylePath = os.path.join(repPath, style["href"])
                with open(stylePath, "r") as file:
                    src = file.read()
                style.string = src
                style.attrs = None
                style.name = "style"
        except Exception as e:
            logger.exception(e)
            return "Something go wrong..."
        return str(parsedHtml)
    
    #======================================= SHARE ===============================================

    def ProjectShare(self, sid: str) -> str:
        
        logger.info("Call ShareSession()...")
        
        sData = self.ProjectGetMeta(sid)
        sData.link = uuid.uuid4().hex
        
        session = SessionModel.query.filter_by(sid=sid).first()
        if session == None:
            logger.error("Session doesn't exists")
            return None
        
        session.reflink = sData.link
        db.session.commit()
        
        if not self.ProjectSetMeta(sid, sData):
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
        
        glSessionPath = os.path.join(ConfigInterface.GL_PROJECT_PATH, sid)
        lSessionPath = os.path.join(ConfigInterface.GL_USERS_PATH, username, ConfigInterface.USER_REPOS["p_repo"], sid)
        
        os.symlink(glSessionPath, lSessionPath)
        
        sData = self.ProjectGetMeta(sid)
        sData.permitedUsers.append(username)
        
        self.ProjectSetMeta(sid, sData)
        
        logger.info("User {user} added to permitted users in session {sid}".format(user=username, sid=sid))
        
        return True
