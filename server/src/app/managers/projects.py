import uuid
import copy
from app.managers import RepositoryManager
from app.common import Callback, ProjectData
from app.common.logging import logger
from app.models import ProjectModel
from app import db

from datetime import datetime

class ProjectManager():

    def __init__(self) -> None:
        pass
    
    def CreatePresets(self, username: str) -> bool:
        mgr  = RepositoryManager()
        presets = mgr.ListPresets()
        for preset in presets:
            tmp  = mgr.GetMetaPreset(preset)
            meta = ProjectData(owner=username, name=tmp.name, desc=tmp.description, isTemplate=True)
            pid  = self.CreateProject(username, meta).data["pid"]
            mgr.InitFromPreset(pid, preset)

        return True


    def CreateProject(self, username: str, meta: ProjectData = ProjectData(), template: str = None) -> Callback:
        logger.info("Call CreateProject()...")
        
        newPID   = uuid.uuid4().hex
        link     = uuid.uuid4().hex
        
        manager      = RepositoryManager()
        userProjects = manager.GetProjects()
        
        while newPID in userProjects:
            newPID = uuid.uuid4().hex
        
        if not manager.CreateProject(username, newPID, meta, template):
            logger.error("Project creation with pid {pid} for user {user} failed".format(pid=newPID, user=username))
            return Callback(status=1, description="Project create failed!")

        s = ProjectModel(newPID, link)
        db.session.add(s)
        db.session.commit()

        logger.info("Project {pid} for user {user} created".format(pid=newPID, user=username))
        return self.GetProject(username, newPID)

    def RemoveProject(self, username: str, pid: str) -> Callback:
        logger.info("Call RemoveProject()...")

        manager = RepositoryManager()
        
        if not manager.IsUserProject(username, pid):
            logger.error("Project {pid} of user {user} doesn't exist".format(pid=pid, user=username))
            return Callback(status=1, description="Project doesn't exists!")
        
        meta = manager.GetProjectMeta(pid)

        if meta.owner != username:
            logger.warn("User {name} tried to remove project {pid} of user {owner}! Rejected!".format(name=username, pid=pid, owner=meta.owner))
            return Callback(status=2, description="The project doesn't belong to you!")

        if not manager.RemoveProject(username, pid):
            logger.error("Project with pid {pid} remove failed!".format(pid=pid))
            return Callback(status=3, description="Project remove failed!")
        
        s = ProjectModel.query.filter_by(pid=pid).one()
        if s == None:
            logger.error("Session {pid} doesn't exists".format(pid=pid))
            return False
        db.session.delete(s)
        db.session.commit()

        logger.info("Project {pid} of user {user} removed".format(pid=pid, user=username))
        
        return Callback()
    
    def GetUserProjects(self, username: str, isTemplate: bool = False) -> Callback:
        logger.info("Call GetUserProjects()...")
        
        manager = RepositoryManager()
        pDict = manager.GetUserProjects(username, isTemplate)
        
        for pid in pDict:
            actions = {
                "url": "/project/" + pid,
                "methods": ["GET", "PATCH", "DELETE"]
            }
            pDict[pid].update({"actions": actions})

        if pDict == None:
            logger.warn("Get user list failed. User doesn't exists.")
            return Callback(status=1, description="User doesn't exists!")
        
        return Callback(data=pDict)
    
    def GetAllProjects(self, isAll: bool = False) -> Callback:
        logger.info("Call GetUserProjects()...")
        
        manager = RepositoryManager()
        pDict = manager.GetProjects(isAll)
        
        if pDict == None:
            logger.warn("Get user list failed. User doesn't exists.")
            return Callback(status=1, description="User doesn't exists!")
        
        for pid in pDict:
            actions = {
                "url": "/project/" + pid,
                "methods": "GET"
            }
            pDict[pid].update({"actions": actions})

        
        return Callback(data=pDict)

    def GetProject(self, username: str, pid: str) -> Callback:
        logger.info("Call GetProject()...")
        
        manager = RepositoryManager()
        meta    = manager.GetProjectMeta(pid)
        if meta == None:
            logger.warn("Getting Project Metadata {pid} of user {user} failed".format(pid=pid, user=username))
            return Callback(status=1, description="Getting metadata from project failed!")
        
        if not manager.IsUserProject(username, pid):
            if not meta.isPublic:
                logger.error("Project {pid} of user {user} doesn't exist".format(pid=pid, user=username))
                return Callback(status=2, description="Project doesn't exists!")
            
            newPID = uuid.uuid4().hex
            if not manager.CopyProject(username, pid, newPID):
                logger.error("Project {pid} failed to copy!".format(pid=pid))
                return Callback(status=3, description="Failed to create copy!")
            
            pid = newPID

        projectFiles = manager.GetProjectFiles(pid)
        if projectFiles == None:
            logger.warn("Getting Project Files {pid} of user {user} failed".format(pid=pid, user=username))
            return Callback(status=4, description="Getting files from project failed!")
        
        result = {}

        for file in projectFiles:
            actions = {
                    "url": "/project/" + pid + "/" + file,
                    "methods": ["GET", "PATCH", "DELETE"]
            }
            result[file] = {"actions": actions}

        return Callback(data={"pid": pid, "meta": meta.__dict__, "files": result})
    
    def GetTemplatesWithNames(self) -> Callback:
        mgr = RepositoryManager()
        templates = mgr.GetTemplatesWithNames()
        return Callback(data=templates)

    def GetFileProject(self, username: str, pid: str, filename: str) -> Callback:
        logger.info("Call GetFileProject()...")
        
        manager = RepositoryManager()
        
        if not manager.IsUserProject(username, pid):
            logger.error("Project {pid} of user {user} doesn't exist".format(pid=pid, user=username))
            return Callback(status=1, description="Project doesn't exists!")
        
        fileData = manager.GetProjectFile(pid, filename)
        
        if fileData == None:
            logger.warn("Getting file {filename} in Project {pid} of user {user} failed".format(filename=filename, pid=pid, user=username))
            return Callback(status=2, description="Getting file from project failed!")
        
        return Callback(data=fileData)
    
    def SetFileProject(self, username: str, pid: str, filename: str, data: str) -> Callback:
        logger.info("Call ProjectSetFile()...")
        
        manager = RepositoryManager()
        if not manager.IsUserProject(username, pid):
            logger.error("Project {pid} of user {user} doesn't exist".format(pid=pid, user=username))
            return Callback(status=1, description="Project doesn't exists!")
        
        manager.SetProjectFile(pid, filename, data)
        
        logger.info("File {filename} in Project {pid} of {user} updated".format(pid=pid, filename=filename, user=username))
        
        return Callback()
    
    def RemoveProjectFile(self, username: str, pid: str, filename: str) -> Callback:
        logger.info("Call RemoveProjectFile()...")
        
        manager = RepositoryManager()
        
        if not manager.IsUserProject(username, pid):
            logger.error("Project {pid} of user {user} doesn't exist".format(pid=pid, user=username))
            return Callback(status=1, description="Project doesn't exists!")
        
        manager.RemoveProjectFile(pid, filename)
        
        logger.info("File {filename} in project {pid} of {user} removed".format(pid=pid, filename=filename, user=username))
        
        return Callback()
    
    def CreateProjectFile(self, username: str, pid: str, filename: str) -> Callback:
        logger.info("Call CreateProjectFile()...")
        
        manager = RepositoryManager()
        
        if not manager.IsUserProject(username, pid):
            logger.error("Project {pid} of user {user} doesn't exist".format(pid=pid, user=username))
            return Callback(status=1, description="Project doesn't exists!")
        
        manager.CreateProjectFile(pid, filename)
        
        logger.info("File {filename} in project {pid} of {user} updated".format(pid=pid, filename=filename, user=username))
        
        return Callback(data="")
    
    def GeneratePage(self, username: str, pid: str, filename: str) -> Callback:
        
        logger.info("Call GeneratePage()...")
        
        manager = RepositoryManager()
        
        if not manager.IsUserProject(username, pid):
            logger.error("Project {pid} of user {user} doesn't exist".format(pid=pid, user=username))
            return Callback(status=1, description="Project doesn't exists!")
        
        page = manager.ProjectGetPage(pid, filename)
        
        if page == None:
            logger.error("Getting page from {pid} of {user} failed".format(pid=pid, user=username))
            return Callback(status=2, description="Getting page failed!")
        
        return Callback(data=page)
    
    def SetProjectMeta(self, username: str, pid: str, data: dict) -> Callback:
        
        logger.info("Call ProjectSetMeta()...")
        
        manager = RepositoryManager()
        
        if not manager.IsUserProject(username, pid):
            logger.error("Project {pid} of user {user} doesn't exist".format(pid=pid, user=username))
            return Callback(status=1, description="Project doesn't exists!")
        
        try:
            metaOld = manager.GetProjectMeta(pid)
            metaNew = copy.deepcopy(metaOld)
            metaNew.__dict__.update(data)
            metaNew.lastUpdated = datetime.now().strftime('%Y.%m.%d %H:%M:%S')
            manager.SetProjectMeta(pid, metaNew)
            manager.UpdateLinks(pid, metaOld, metaNew)
        except Exception as e:
            logger.error("Error while updating project data of {pid}".format(pid=pid))
            logger.exception(e)
            return Callback(status=2, description="Setting project metadata failed!")
        
        logger.info("Project {pid} of {user} updated".format(pid=pid, user=username))
        
        return Callback()
    
    def CreateLinkProject(self, username: str, pid: str) -> Callback:
        
        logger.info("Call CreateLinkProject()...")
        
        manager = RepositoryManager()
        
        if not manager.IsUserProject(username, pid):
            logger.error("Project {pid} of user {user} doesn't exist".format(pid=pid, user=username))
            return Callback(status=1, description="Project doesn't exists!")
        
        newLink = uuid.uuid4().hex
        project = ProjectModel.query.filter_by(pid=pid).first()
        if project == None:
            logger.error("Project doesn't exists")
            return None
        project.reflink = newLink
        db.session.commit()
        
        if newLink == None:
            logger.error("Error while generate share link")
            return Callback(status=2, description="Error while generate share link")
        
        logger.info("New share link {link} for {pid} of {user} created".format(link=newLink, pid=pid, user=username))
        
        return Callback(data=newLink)
    
    def GetLinkProject(self, username: str, pid: str) -> Callback:
        
        logger.info("Call GetLinkProject()...")
        
        manager = RepositoryManager()
        
        if not manager.IsUserProject(username, pid):
            logger.error("Project {pid} of user {user} doesn't exist".format(pid=pid, user=username))
            return Callback(status=1, description="Project doesn't exists!")
        
        project = ProjectModel.query.filter_by(pid=pid).first()
        if project == None:
            logger.error("Project doesn't exists")
            return None
        
        reflink = project.reflink
        if reflink == None:
            logger.error("Error while getting share link")
            return Callback(status=2, description="Error while getting share link")
        
        logger.info("New share link for {pid} of {user} created".format(pid=pid, user=username))
        
        return Callback(data=reflink)

    def UseLinkProject(self, username: str, link: str) -> Callback:
        
        logger.info("Call ProjectUseLink()...")
        
        manager = RepositoryManager()
        
        project = ProjectModel.query.filter_by(reflink=link).first()
        if project == None:
            logger.warn("Link is outdated")
            return False
        
        pid  = project.pid

        if not manager.UseLinkProject(username, pid):
            logger.error("Using link {link} failed".format(link=link))
            return Callback(status=1, description="Link outdated!")
        logger.info("Share link {link} used for user {user}".format(link=link, user=username))
        
        return Callback()
    
    def CopyProject(self, username: str, pid: str, isPublic: bool = False) -> Callback:
        
        logger.info("Call CopyProject()...")
        
        manager = RepositoryManager()
        
        if not manager.IsUserProject(username, pid) and not isPublic:
            logger.error("Project {pid} of user {user} doesn't exist".format(pid=pid, user=username))
            return Callback(status=1, description="Project doesn't exists!")
        
        newPID = uuid.uuid4().hex
        
        allProjects = manager.GetProjects(isAll=True)
        
        while newPID in allProjects:
            newPID = uuid.uuid4().hex
        
        if not manager.CopyProject(username, pid, newPID):
            logger.error("Copy project {pid} of user {user} failed".format(pid=pid, user=username))
            return Callback(status=2, description="Copy failed")
        
        return self.GetProject(username, newPID)
        