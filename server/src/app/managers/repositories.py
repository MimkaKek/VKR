import os
import shutil
import json
from datetime import datetime
from flask import render_template
from bs4 import BeautifulSoup
import re

from app import db
from app.cfg import ConfigInterface
from app.models import ProjectModel
from app.common import UserData, ProjectData
from app.common.logging import logger

class RepositoryManager():

    #=============================== COMMON ========================================
    
    def __init__(self) -> None:
        pass
    
    def RepositoryCopy(self, dstPath: str, srcPath: str) -> bool:
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
        if not os.path.exists(ConfigInterface.GL_PUBLIC_PATH):
            os.makedirs(ConfigInterface.GL_PUBLIC_PATH)
        if not os.path.exists(ConfigInterface.GL_TEMPLATES_PATH):
            os.makedirs(ConfigInterface.GL_TEMPLATES_PATH)
    
    def InitFromPreset(self, pid, preset) -> bool:
        projectPath = os.path.join(ConfigInterface.GL_PROJECT_PATH, pid, ConfigInterface.PROJECT_REPOS["src"])
        presetPath  = os.path.join(ConfigInterface.PRESETS_PATH, preset, ConfigInterface.PROJECT_REPOS["src"])
        return self.RepositoryCopy(projectPath, presetPath)

    # =================================== PRESETS =====================================

    def ListPresets(self) -> list[str]:
        return os.listdir(os.path.join(ConfigInterface.PRESETS_PATH))

    def GetMetaPreset(self, preset) -> ProjectData:
        path = os.path.join(ConfigInterface.PRESETS_PATH, preset, ConfigInterface.PRESET_DATA)
        with open(path, "r") as file:
            tmp = json.load(file)
            logger.debug(tmp)
            return ProjectData(name=tmp['name'], desc=tmp['description'])

    # ==================================== USER =======================================
    
    def RepUserCreate(self, username: str) -> bool:
        usrPath = os.path.join(ConfigInterface.GL_USERS_PATH, username)
        
        if not os.path.exists(usrPath):
            os.makedirs(usrPath)
        
        for key, value in ConfigInterface.USER_REPOS.items():
            repoPath = os.path.join(usrPath, value)
            if not os.path.exists(repoPath):
                os.makedirs(repoPath)
        
        usrDataPath = os.path.join(usrPath, ConfigInterface.USER_DATA)
        usrData     = UserData()

        usrData.registered = datetime.now().strftime('%Y.%m.%d')
        
        with open(usrDataPath, "w") as file:
            file.write(usrData.dump())
        
        logger.info("User repo created")
        
        return True
    
    def RepUserRemove(self, username: str) -> bool:
        usrPath = os.path.join(ConfigInterface.GL_USERS_PATH, username)
        
        if not os.path.exists(usrPath):
            logger.error("User already removed")
            return False
        
        pList = os.listdir(os.path.join(usrPath, ConfigInterface.USER_REPOS["p_repo"]))
        tList = os.listdir(os.path.join(usrPath, ConfigInterface.USER_REPOS["t_repo"]))
        
        for pid in pList:
            meta = self.GetProjectMeta(pid)
            if meta == None:
                logger.error("Failed get metadata for {pid} of user {user}".format(pid=pid, user=username))
                return False
            
            if meta.owner == username:
                self.RemoveProject(username, pid)

        for pid in tList:
            meta = self.GetProjectMeta(pid)
            if meta == None:
                logger.error("Failed get metadata for {pid} of user {user}".format(pid=pid, user=username))
                return False
            
            if meta.owner == username:
                self.RemoveProject(username, pid)

        shutil.rmtree(usrPath)
        
        return True
    
    def RepUserExist(self, username: str) -> bool:
        uList = os.listdir(ConfigInterface.GL_USERS_PATH)
        return username in uList
    
    def RepUsersList(self) -> list:
        return os.listdir(ConfigInterface.GL_USERS_PATH)

    #======================================= PROJECT ===============================================
    
    def CreateProject(self, username: str, pid: str, meta: ProjectData = ProjectData(), templateID: str = None, copy: bool = False) -> bool:

        # Set Links

        repo    = "t_repo" if meta.isTemplate else "p_repo"
        usrPath = os.path.join(ConfigInterface.GL_USERS_PATH, username)

        glProjectPath = os.path.join(ConfigInterface.GL_PROJECT_PATH, pid)
        lProjectPath  = os.path.join(usrPath, ConfigInterface.USER_REPOS[repo], pid)

        if not os.path.exists(glProjectPath):
            os.makedirs(os.path.join(glProjectPath, ConfigInterface.PROJECT_REPOS["src"]))

        os.symlink(glProjectPath, lProjectPath)

        if meta.isTemplate:
            os.symlink(glProjectPath, os.path.join(ConfigInterface.GL_TEMPLATES_PATH, pid))

        if meta.isPublic:
            os.symlink(glProjectPath, os.path.join(ConfigInterface.GL_PUBLIC_PATH, pid))
        
        logger.info("Symlink for {pid} of {user} from {link} created".format(pid=pid, user=username, link=lProjectPath))

        # Set MetaData
        
        self.SetProjectMeta(pid, meta)
        
        # Use template

        if templateID == None:
            logger.info("Repository created")
            return True
        
        templateSrcPath = None

        if not os.path.exists(os.path.join(ConfigInterface.GL_TEMPLATES_PATH, templateID)):
            if not copy or not os.path.exists(os.path.join(ConfigInterface.GL_PROJECT_PATH, templateID)):
                logger.error("Template {path} doesn't exists. Rollback changes".format(path=templateID))
                os.unlink(lProjectPath)
                shutil.rmtree(glProjectPath)
                return False
            templateSrcPath = os.path.join(os.path.join(ConfigInterface.GL_PROJECT_PATH, templateID, ConfigInterface.PROJECT_REPOS["src"]))
        else:
            templateSrcPath = os.path.join(ConfigInterface.GL_TEMPLATES_PATH, templateID, ConfigInterface.PROJECT_REPOS["src"])

        lSessionSrcPath = os.path.join(lProjectPath, ConfigInterface.PROJECT_REPOS["src"])

        self.RepositoryCopy(lSessionSrcPath, templateSrcPath)

        logger.info("Repository created")
        
        return True
        
    def RemoveProject(self, username: str, pid: str) -> bool:
        
        # Unlink
        usrPath       = os.path.join(ConfigInterface.GL_USERS_PATH, username)
        glProjectPath = os.path.join(ConfigInterface.GL_PROJECT_PATH, pid)
        lProjectPath  = os.path.join(usrPath, ConfigInterface.USER_REPOS["p_repo"], pid)

        meta = self.GetProjectMeta(pid)
        if meta == None:
            logger.error("Failed get metadata for {pid} of user {user}".format(pid=pid, user=username))
            return False
        
        for user in meta.permitedUsers:
            os.unlink(os.path.join(ConfigInterface.GL_USERS_PATH, user, ConfigInterface.USER_REPOS["p_repo"], pid))

        if meta.isTemplate:
            os.unlink(os.path.join(ConfigInterface.GL_TEMPLATES_PATH, pid))

        if meta.isPublic:
            os.unlink(os.path.join(ConfigInterface.GL_PUBLIC_PATH, pid))
            
        os.unlink(lProjectPath)

        # Remove
        shutil.rmtree(glProjectPath)

        logger.info("Project {pid} of {user} removed".format(pid=pid, user=username))
        return True
    
    def CopyProject(self, username: str, pid: str, newpid: str) -> bool:
        meta = self.GetProjectMeta(pid)
        if meta == None:
            logger.error("Failed get metadata for {pid} of user {user}".format(pid=pid, user=username))
            return False
        
        meta.name          += " (copy)"
        meta.permitedUsers  = []
        meta.isTemplate     = False
        meta.isPublic       = False
        meta.created        = datetime.now().strftime('%Y.%m.%d %H:%M:%S')
        meta.lastUpdated    = datetime.now().strftime('%Y.%m.%d %H:%M:%S')
        meta.isCopy         = True
        
        copy = True

        if not self.CreateProject(username, newpid, meta, pid, copy):
            return False
        
        logger.info("Project {pid} copied to {newpid} for user {user}".format(pid=pid, newpid=newpid, user=username))
        return True
    
    def GetProjects(self, isAll: bool = False) -> dict[str, dict]:
        result = {}
        pPath  = ConfigInterface.GL_PROJECT_PATH if isAll else ConfigInterface.GL_PUBLIC_PATH

        sessions = os.listdir(pPath)
        for pid in sessions:
            meta = self.GetProjectMeta(pid)
            if meta == None:
                logger.error("Failed get metadata for {pid}".format(pid=pid))
                return result
            result[pid] = {"name": meta.name, "description": meta.description, "owner": meta.owner, "lastUpdated": meta.lastUpdated}
        
        logger.info("List of all projects getted")
        return result
    
    def GetUserProjects(self, username: str, isTemplate: bool = False) -> dict[str, dict]:
        result = {}
        repo   = "t_repo" if isTemplate else "p_repo"
        sPath  = os.path.join(ConfigInterface.GL_USERS_PATH, username, ConfigInterface.USER_REPOS[repo])
        
        projects = os.listdir(sPath)
        for pid in projects:
            meta = self.GetProjectMeta(pid)
            if meta == None:
                logger.error("Failed get metadata for {pid} of user {user}".format(pid=pid, user=username))
                return result
            result.update({pid: {"name": meta.name, "description": meta.description, "created": meta.created, "lastUpdated": meta.lastUpdated, "owner": meta.owner, "isPublic": meta.isPublic}})
        
        logger.info("List of user projects getted")
        
        return result

    def IsUserProject(self, username: str, pid: str) -> bool:
        for _, repo in ConfigInterface.USER_REPOS.items():
            path     = os.path.join(ConfigInterface.GL_USERS_PATH, username, repo)
            projects = os.listdir(path)
            if pid in projects:
                return True
        
        return False
    
    def GetTemplates(self) -> list[str]:
        return os.listdir(ConfigInterface.GL_TEMPLATES_PATH)
    
    def GetTemplatesWithNames(self) -> dict[str, str]:
        result = {}
        templatesID = self.GetTemplates()
        for pid in templatesID:
            meta = self.GetProjectMeta(pid)
            result[pid] = meta.name
        return result

    #======================================= FILES ===============================================

    def GetProjectFiles(self, pid: str) -> list[str]:
        srcPath = os.path.join(ConfigInterface.GL_PROJECT_PATH, pid, ConfigInterface.PROJECT_REPOS["src"])
        return os.listdir(srcPath)
    
    def GetProjectFile(self, pid: str, filename: str) -> str | None:
        result = None
        filePath = os.path.join(ConfigInterface.GL_PROJECT_PATH, pid, ConfigInterface.PROJECT_REPOS["src"], filename)
        
        if os.path.isfile(filePath):
            with open(filePath, "r") as file:
                result = file.read()
                    
        logger.info("File {filename} of project {pid} getted".format(filename=filename, pid=pid)) 
        return result
    
    def SetProjectFile(self, pid: str, filename: str, data: dict[str, str]) -> bool:
        filePath = os.path.join(ConfigInterface.GL_PROJECT_PATH, pid, ConfigInterface.PROJECT_REPOS["src"], filename)

        content = data.get("content", None)
        if content is not None:
            with open(filePath, "w") as file:
                file.write(content)

        newName = data.get("name", None)
        if newName is not None and filename != newName:
            newFilePath = os.path.join(ConfigInterface.GL_PROJECT_PATH, pid, ConfigInterface.PROJECT_REPOS["src"], newName)
            os.rename(filePath, newFilePath)

        meta = self.GetProjectMeta(pid)
        if meta == None:
            logger.error("Failed get metadata for {pid}".format(pid=pid))
            return False
        
        meta.lastUpdated = datetime.now().strftime('%Y.%m.%d %H:%M:%S')
        self.SetProjectMeta(pid, meta)
        
        logger.info("File {filename} of project {pid} updated".format(filename=filename, pid=pid))
        return True
    
    def CreateProjectFile(self, pid: str, filename: str) -> bool:
        filePath = os.path.join(ConfigInterface.GL_PROJECT_PATH, pid, ConfigInterface.PROJECT_REPOS["src"], filename)
        if not os.path.exists(filePath):
            meta = self.GetProjectMeta(pid)
            if meta == None:
                logger.error("Failed get metadata for {pid}".format(pid=pid))
                return False
            
            meta.lastUpdated = datetime.now().strftime('%Y.%m.%d %H:%M:%S')
            self.SetProjectMeta(pid, meta)
            with open(filePath, "w") as f:
                pass
        logger.info("File {filename} of project {pid} created".format(filename=filename, pid=pid))
        return True
    
    def RemoveProjectFile(self, pid: str, filename: str) -> bool:
        filePath = os.path.join(ConfigInterface.GL_PROJECT_PATH, pid, ConfigInterface.PROJECT_REPOS["src"], filename)
        if os.path.exists(filePath):
            meta = self.GetProjectMeta(pid)
            if meta == None:
                logger.error("Failed get metadata for {pid}".format(pid=pid))
                return False
        
            meta.lastUpdated = datetime.now().strftime('%Y.%m.%d %H:%M:%S')
            self.SetProjectMeta(pid, meta)
            os.remove(filePath)
        logger.info("File {filename} of project {pid} removed".format(filename=filename, pid=pid))
        return True
    
    def UpdateLinks(self, pid: str, username: str, metaOld: ProjectData, metaNew: ProjectData) -> bool:
        
        projectPath      = os.path.join(ConfigInterface.GL_PROJECT_PATH, pid)
        publicPath       = os.path.join(ConfigInterface.GL_PUBLIC_PATH, pid)
        templatePath     = os.path.join(ConfigInterface.GL_TEMPLATES_PATH, pid)
        loc_projectPath  = os.path.join(ConfigInterface.GL_USERS_PATH, username, ConfigInterface.USER_REPOS["p_repo"], pid)
        loc_templatePath = os.path.join(ConfigInterface.GL_USERS_PATH, username, ConfigInterface.USER_REPOS["t_repo"], pid)

        try:
            if metaOld.isPublic != metaNew.isPublic:
                if metaOld.isPublic:
                    os.unlink(publicPath)
                else:
                    os.symlink(projectPath, publicPath)

            if metaOld.isTemplate != metaNew.isTemplate:
                if metaOld.isTemplate:
                    os.unlink(templatePath)
                    os.unlink(loc_templatePath)
                    os.symlink(projectPath, loc_projectPath)
                else:
                    os.symlink(projectPath, loc_templatePath)
                    os.symlink(projectPath, templatePath)
                    os.unlink(loc_projectPath)
        except Exception as e:
            logger.error("Update links failed for project {pid}".format(pid=pid))
            logger.exception(e)
            return False
        
        return True
    
    #======================================= METADATA ===============================================

    def SetProjectMeta(self, pid: str, sData: ProjectData) -> bool:
        
        sDataPath = os.path.join(ConfigInterface.GL_PROJECT_PATH, pid, ConfigInterface.PROJECT_DATA)
        with open(sDataPath, "w") as file:
            file.write(sData.dump())
            
        logger.info("Session data for {pid} updated".format(pid=pid))
        return True
    
    def GetProjectMeta(self, pid: str) -> ProjectData | None:
        
        result   = None
        dataPath = os.path.join(ConfigInterface.GL_PROJECT_PATH, pid, ConfigInterface.PROJECT_DATA)
        if os.path.exists(dataPath):
            with open(dataPath, "r") as file:
                result = ProjectData()
                result.load(file.read())
        
        logger.info("Project data get from {pid}".format(pid=pid))
        return result
    
    #======================================= PREVIEW ===============================================

    def ProjectGetPage(self, pid: str, filename: str) -> str:
        repPath  = os.path.join(ConfigInterface.GL_PROJECT_PATH, pid, ConfigInterface.PROJECT_REPOS["src"])
        tempPath = os.path.join(repPath, filename)

        if not os.path.exists(tempPath):
            logger.error("File {filename} in {pid} doesn't exists".format(pid=pid, filename=filename))
            return ""

        html = ""
        with open(tempPath, "r") as f:
            html = f.read()

        parsedHtml = BeautifulSoup(html, "html.parser")
        try:
            for script in parsedHtml.find_all('script', {"src": re.compile(".*")}):
                src = ""
                if "http" in script["src"]:
                    continue
                scriptPath = os.path.join(repPath, script["src"])
                with open(scriptPath, "r") as file:
                    src = file.read()
                script.string = src
                script.attrs = None

            for style in parsedHtml.find_all('link', {"rel":"stylesheet"}):
                src = ""
                if "http" in style["href"]:
                    continue
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

    def UseLinkProject(self, username: str, pid: str) -> bool:
        
        meta = self.GetProjectMeta(pid)
        if meta == None:
            logger.error("Failed get metadata for {pid} of user {user}".format(pid=pid, user=username))
            return False
        
        repo = "t_repo" if meta.isTemplate else "p_repo"

        glProjectPath = os.path.join(ConfigInterface.GL_PROJECT_PATH, pid)
        lProjectPath  = os.path.join(ConfigInterface.GL_USERS_PATH, username, ConfigInterface.USER_REPOS[repo], pid)
        
        os.symlink(glProjectPath, lProjectPath)
        
        meta.permitedUsers.append(username)
        self.SetProjectMeta(pid, meta)
        
        logger.info("User {user} added to permitted users in project {pid}".format(user=username, pid=pid))
        
        return True
