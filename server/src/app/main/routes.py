from flask import jsonify, request, Blueprint
from app.managers import UserManager, ProjectManager, TemplateManager
from app.common import Callback
from app.common.logging import logger
import json

main_bp = Blueprint('main_blueprint', __name__)

@main_bp.route('/request', methods=['GET', 'POST'])
def main():
    
    usrManager = UserManager()
    sManager   = ProjectManager()
    tManager   = TemplateManager()
    logged     = False
    
    actions = {
        "U_CHECK":     usrManager.ValidateUser,
        "U_REG":       usrManager.AddUser,
        "U_DEL":       usrManager.RemoveUser,
        "U_LIST":      usrManager.ListUsers,
        
        "S_ADD":       sManager.ProjectCreate,
        "S_DEL":       sManager.ProjectRemove,
        "S_UPD":       sManager.ProjectUpdate,
        "S_COPY":      sManager.ProjectCopy,
        "S_LIST":      sManager.ProjectGetUserList,
        "S_GET":       sManager.ProjectGet,
        "S_GEN":       sManager.GeneratePage,
        "S_SHARE":     sManager.ProjectShare,
        "S_USE_SHARE": sManager.ProjectUseLink,
        
        "T_ADD":       tManager.CreateTemplate,
        "T_UPD":       tManager.UpdateTemplate,
        "T_LIST":      tManager.GetUserTemplateList,
        "T_GET":       tManager.GetTemplate,
        "T_GEN":       tManager.GeneratePage,
        "T_SHARE":     tManager.ShareTemplate,
        "T_USE_SHARE": tManager.UseTemplateLink
    }
    
    if "action" not in request.json:
        logger.warn("Request doesn't have 'action' field...")
        logger.debug(json.dumps(request.json))
        callback = Callback(status=False).dump()
        return jsonify(callback)
    
    action = request.json["action"]
    logger.debug("Action: {act}".format(act=action))
    
    if action == "U_REG" or action == "U_CHECK":
        callback = actions[action]()
        return jsonify(callback.dump())
    
    if "user" in request.json:
        logged = usrManager.ValidateUser()
            
    if not logged.status:
        logger.warn("User not validated!")
        return jsonify(Callback(status=False).dump())
    
    callback = actions[action]()
    
    if action == "S_GEN":
        logger.info("Return page...")
        return callback.data
    
    return jsonify(callback.dump())