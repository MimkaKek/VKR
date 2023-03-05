import uuid
from app.managers import RepositoryManager
from app.common import Callback
from app.common.logging import logger

class ProjectManager():

    def __init__(self) -> None:
        pass

    def ProjectCreate(self, username: str, repName: str) -> Callback:
        
        logger.info("Call CreateProject()...")
        
        newPID   = uuid.uuid4().hex
        
        manager = RepositoryManager()
        userProjects = manager.ProjectsGetAll()
        
        while newPID in userProjects:
            newPID = uuid.uuid4().hex
        
        if not manager.ProjectCreate(username, newPID, repName):
            logger.error("Session {pid} for user {user} failed".format(pid=newPID, user=username))
            return Callback(status=False)

        logger.info("Session {pid} for user {user} created".format(pid=newPID, user=username))
        return Callback(data=newPID)

    def ProjectRemove(self, username: str, pid: str) -> Callback:
        
        logger.info("Call RemoveSession()...")

        manager = RepositoryManager()
        
        if not manager.IsUserProject(username, pid):
            logger.error("Session {pid} of user {user} doesn't exist".format(pid=pid, user=username))
            return Callback(status=False)
        
        if not manager.ProjectRemove(username, pid):
            logger.error("Session remove failed")
            return Callback(status=False)
        
        logger.info("Session {pid} of user {user} removed".format(pid=pid, user=username))
        
        return Callback()
    
    def ProjectGetUserList(self, username: str) -> Callback:
        
        logger.info("Call GetUserSessionList()...")
        
        manager = RepositoryManager()
        
        sList = manager.ProjectsGetByUser(username)
        
        if sList == None:
            logger.warn("Get user list failed. User doesn't exists.")
            return Callback(status=False)
        
        return Callback(data=sList)
    
    def ProjectGet(self, username: str, pid: str) -> Callback:
        
        logger.info("Call GetSession()...")
        
        manager = RepositoryManager()
        
        if not manager.IsUserProject(username, pid):
            logger.error("Session {pid} of user {user} doesn't exist".format(pid=pid, user=username))
            return Callback(status=False)
        
        sData = manager.ProjectGetData(pid)
        srcData = manager.ProjectGetSrc(pid)
        
        if sData == None or srcData == None:
            logger.warn("Getting session {pid} of user {user} failed".format(pid=pid, user=username))
            return Callback(status=False)
        
        return Callback(data={"data": sData.__dict__, "src": srcData})
    
    def ProjectGetFile(self, username: str, pid: str, filename: str) -> Callback:
        
        logger.info("Call ProjectGetFile()...")
        
        manager = RepositoryManager()
        
        if not manager.IsUserProject(username, pid):
            logger.error("Session {pid} of user {user} doesn't exist".format(pid=pid, user=username))
            return Callback(status=False)
        
        fileData = manager.ProjectGetFile(pid, filename)
        
        if fileData == None:
            logger.warn("Getting file {filename} in session {pid} of user {user} failed".format(filename=filename, pid=pid, user=username))
            return Callback(status=False)
        
        return Callback(data=fileData)
    
    def ProjectSetFile(self, username: str, pid: str, filename: str, data: str) -> Callback:
        
        logger.info("Call ProjectSetFile()...")
        
        manager = RepositoryManager()
        
        if not manager.IsUserProject(username, pid):
            logger.error("Session {pid} of user {user} doesn't exist".format(pid=pid, user=username))
            return Callback(status=False)
        
        manager.ProjectSetFile(pid, filename, data)
        
        logger.info("File {filename} in session {pid} of {user} updated".format(pid=pid, filename=filename, user=username))
        
        return Callback()
    
    def ProjectRemoveFile(self, username: str, pid: str, filename: str) -> Callback:
        logger.info("Call ProjectRemoveFile()...")
        
        manager = RepositoryManager()
        
        if not manager.IsUserProject(username, pid):
            logger.error("Session {pid} of user {user} doesn't exist".format(pid=pid, user=username))
            return Callback(status=False)
        
        manager.ProjectRemoveFile(pid, filename)
        
        logger.info("File {filename} in session {pid} of {user} removed".format(pid=pid, filename=filename, user=username))
        
        return Callback()
    
    def ProjectCreateFile(self, username: str, pid: str, filename: str) -> Callback:
        logger.info("Call ProjectCreateFile()...")
        
        manager = RepositoryManager()
        
        if not manager.IsUserProject(username, pid):
            logger.error("Session {pid} of user {user} doesn't exist".format(pid=pid, user=username))
            return Callback(status=False)
        
        manager.ProjectCreateFile(pid, filename)
        
        logger.info("File {filename} in session {pid} of {user} updated".format(pid=pid, filename=filename, user=username))
        
        return Callback(data={filename: ""})
    
    def GeneratePage(self, username: str, pid: str, filename: str) -> Callback:
        
        logger.info("Call GeneratePage()...")
        
        manager = RepositoryManager()
        
        if not manager.IsUserProject(username, pid):
            logger.error("Session {pid} of user {user} doesn't exist".format(pid=pid, user=username))
            return Callback(status=False)
        
        page = manager.ProjectGetPage(pid, filename)
        
        if page == None:
            logger.error("Getting page from {pid} of {user} failed".format(pid=pid, user=username))
            return Callback(status=False)
        
        return Callback(data=page)
    
    def ProjectUpdate(self, username: str, pid: str, data: dict) -> Callback:
        
        logger.info("Call UpdateSession()...")
        
        manager = RepositoryManager()
        
        if not manager.IsUserProject(username, pid):
            logger.error("Session {pid} of user {user} doesn't exist".format(pid=pid, user=username))
            return Callback(status=False)
        
        if "src" in data:
            srcData = data["src"]
            try:
                manager.ProjectSetSrc(pid, srcData)
            except Exception as e:
                logger.error("Error while updating src of {pid}".format(pid=pid))
                logger.exception(e)
                return Callback(status=False)
            
        if "session" in data:
            sData = data["session"]
            try:
                manager.ProjectSetData(pid, sData)
            except Exception as e:
                logger.error("Error while updating session data of {pid}".format(pid=pid))
                logger.exception(e)
                return Callback(status=False)
        
        logger.info("Session {pid} of {user} updated".format(pid=pid, user=username))
        
        return Callback()
    
    def ProjectShare(self, username: str, pid: str) -> Callback:
        
        logger.info("Call ShareSession()...")
        
        manager = RepositoryManager()
        
        if not manager.IsUserProject(username, pid):
            logger.error("Session {pid} of user {user} doesn't exist".format(pid=pid, user=username))
            return Callback(status=False)
        
        newLink = manager.ProjectShare(pid)
        
        if newLink == None:
            logger.error("Error while generate share link")
            return Callback(status=False)
        
        logger.info("New share link for {pid} of {user} created".format(pid=pid, user=username))
        
        return Callback(data=newLink)
    
    def ProjectUseLink(self, username: str, link: str) -> Callback:
        
        logger.info("Call UseSessionLink()...")
        
        manager = RepositoryManager()
        
        if not manager.ProjectUseShareLink(username, link):
            logger.error("Using link {link} failed".format(link=link))
            return Callback(status=False)
        logger.info("Share link {link} used for user {user}".format(link=link, user=username))
        
        return Callback()
    
    def ProjectCopy(self, username: str, pid: str) -> Callback:
        
        logger.info("Call CopySession()...")
        
        manager = RepositoryManager()
        
        if not manager.IsUserProject(username, pid):
            logger.error("Session {sid} of user {user} doesn't exist".format(sid=pid, user=username))
            return Callback(status=False)
        
        newPID = uuid.uuid4().hex
        
        userSessions = manager.ProjectsGetAll()
        
        while newPID in userSessions:
            newPID = uuid.uuid4().hex
        
        if not manager.ProjectCopy(username, pid, newPID):
            logger.error("Copy session {sid} of user {user} failed".format(sid=pid, user=username))
            return Callback(status=False)
        
        return Callback()
        