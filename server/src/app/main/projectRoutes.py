from flask import jsonify, request, Blueprint
from app.managers import UserManager, ProjectManager, TemplateManager
from app.common import Callback
from app.common.auth import loginRequired
from app.common.logging import logger
import json

# actions = {
#     "S_ADD":       sManager.CreateSession,
#     "S_DEL":       sManager.RemoveSession,
#     "S_UPD":       sManager.UpdateSession,
#     "S_COPY":      sManager.CopySession,
#     "S_LIST":      sManager.GetUserSessionList,
#     "S_GET":       sManager.GetSession,
#     "S_GEN":       sManager.GeneratePage,
#     "S_SHARE":     sManager.ShareSession,
#     "S_USE_SHARE": sManager.UseSessionLink
# }

projectBlueprint = Blueprint('project_blueprint', __name__)

@projectBlueprint.route('/projects', methods=['GET'])
@loginRequired()
def projectList():
    username = request.json["user"]["name"]
    pManager   = ProjectManager()
    callback = pManager.ProjectGetUserList(username)
    return jsonify(callback.dump())

@projectBlueprint.route('/projects', methods=['PUT'])
@loginRequired()
def projectCreate():
    
    username = request.json["user"]["name"]
    if "data" not in request.json:
        logger.warn("'data' field needed")
        return jsonify(Callback(status=False).dump())
    repName  = request.json["data"]
    
    pManager   = ProjectManager()
    callback = pManager.ProjectCreate(username, repName)
    return jsonify(callback.dump())

@projectBlueprint.route('/project/<hash>', methods=['GET'])
@loginRequired()
def projectGet(hash):
    username = request.json["user"]["name"]
    pManager = ProjectManager()
    callback = pManager.ProjectGet(username, hash)
    return jsonify(callback.dump())

@projectBlueprint.route('/project/<hash>', methods=['PATCH'])
@loginRequired()
def projectUpdate(hash):
    username = request.json["user"]["name"]
    if "data" not in request.json:
        logger.warn("'data' field needed")
        return jsonify(Callback(status=False).dump())
    data     = request.json["data"]
    pManager = ProjectManager()
    callback = pManager.ProjectUpdate(username, hash, data)
    return jsonify(callback.dump())

@projectBlueprint.route('/project/<hash>', methods=['DELETE'])
@loginRequired()
def projectRemove(hash):
    username = request.json["user"]["name"]
    pManager = ProjectManager()
    callback = pManager.ProjectRemove(username, hash)
    return jsonify(callback.dump())

@projectBlueprint.route('/project/<hash>/<filename>', methods=['GET'])
@loginRequired()
def projectFileGet(hash, filename):
    username = request.json["user"]["name"]
    pManager = ProjectManager()
    callback = pManager.ProjectGetFile(username, hash, filename)
    return jsonify(callback.dump())

@projectBlueprint.route('/project/<hash>/<filename>', methods=['PATCH'])
@loginRequired()
def projectFileSet(hash, filename):
    username = request.json["user"]["name"]
    
    if "data" not in request.json:
        logger.warn("'data' field needed")
        return jsonify(Callback(status=False).dump())
    data     = request.json["data"]
    
    pManager = ProjectManager()
    callback = pManager.ProjectSetFile(username, hash, filename, data)
    return jsonify(callback.dump())

@projectBlueprint.route('/project/<hash>/<filename>', methods=['DELETE'])
@loginRequired()
def projectFileDelete(hash, filename):
    username = request.json["user"]["name"]
    pManager = ProjectManager()
    callback = pManager.ProjectRemoveFile(username, hash, filename)
    return jsonify(callback.dump())

@projectBlueprint.route('/project/<hash>/<filename>', methods=['PUT'])
@loginRequired()
def projectFileCreate(hash, filename):
    username = request.json["user"]["name"]
    pManager = ProjectManager()
    callback = pManager.ProjectCreateFile(username, hash, filename)
    return jsonify(callback.dump())

@projectBlueprint.route('/project/<hash>/<filename>/preview', methods=['GET'])
@loginRequired()
def projectFileCreate(hash, filename):
    username = request.json["user"]["name"]
    pManager = ProjectManager()
    callback = pManager.GeneratePage(username, hash, filename)
    return callback.data
