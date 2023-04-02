from flask import jsonify, request, Blueprint
from app.managers import ProjectManager, UserManager
from app.common import Callback, ProjectData
from app.common.auth import loginRequired
from app.common.logging import logger
from app.cfg import ConfigInterface as cfg

projectBlueprint = Blueprint('project_blueprint', __name__)

@projectBlueprint.route('/templates_all', methods=['GET'])
@loginRequired(cfg.ROLES.STUDENT)
def templatesAllList():
    pManager = ProjectManager()
    callback = pManager.GetTemplatesWithNames()
    return jsonify(callback.dict())

@projectBlueprint.route('/templates', methods=['GET'])
@loginRequired(cfg.ROLES.STUDENT)
def templatesList():
    username = request.json["user"]["name"]
    pManager = ProjectManager()
    callback = pManager.GetUserProjects(username, isTemplate=True)
    return jsonify(callback.dict())

@projectBlueprint.route('/public_projects', methods=['GET'])
@loginRequired(cfg.ROLES.STUDENT)
def publicProjects():
    pManager = ProjectManager()
    callback = pManager.GetAllProjects()
    return jsonify(callback.dict())

@projectBlueprint.route('/projects', methods=['GET'])
@loginRequired(cfg.ROLES.STUDENT)
def projectsList():
    username = request.json["user"]["name"]
    pManager = ProjectManager()
    callback = pManager.GetUserProjects(username)
    return jsonify(callback.dict())

@projectBlueprint.route('/projects', methods=['PUT'])
@loginRequired(cfg.ROLES.STUDENT)
def projectsCreate():
    username = request.json["user"]["name"]
    if "data" not in request.json:
        logger.warn("'data' field needed")
        return jsonify(Callback(status=1, description="'data' field required").dict())
    if "meta" not in request.json["data"]:
        logger.warn("'meta' field needed")
        return jsonify(Callback(status=1, description="'meta' field required").dict())
    
    meta = ProjectData()
    meta.__dict__.update(request.json["data"]["meta"])
    meta.owner = username

    templateID = None
    if "tid" in request.json["data"]:
        templateID = request.json["data"]["tid"]
    
    pManager = ProjectManager()
    callback = pManager.CreateProject(username, meta, templateID)
    return jsonify(callback.dict())

@projectBlueprint.route('/project/<hash>', methods=['GET'])
@loginRequired(cfg.ROLES.STUDENT)
def projectGet(hash):
    username = request.json["user"]["name"]
    pManager = ProjectManager()
    callback = pManager.GetProject(username, hash)
    return jsonify(callback.dict())

@projectBlueprint.route('/project/<hash>', methods=['PATCH'])
@loginRequired(cfg.ROLES.STUDENT)
def projectUpdate(hash):
    username = request.json["user"]["name"]
    if "data" not in request.json:
        logger.warn("'data' field needed")
        return jsonify(Callback(status=1, description="'data' field required").dict())
    data     = request.json["data"]

    if "isTemplate" in data:
        userMgr = UserManager()
        role = userMgr.GetRole(username)
        if role == cfg.ROLES.STUDENT:
            logger.warn("Attempt to change some specific meta for project {pid} by user {name}".format(pid=hash, name=username))
            data.pop("isTemplate")

    pManager = ProjectManager()
    callback = pManager.SetProjectMeta(username, hash, data)
    return jsonify(callback.dict())

@projectBlueprint.route('/project/<hash>', methods=['DELETE'])
@loginRequired(cfg.ROLES.STUDENT)
def projectRemove(hash):
    username = request.json["user"]["name"]
    pManager = ProjectManager()
    callback = pManager.RemoveProject(username, hash)
    return jsonify(callback.dict())

@projectBlueprint.route('/project/<hash>', methods=['POST'])
@loginRequired(cfg.ROLES.STUDENT)
def projectCopy(hash):
    username = request.json["user"]["name"]
    pManager = ProjectManager()
    callback = pManager.CopyProject(username, hash)
    return jsonify(callback.dict())

@projectBlueprint.route('/project/<hash>/<filename>', methods=['GET'])
@loginRequired(cfg.ROLES.STUDENT)
def projectFileGet(hash, filename):
    username = request.json["user"]["name"]
    pManager = ProjectManager()
    callback = pManager.GetFileProject(username, hash, filename)
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
    callback = pManager.SetFileProject(username, hash, filename, data)
    return jsonify(callback.dict())

@projectBlueprint.route('/project/<hash>/<filename>', methods=['DELETE'])
@loginRequired(cfg.ROLES.STUDENT)
def projectFileDelete(hash, filename):
    username = request.json["user"]["name"]
    pManager = ProjectManager()
    callback = pManager.RemoveProjectFile(username, hash, filename)
    return jsonify(callback.dict())

@projectBlueprint.route('/project/<hash>/<filename>', methods=['PUT'])
@loginRequired(cfg.ROLES.STUDENT)
def projectFileCreate(hash, filename):
    username = request.json["user"]["name"]
    pManager = ProjectManager()
    callback = pManager.CreateProjectFile(username, hash, filename)
    return jsonify(callback.dict())

@projectBlueprint.route('/project/<hash>/<filename>/preview', methods=['GET'])
@loginRequired(cfg.ROLES.STUDENT)
def projectFilePreview(hash, filename):
    username = request.json["user"]["name"]
    pManager = ProjectManager()
    callback = pManager.GeneratePage(username, hash, filename)
    return callback.data

@projectBlueprint.route('/link/<hash>', methods=['GET'])
@loginRequired(cfg.ROLES.STUDENT)
def getShareLink(hash):
    username = request.json["user"]["name"]
    pManager = ProjectManager()
    callback = pManager.GetLinkProject(username, hash)
    return jsonify(callback.dict())

@projectBlueprint.route('/link/<hash>', methods=['PUT'])
@loginRequired(cfg.ROLES.STUDENT)
def createShareLink(hash):
    username = request.json["user"]["name"]
    pManager = ProjectManager()
    callback = pManager.CreateLinkProject(username, hash)
    return jsonify(callback.dict())

@projectBlueprint.route('/link/<hash>', methods=['PATCH'])
@loginRequired(cfg.ROLES.STUDENT)
def useShareLink(hash):
    username = request.json["user"]["name"]
    pManager = ProjectManager()
    callback = pManager.UseLinkProject(username, hash)
    return jsonify(callback.dict())