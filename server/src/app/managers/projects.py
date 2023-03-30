import uuid
from app.managers import RepositoryManager
from app.common import Callback, SessionData
from app.common.logging import logger
from app.models import SessionModel
from app import db

class ProjectManager():

    def __init__(self) -> None:
        pass

    def ProjectCreate(self, username: str, repName: str, isPublic: bool = False, isTemplate: bool = False) -> Callback:
        
        logger.info("Call ProjectCreate()...")
        
        newPID   = uuid.uuid4().hex
        link     = uuid.uuid4().hex
        
        manager = RepositoryManager()
        userProjects = manager.ProjectsGetAll()
        
        while newPID in userProjects:
            newPID = uuid.uuid4().hex
        
        if not manager.ProjectCreate(username, newPID, repName, isPublic=isPublic, isTemplate=isTemplate):
            logger.error("Project {pid} for user {user} failed".format(pid=newPID, user=username))
            return Callback(status=1, description="Project create failed!")

        s = SessionModel(newPID, link)
        db.session.add(s)
        db.session.commit()

        logger.info("Project {pid} for user {user} created".format(pid=newPID, user=username))
        return Callback(data=newPID)

    def ProjectRemove(self, username: str, pid: str) -> Callback:
        
        logger.info("Call ProjectRemove()...")

        manager = RepositoryManager()
        
        if not manager.IsUserProject(username, pid):
            logger.error("Project {pid} of user {user} doesn't exist".format(pid=pid, user=username))
            return Callback(status=1, description="Project doesn't exists!")
        
        if not manager.ProjectRemove(username, pid):
            logger.error("Project remove failed")
            return Callback(status=2, description="Project remove failed!")
        
        s = SessionModel.query.filter_by(sid=pid).one()
        if s == None:
            logger.error("Session {sid} doesn't exists".format(sid=pid))
            return False
        db.session.delete(s)
        db.session.commit()

        logger.info("Project {pid} of user {user} removed".format(pid=pid, user=username))
        
        return Callback()
    
    def ProjectGetUserList(self, username: str, isTemplate: bool = False) -> Callback:
        
        logger.info("Call ProjectGetUserList()...")
        
        manager = RepositoryManager()
        pDict = manager.ProjectsGetByUser(username, isTemplate)
        
        for pid in pDict:
            actions = {
                "open": {
                    "url": "/project/" + pid,
                    "method": "GET"
                },
                "edit": {
                    "url": "/project/" + pid,
                    "method": "PATCH"
                },
                "delete": {
                    "url": "/project/" + pid,
                    "method": "DELETE"
                }
            }
            pDict[pid].update({"actions": actions})

        if pDict == None:
            logger.warn("Get user list failed. User doesn't exists.")
            return Callback(status=1, description="User doesn't exists!")
        
        return Callback(data=pDict)
    
    def ProjectGet(self, username: str, pid: str) -> Callback:
        
        logger.info("Call ProjectGet()...")
        
        manager = RepositoryManager()
        
        if not manager.IsUserProject(username, pid):
            logger.error("Project {pid} of user {user} doesn't exist".format(pid=pid, user=username))
            return Callback(status=1, description="Project doesn't exists!")
        
        metaData = manager.ProjectGetMeta(pid)
        srcData = manager.ProjectGetFilesSrc(pid)
        
        if metaData == None or srcData == None:
            logger.warn("Getting Project {pid} of user {user} failed".format(pid=pid, user=username))
            return Callback(status=2, description="Getting data from project failed!")
        
        for file in srcData:
            actions = {
                    "open": {
                        "url": "/project/" + pid + "/" + file,
                        "method": "GET"
                    },
                    "edit": {
                        "url": "/project/" + pid + "/" + file,
                        "method": "PATCH"
                    },
                    "delete": {
                        "url": "/project/" + pid + "/" + file,
                        "method": "DELETE"
                    }
            }
            srcData[file].update({"actions": actions})

        return Callback(data={"meta": metaData.__dict__, "src": srcData})
    
    def ProjectGetFile(self, username: str, pid: str, filename: str) -> Callback:
        
        logger.info("Call ProjectGetFile()...")
        
        manager = RepositoryManager()
        
        if not manager.IsUserProject(username, pid):
            logger.error("Project {pid} of user {user} doesn't exist".format(pid=pid, user=username))
            return Callback(status=1, description="Project doesn't exists!")
        
        fileData = manager.ProjectGetFile(pid, filename)
        
        if fileData == None:
            logger.warn("Getting file {filename} in Project {pid} of user {user} failed".format(filename=filename, pid=pid, user=username))
            return Callback(status=2, description="Getting file from project failed!")
        
        return Callback(data=fileData)
    
    def ProjectSetFile(self, username: str, pid: str, filename: str, data: str) -> Callback:
        
        logger.info("Call ProjectSetFile()...")
        
        manager = RepositoryManager()
        
        if not manager.IsUserProject(username, pid):
            logger.error("Project {pid} of user {user} doesn't exist".format(pid=pid, user=username))
            return Callback(status=1, description="Project doesn't exists!")
        
        manager.ProjectSetFile(pid, filename, data)
        
        logger.info("File {filename} in Project {pid} of {user} updated".format(pid=pid, filename=filename, user=username))
        
        return Callback()
    
    def ProjectRemoveFile(self, username: str, pid: str, filename: str) -> Callback:
        logger.info("Call ProjectRemoveFile()...")
        
        manager = RepositoryManager()
        
        if not manager.IsUserProject(username, pid):
            logger.error("Project {pid} of user {user} doesn't exist".format(pid=pid, user=username))
            return Callback(status=1, description="Project doesn't exists!")
        
        manager.ProjectRemoveFile(pid, filename)
        
        logger.info("File {filename} in project {pid} of {user} removed".format(pid=pid, filename=filename, user=username))
        
        return Callback()
    
    def ProjectCreateFile(self, username: str, pid: str, filename: str) -> Callback:
        logger.info("Call ProjectCreateFile()...")
        
        manager = RepositoryManager()
        
        if not manager.IsUserProject(username, pid):
            logger.error("Project {pid} of user {user} doesn't exist".format(pid=pid, user=username))
            return Callback(status=1, description="Project doesn't exists!")
        
        manager.ProjectCreateFile(pid, filename)
        
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
    
    def ProjectSetMeta(self, username: str, pid: str, data: dict) -> Callback:
        
        logger.info("Call ProjectUpdate()...")
        
        manager = RepositoryManager()
        
        if not manager.IsUserProject(username, pid):
            logger.error("Project {pid} of user {user} doesn't exist".format(pid=pid, user=username))
            return Callback(status=1, description="Project doesn't exists!")
            
        try:
            sData = SessionData()
            sData.__dict__ = data
            manager.ProjectSetMeta(pid, sData)
        except Exception as e:
            logger.error("Error while updating project data of {pid}".format(pid=pid))
            logger.exception(e)
            return Callback(status=2, description="Setting project metadata failed!")
        
        logger.info("Project {pid} of {user} updated".format(pid=pid, user=username))
        
        return Callback()
    
    def ProjectNewLink(self, username: str, pid: str) -> Callback:
        
        logger.info("Call ProjectNewLink()...")
        
        manager = RepositoryManager()
        
        if not manager.IsUserProject(username, pid):
            logger.error("Project {pid} of user {user} doesn't exist".format(pid=pid, user=username))
            return Callback(status=1, description="Project doesn't exists!")
        
        newLink = manager.ProjectNewLink(pid)
        
        if newLink == None:
            logger.error("Error while generate share link")
            return Callback(status=2, description="Error while generate share link")
        
        logger.info("New share link for {pid} of {user} created".format(pid=pid, user=username))
        
        return Callback(data=newLink)
    
    def ProjectGetLink(self, username: str, pid: str) -> Callback:
        
        logger.info("Call ProjectGetLink()...")
        
        manager = RepositoryManager()
        
        if not manager.IsUserProject(username, pid):
            logger.error("Project {pid} of user {user} doesn't exist".format(pid=pid, user=username))
            return Callback(status=1, description="Project doesn't exists!")
        
        newLink = manager.ProjectGetLink(pid)
        
        if newLink == None:
            logger.error("Error while generate share link")
            return Callback(status=2, description="Error while generate share link")
        
        logger.info("New share link for {pid} of {user} created".format(pid=pid, user=username))
        
        return Callback(data=newLink)

    def ProjectUseLink(self, username: str, link: str) -> Callback:
        
        logger.info("Call ProjectUseLink()...")
        
        manager = RepositoryManager()
        
        if not manager.ProjectUseLink(username, link):
            logger.error("Using link {link} failed".format(link=link))
            return Callback(status=1, description="Link outdated!")
        logger.info("Share link {link} used for user {user}".format(link=link, user=username))
        
        return Callback()
    
    def ProjectCopy(self, username: str, pid: str) -> Callback:
        
        logger.info("Call ProjectCopy()...")
        
        manager = RepositoryManager()
        
        if not manager.IsUserProject(username, pid):
            logger.error("Project {sid} of user {user} doesn't exist".format(sid=pid, user=username))
            return Callback(status=1, description="Project doesn't exists!")
        
        newPID = uuid.uuid4().hex
        
        allProjects = manager.ProjectsGetAll()
        
        while newPID in allProjects:
            newPID = uuid.uuid4().hex
        
        if not manager.ProjectCopy(username, pid, newPID):
            logger.error("Copy project {sid} of user {user} failed".format(sid=pid, user=username))
            return Callback(status=2, description="Copy failed")
        
        return Callback()
        