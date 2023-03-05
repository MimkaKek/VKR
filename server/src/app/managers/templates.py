import uuid

from flask import request
from app.managers import RepositoryManager
from app.common import Callback
from app.common.logging import logger

class TemplateManager():

    def __init__(self) -> None:
        pass

    def CreateTemplate(self) -> Callback:
        
        logger.info("Call CreateSession()...")
        
        manager = RepositoryManager()
        
        username = request.json["user"]["name"]
        
        if "data" not in request.json:
            logger.warn("'data' field needed")
            return Callback(status=False)
            
        repName  = request.json["data"]
        
        newTID   = uuid.uuid4().hex
        
        allTemplates = manager.GetAllTemplates()
        
        while newTID in allTemplates:
            newTID = uuid.uuid4().hex
        
        if not manager.CreateUserTemplate(username, newTID, repName):
            logger.error("Session {sid} for user {user} failed".format(sid=newTID, user=username))
            return Callback(status=False)

        logger.info("Session {sid} for user {user} created".format(sid=newTID, user=username))
        return Callback(data=newTID)

    def RemoveTemplate(self) -> Callback:
        
        logger.info("Call RemoveSession()...")
        
        username = request.json["user"]["name"]
        
        if "template" not in request.json:
            logger.warn("'template' field doesn't exists")
            return Callback(status=False)
        
        tid = request.json["template"]

        manager = RepositoryManager()
        
        if not manager.IsUserTemplate(username, tid):
            logger.error("Template {tid} of user {user} doesn't exist".format(tid=tid, user=username))
            return Callback(status=False)
        
        if not manager.RemoveTemplateRep(username, tid):
            logger.error("Session remove failed")
            return Callback(status=False)
        
        logger.info("Session {sid} of user {user} removed".format(sid=tid, user=username))
        
        return Callback()
    
    def GetUserTemplateList(self) -> Callback:
        logger.info("Call GetUserTemplateList()...")
        username = request.json["user"]["name"]
        manager = RepositoryManager()
        
        if not manager.RepUserExist(username):
            logger.error("User {user} doesn't exist".format(user=username))
        
        sList = manager.ProjectsGetByUser(username)
        
        return Callback(data=sList)
    
    def GetTemplate(self) -> Callback:
        
        logger.info("Call GetTemplate()...")
        
        username = request.json["user"]["name"]
        if "template" not in request.json:
            logger.warn("'data' field doesn't exists")
            return Callback(status=False)
        
        tid = request.json["template"]
        
        manager = RepositoryManager()
        if not manager.IsUserTemplate(username, tid):
            logger.error("Template {sid} of user {user} doesn't exist".format(sid=tid, user=username))
            return Callback(status=False)
        
        sData = manager.ProjectGetData(tid)
        srcData = manager.ProjectGetSrc(tid)
        
        if sData == None or srcData == None:
            logger.warn("Getting session {sid} of user {user} failed".format(sid=tid, user=username))
            return Callback(status=False)
        
        return Callback(data={"data": sData, "src": srcData})
    
    def GeneratePage(self) -> Callback:
        
        logger.info("Call GeneratePage()...")
        
        username = request.json["user"]["name"]
        
        if "template" not in request.json or "data" not in request.json:
            logger.warn("'template' or 'data' fields doesn't exists")
            return Callback(status=False)
        
        tid      = request.json["template"]
        
        manager = RepositoryManager()
        if not manager.IsUserTemplate(username, tid):
            logger.error("Template {tid} of user {user} doesn't exist".format(tid=tid, user=username))
            return Callback(status=False)
        
        page = manager.GetTemplatePage(username, tid)
        if page == None:
            logger.error("Getting page from {tid} of {user} failed".format(tid=tid, user=username))
            return Callback(status=False)
        
        return Callback(data=page)
    
    def UpdateTemplate(self) -> Callback:
        
        logger.info("Call UpdateTemplate()...")
        
        username    = request.json["user"]["name"]
        
        if "template" not in request.json or "data" not in request.json:
            logger.warn("'template' or 'data' fields doesn't exists")
            return Callback(status=False)
        
        tid          = request.json["template"]
        templateData = request.json["data"]
        
        manager = RepositoryManager()
        
        if not manager.IsUserTemplate(username, tid):
            logger.error("Template {tid} of user {user} doesn't exist".format(tid=tid, user=username))
            return Callback(status=False)
        
        if "src" in templateData:
            srcData = templateData["src"]
            try:
                manager.SetTemplateSrc(username, tid, srcData)
            except Exception as e:
                logger.error("Error while updating src of {tid}".format(tid=tid))
                logger.error(e)
                return Callback(status=False)
            
        if "template" in templateData:
            tData = manager.GetTemplateData(tid)
            for data in templateData["template"]:
                tData.__dict__[data] = templateData["template"][data]
            try:
                manager.SetTemplateData(username, tid, tData)
            except Exception as e:
                logger.error("Error while updating template data of {tid}".format(tid=tid))
                logger.error(e)
                return Callback(status=False)
        
        logger.info("Template {tid} of {user} updated".format(tid=tid, user=username))
        
        return Callback()
    
    def ShareTemplate(self) -> Callback:
        
        logger.info("Call ShareTemplate()...")
        
        if "template" not in request.json:
            logger.warn("'template' field doesn't exists")
            return Callback(status=False)
        
        username = request.json["user"]["name"]
        tid      = request.json["template"]
        
        manager = RepositoryManager()
        
        if not manager.IsUserTemplate(username, tid):
            logger.error("Template {tid} of user {user} doesn't exist".format(tid=tid, user=username))
            return Callback(status=False)
        
        newLink = manager.ShareTemplate(tid)
        
        if newLink == None:
            logger.error("Error while generate share link")
            return Callback(status=False)
        
        logger.info("New share link for {tid} of {user} created".format(tid=tid, user=username))
        
        return Callback(data=newLink)
    
    def UseTemplateLink(self) -> Callback:
        
        logger.info("Call UseTemplateLink()...")
        
        if "data" not in request.json:
            logger.warn("'data' field doesn't exists")
            return Callback(status=False)
        
        username = request.json["user"]["name"]
        link     = request.json["data"]
        
        manager = RepositoryManager()
        
        if not manager.UseTemplateShareLink(username, link):
            logger.error("Using link {link} failed".format(link=link))
            return Callback(status=False)
        logger.info("Share link {link} used for user {user}".format(link=link, user=username))
        
        return Callback()