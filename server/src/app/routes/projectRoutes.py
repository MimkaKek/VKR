from flask import jsonify, request, Blueprint
from app.managers import ProjectManager
from app.common import Callback
from app.common.auth import loginRequired
from app.common.logging import logger
from app.cfg import ConfigInterface as cfg

projectBlueprint = Blueprint('project_blueprint', __name__)

@projectBlueprint.route('/templates', methods=['GET'])
@loginRequired(cfg.ROLES.TEACHER)
def templateList():
    username = request.json["user"]["name"]
    pManager = ProjectManager()
    callback = pManager.ProjectGetUserList(username, isTemplate=True)
    return jsonify(callback.dict())

@projectBlueprint.route('/templates', methods=['PUT'])
@loginRequired(cfg.ROLES.TEACHER)
def templateCreate():
    
    username = request.json["user"]["name"]
    if "data" not in request.json:
        logger.warn("'data' field needed")
        return jsonify(Callback(status=1, description="'data' field required").dict())
    repName  = request.json["data"]
    
    pManager = ProjectManager()
    callback = pManager.ProjectCreate(username, repName)
    return jsonify(callback.dict())

@projectBlueprint.route('/projects', methods=['GET'])
@loginRequired(cfg.ROLES.STUDENT)
def projectList():
    username = request.json["user"]["name"]
    pManager = ProjectManager()
    callback = pManager.ProjectGetUserList(username)
    return jsonify(callback.dict())

@projectBlueprint.route('/projects', methods=['PUT'])
@loginRequired(cfg.ROLES.STUDENT)
def projectCreate():
    
    username = request.json["user"]["name"]
    if "data" not in request.json:
        logger.warn("'data' field needed")
        return jsonify(Callback(status=1, description="'data' field required").dict())
    repName  = request.json["data"]
    
    pManager = ProjectManager()
    callback = pManager.ProjectCreate(username, repName)
    return jsonify(callback.dict())

@projectBlueprint.route('/project/<hash>', methods=['GET'])
@loginRequired(cfg.ROLES.STUDENT)
def projectGet(hash):
    username = request.json["user"]["name"]
    pManager = ProjectManager()
    callback = pManager.ProjectGet(username, hash)
    return jsonify(callback.dict())

@projectBlueprint.route('/project/<hash>', methods=['PATCH'])
@loginRequired(cfg.ROLES.STUDENT)
def projectUpdate(hash):
    username = request.json["user"]["name"]
    if "data" not in request.json:
        logger.warn("'data' field needed")
        return jsonify(Callback(status=1, description="'data' field required").dict())
    data     = request.json["data"]
    pManager = ProjectManager()
    callback = pManager.ProjectSetMeta(username, hash, data)
    return jsonify(callback.dict())

@projectBlueprint.route('/project/<hash>', methods=['DELETE'])
@loginRequired(cfg.ROLES.STUDENT)
def projectRemove(hash):
    username = request.json["user"]["name"]
    pManager = ProjectManager()
    callback = pManager.ProjectRemove(username, hash)
    return jsonify(callback.dict())

@projectBlueprint.route('/project/<hash>', methods=['POST'])
@loginRequired(cfg.ROLES.STUDENT)
def projectCopy(hash):
    username = request.json["user"]["name"]
    pManager = ProjectManager()
    callback = pManager.ProjectCopy(username, hash)
    return jsonify(callback.dict())

@projectBlueprint.route('/project/<hash>/<filename>', methods=['GET'])
@loginRequired(cfg.ROLES.STUDENT)
def projectFileGet(hash, filename):
    username = request.json["user"]["name"]
    pManager = ProjectManager()
    callback = pManager.ProjectGetFile(username, hash, filename)
    return jsonify(callback.dict())

@projectBlueprint.route('/project/<hash>/<filename>', methods=['PATCH'])
@loginRequired(cfg.ROLES.STUDENT)
def projectFileSet(hash, filename):
    username = request.json["user"]["name"]
    
    if "data" not in request.json:
        logger.warn("'data' field needed")
        return jsonify(Callback(status=1, description="'data' field required").dict())
    data     = request.json["data"]
    
    pManager = ProjectManager()
    callback = pManager.ProjectSetFile(username, hash, filename, data)
    return jsonify(callback.dict())

@projectBlueprint.route('/project/<hash>/<filename>', methods=['DELETE'])
@loginRequired(cfg.ROLES.STUDENT)
def projectFileDelete(hash, filename):
    username = request.json["user"]["name"]
    pManager = ProjectManager()
    callback = pManager.ProjectRemoveFile(username, hash, filename)
    return jsonify(callback.dict())

@projectBlueprint.route('/project/<hash>/<filename>', methods=['PUT'])
@loginRequired(cfg.ROLES.STUDENT)
def projectFileCreate(hash, filename):
    username = request.json["user"]["name"]
    pManager = ProjectManager()
    callback = pManager.ProjectCreateFile(username, hash, filename)
    return jsonify(callback.dict())

@projectBlueprint.route('/project/<hash>/<filename>/preview', methods=['GET'])
@loginRequired(cfg.ROLES.STUDENT)
def projectFilePreview(hash, filename):
    username = request.json["user"]["name"]
    pManager = ProjectManager()
    callback = pManager.GeneratePage(username, hash, filename)
    return callback.data
