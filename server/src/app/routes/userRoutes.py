from flask import jsonify, request, Blueprint
from app.managers import UserManager
from app.common import Callback
from app.cfg import ConfigInterface as cfg
from app.common.logging import logger
from app.common.auth import loginRequired
import json

userBlueprint = Blueprint('user_blueprint', __name__)

@userBlueprint.route('/user', methods=['GET'])
@loginRequired(cfg.ROLES.STUDENT)
def auth():

    logger.info("Auth(): begin")

    email    = request.json["user"]["mail"]
    username = request.json["user"]["name"]

    mgr = UserManager()
    user = mgr.GetUser(username, email).data
    callback = Callback()
    callback.data = user.role
    logger.debug(callback.dump())
    return jsonify(callback.dict())

@userBlueprint.route('/user', methods=['PUT'])
def register():
    logger.debug("Register user: begin")

    if "user" not in request.json:
        logger.warn("'user' field doesn't exist!")
        return jsonify(Callback(status=1, description="'user' field doesn't exists!").dict())
    
    if "mail" not in request.json["user"] or "name" not in request.json["user"] or "pass" not in request.json["user"]:
        logger.warn("'user' field doesn't have some subfields!")
        return jsonify(Callback(status=2, description="'user' field doesn't have subfields").dict())
    
    email    = request.json["user"]["mail"]
    username = request.json["user"]["name"]
    password = request.json["user"]["pass"]

    usrManager = UserManager()
    callback   = usrManager.AddUser(username, email, password)

    logger.debug("Register user: end")
    return jsonify(callback.dict())

@userBlueprint.route('/user', methods=['PATCH'])
@loginRequired(cfg.ROLES["ADMIN"])
def setUserRole():
    logger.debug("Update user: begin")
    
    if "data" not in request.json:
        logger.warn("'data' field needed")
        return jsonify(Callback(status=1, description="'data' field required").dict())
    data     = request.json["data"]

    username = data["name"]
    newRole  = data["role"]

    usrManager = UserManager()
    callback   = usrManager.SetRole(username, newRole)

    logger.debug("Update user: end")
    return jsonify(callback.dict())

@userBlueprint.route('/user', methods=['DELETE'])
@loginRequired(cfg.ROLES.STUDENT)
def removeUser():
    logger.debug("Remove user: begin")
    
    username = request.json["user"]["name"]

    usrManager = UserManager()
    callback   = usrManager.RemoveUser(username)

    logger.debug("Remove user: end")
    return jsonify(callback.dict())

@userBlueprint.route('/users', methods=['GET'])
@loginRequired(cfg.ROLES.STUDENT)
def userList():
    logger.debug("List users: begin")

    usrManager = UserManager()
    callback   = usrManager.ListUsers()
    
    logger.debug("List users: end")
    return jsonify(callback.dict())

