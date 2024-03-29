from flask import jsonify, request, Blueprint
from flask_cors import cross_origin

from app.managers import ProjectManager, UserManager
from app.common import Callback, ProjectData
from app.common.auth import loginRequired
from app.common.logging import logger
from app.cfg import ConfigInterface as cfg

projectBlueprint = Blueprint('project_blueprint', __name__)

@projectBlueprint.route('/templates_all', methods=['GET'])
@cross_origin()
@loginRequired(cfg.ROLES.STUDENT)
def templatesAllList():
    try:
        pManager = ProjectManager()
        callback = pManager.GetTemplatesWithNames()
        return jsonify(callback.dict())
    except Exception as e:
        logger.error("Caught exception at {endpoint}".format(endpoint=request.endpoint))
        logger.exception(e)
        return jsonify(Callback(100, "Unexpected error").dict())

@projectBlueprint.route('/templates', methods=['GET'])
@cross_origin()
@loginRequired(cfg.ROLES.TEACHER)
def templatesList():
    try:
        sid = request.args.get('sid', None)

        uManager = UserManager()
        pManager = ProjectManager()

        user     = uManager.GetUser(sid=sid).data
        username = user.username

        callback = pManager.GetUserProjects(username, isTemplate=True)
        return jsonify(callback.dict())
    except Exception as e:
        logger.error("Caught exception at {endpoint}".format(endpoint=request.endpoint))
        logger.exception(e)
        return jsonify(Callback(100, "Unexpected error").dict())

@projectBlueprint.route('/public_projects', methods=['GET'])
@cross_origin()
@loginRequired(cfg.ROLES.STUDENT)
def publicProjects():
    try:
        pManager = ProjectManager()
        callback = pManager.GetAllProjects()
        return jsonify(callback.dict())
    except Exception as e:
        logger.error("Caught exception at {endpoint}".format(endpoint=request.endpoint))
        logger.exception(e)
        return jsonify(Callback(100, "Unexpected error").dict())

@projectBlueprint.route('/projects', methods=['GET'])
@cross_origin()
@loginRequired(cfg.ROLES.STUDENT)
def projectsList():
    try:
        sid = request.args.get('sid', None)

        uManager = UserManager()
        pManager = ProjectManager()

        user     = uManager.GetUser(sid=sid).data
        username = user.username

        callback = pManager.GetUserProjects(username)
        return jsonify(callback.dict())
    except Exception as e:
        logger.error("Caught exception at {endpoint}".format(endpoint=request.endpoint))
        logger.exception(e)
        return jsonify(Callback(100, "Unexpected error").dict())

@projectBlueprint.route('/projects', methods=['PUT'])
@cross_origin()
@loginRequired(cfg.ROLES.STUDENT)
def projectsCreate():
    try:
        sid = request.args.get('sid', None)

        uManager = UserManager()
        pManager = ProjectManager()

        user     = uManager.GetUser(sid=sid).data
        username = user.username
        
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

        callback = pManager.CreateProject(username, meta, templateID)
        return jsonify(callback.dict())
    except Exception as e:
        logger.error("Caught exception at {endpoint}".format(endpoint=request.endpoint))
        logger.exception(e)
        return jsonify(Callback(100, "Unexpected error").dict())

@projectBlueprint.route('/project/<hash>', methods=['GET'])
@cross_origin()
@loginRequired(cfg.ROLES.STUDENT)
def projectGet(hash):
    try:
        sid = request.args.get('sid', None)

        uManager = UserManager()
        pManager = ProjectManager()

        user     = uManager.GetUser(sid=sid).data
        username = user.username
        
        callback = pManager.GetProject(username, hash)
        return jsonify(callback.dict())
    except Exception as e:
        logger.error("Caught exception at {endpoint}".format(endpoint=request.endpoint))
        logger.exception(e)
        return jsonify(Callback(100, "Unexpected error").dict())

@projectBlueprint.route('/project/<hash>', methods=['PATCH'])
@cross_origin()
@loginRequired(cfg.ROLES.STUDENT)
def projectUpdate(hash):
    try:
        sid = request.args.get('sid', None)

        uManager = UserManager()
        pManager = ProjectManager()

        user     = uManager.GetUser(sid=sid).data
        username = user.username
        
        if "data" not in request.json:
            logger.warn("'data' field needed")
            return jsonify(Callback(status=1, description="'data' field required").dict())
        data = request.json["data"]

        if "isTemplate" in data:
            roleStatus = uManager.GetRole(user)
            if roleStatus.status != 0:
                return jsonify(roleStatus.dict())
            role = roleStatus.data

            if role == cfg.ROLES.STUDENT:
                logger.warn("Attempt to change some specific meta for project {pid} by user {name}".format(pid=hash, name=username))
                data.pop("isTemplate")

        pManager = ProjectManager()
        callback = pManager.SetProjectMeta(username, hash, data)
        return jsonify(callback.dict())
    except Exception as e:
        logger.error("Caught exception at {endpoint}".format(endpoint=request.endpoint))
        logger.exception(e)
        return jsonify(Callback(100, "Unexpected error").dict())

@projectBlueprint.route('/project/<hash>', methods=['DELETE'])
@cross_origin()
@loginRequired(cfg.ROLES.STUDENT)
def projectRemove(hash):
    try:
        sid = request.args.get('sid', None)

        uManager = UserManager()
        pManager = ProjectManager()

        user     = uManager.GetUser(sid=sid).data
        username = user.username
        
        callback = pManager.RemoveProject(username, hash)
        logger.debug(jsonify(callback.dict()))
        return jsonify(callback.dict())
    except Exception as e:
        logger.error("Caught exception at {endpoint}".format(endpoint=request.endpoint))
        logger.exception(e)
        return jsonify(Callback(100, "Unexpected error").dict())

@projectBlueprint.route('/project/<hash>', methods=['POST'])
@cross_origin()
@loginRequired(cfg.ROLES.STUDENT)
def projectCopy(hash):
    try:
        sid = request.args.get('sid', None)

        uManager = UserManager()
        pManager = ProjectManager()

        user     = uManager.GetUser(sid=sid).data
        username = user.username

        callback = pManager.CopyProject(username, hash)
        return jsonify(callback.dict())
    except Exception as e:
        logger.error("Caught exception at {endpoint}".format(endpoint=request.endpoint))
        logger.exception(e)
        return jsonify(Callback(100, "Unexpected error").dict())

@projectBlueprint.route('/project/<hash>/<filename>', methods=['GET'])
@cross_origin()
@loginRequired(cfg.ROLES.STUDENT)
def projectFileGet(hash, filename):
    try:
        sid = request.args.get('sid', None)

        uManager = UserManager()
        pManager = ProjectManager()

        user     = uManager.GetUser(sid=sid).data
        username = user.username
        
        callback = pManager.GetFileProject(username, hash, filename)
        return jsonify(callback.dict())
    except Exception as e:
        logger.error("Caught exception at {endpoint}".format(endpoint=request.endpoint))
        logger.exception(e)
        return jsonify(Callback(100, "Unexpected error").dict())

@projectBlueprint.route('/project/<hash>/<filename>', methods=['PATCH'])
@cross_origin()
@loginRequired(cfg.ROLES.STUDENT)
def projectFileSet(hash, filename):
    try:
        sid = request.args.get('sid', None)

        uManager = UserManager()
        pManager = ProjectManager()

        user     = uManager.GetUser(sid=sid).data
        username = user.username
        
        if "data" not in request.json:
            logger.warn("'data' field needed")
            return jsonify(Callback(status=1, description="'data' field required").dict())
        data     = request.json["data"]
        
        callback = pManager.SetFileProject(username, hash, filename, data)
        return jsonify(callback.dict())
    except Exception as e:
        logger.error("Caught exception at {endpoint}".format(endpoint=request.endpoint))
        logger.exception(e)
        return jsonify(Callback(100, "Unexpected error").dict())

@projectBlueprint.route('/project/<hash>/<filename>', methods=['DELETE'])
@cross_origin()
@loginRequired(cfg.ROLES.STUDENT)
def projectFileDelete(hash, filename):
    try:
        sid = request.args.get('sid', None)

        uManager = UserManager()
        pManager = ProjectManager()

        user     = uManager.GetUser(sid=sid).data
        username = user.username
        
        callback = pManager.RemoveProjectFile(username, hash, filename)
        return jsonify(callback.dict())
    except Exception as e:
        logger.error("Caught exception at {endpoint}".format(endpoint=request.endpoint))
        logger.exception(e)
        return jsonify(Callback(100, "Unexpected error").dict())

@projectBlueprint.route('/project/<hash>/<filename>', methods=['PUT'])
@cross_origin()
@loginRequired(cfg.ROLES.STUDENT)
def projectFileCreate(hash, filename):
    try:
        sid = request.args.get('sid', None)

        uManager = UserManager()
        pManager = ProjectManager()
        logger.debug("CHECK 2")
        user     = uManager.GetUser(sid=sid).data
        username = user.username
        
        callback = pManager.CreateProjectFile(username, hash, filename)
        return jsonify(callback.dict())
    except Exception as e:
        logger.error("Caught exception at {endpoint}".format(endpoint=request.endpoint))
        logger.exception(e)
        return jsonify(Callback(100, "Unexpected error").dict())

@projectBlueprint.route('/project/<hash>/<filename>/preview', methods=['GET'])
@cross_origin()
def projectFilePreview(hash, filename):
    try:
        pManager = ProjectManager()
        callback = pManager.GeneratePageAnon(hash, filename)
        return callback.data
    except Exception as e:
        logger.error("Caught exception at {endpoint}".format(endpoint=request.endpoint))
        logger.exception(e)
        return jsonify(Callback(100, "Unexpected error").dict())

@projectBlueprint.route('/link/<hash>', methods=['GET'])
@cross_origin()
@loginRequired(cfg.ROLES.STUDENT)
def getShareLink(hash):
    try:
        sid = request.args.get('sid', None)

        uManager = UserManager()
        pManager = ProjectManager()

        user     = uManager.GetUser(sid=sid).data
        username = user.username
        
        callback = pManager.GetLinkProject(username, hash)
        return jsonify(callback.dict())
    except Exception as e:
        logger.error("Caught exception at {endpoint}".format(endpoint=request.endpoint))
        logger.exception(e)
        return jsonify(Callback(100, "Unexpected error").dict())

@projectBlueprint.route('/link/<hash>', methods=['PUT'])
@cross_origin()
@loginRequired(cfg.ROLES.STUDENT)
def createShareLink(hash):
    try:
        sid = request.args.get('sid', None)

        uManager = UserManager()
        pManager = ProjectManager()

        user     = uManager.GetUser(sid=sid).data
        username = user.username
        
        callback = pManager.CreateLinkProject(username, hash)
        return jsonify(callback.dict())
    except Exception as e:
        logger.error("Caught exception at {endpoint}".format(endpoint=request.endpoint))
        logger.exception(e)
        return jsonify(Callback(100, "Unexpected error").dict())

@projectBlueprint.route('/link/<hash>', methods=['PATCH'])
@cross_origin()
@loginRequired(cfg.ROLES.STUDENT)
def useShareLink(hash):
    try:
        sid = request.args.get('sid', None)

        uManager = UserManager()
        pManager = ProjectManager()

        user     = uManager.GetUser(sid=sid).data
        username = user.username
        
        callback = pManager.UseLinkProject(username, hash)
        return jsonify(callback.dict())
    except Exception as e:
        logger.error("Caught exception at {endpoint}".format(endpoint=request.endpoint))
        logger.exception(e)
        return jsonify(Callback(100, "Unexpected error").dict())

@projectBlueprint.route('/test_prev', methods=['GET'])
def test_prev():
    try:
        pManager = ProjectManager()
        callback = pManager.GeneratePage("admin", "829351a9fef841ce801fe2f026bec878", "main.html")
        return callback.data
    except Exception as e:
        logger.error("Caught exception at {endpoint}".format(endpoint=request.endpoint))
        logger.exception(e)
        return jsonify(Callback(100, "Unexpected error").dict())