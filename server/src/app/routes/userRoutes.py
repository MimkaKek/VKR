from flask import jsonify, request, Blueprint
from flask_cors import cross_origin

from app.managers import UserManager
from app.common import Callback
from app.cfg import ConfigInterface as cfg
from app.common.logging import logger
from app.common.auth import loginRequired
import json

userBlueprint = Blueprint('user_blueprint', __name__)

@userBlueprint.route('/user', methods=['POST'])
@cross_origin()
def auth():
    logger.info("Auth(): begin")
    logger.debug(request.args)
    email    = request.args.get("mail", None)
    username = request.args.get("name", None)
    password = request.args.get("pass", "")

    mgr = UserManager()
    logger.debug("Params auth: {mail} | {name} | {passwd}".format(mail=email, name=username, passwd=password))
    userStatus = mgr.GetUser(username, email)
    if userStatus.status != 0:
        return jsonify(userStatus.dict())
    user = userStatus.data

    authStatus = mgr.ValidateUser(user, password)
    if authStatus.status != 0:
        return jsonify(authStatus.dict())
    
    sidStatus = mgr.CreateSID(user)
    if sidStatus.status != 0:
        return jsonify(authStatus.dict())

    logger.debug("New SID {sid} for user {name} with role {role}".format(sid=user.sid, name=user.username, role=user.role))

    callback = Callback(data={"sid": user.sid, "role": user.role})
    return jsonify(callback.dict())

@userBlueprint.route('/user', methods=['PUT'])
@cross_origin()
def register():
    logger.debug("Register user: begin")

    username = request.args.get('name')
    email    = request.args.get('mail')
    password = request.args.get('pass')

    if username is None or email is None or password is None:
        return jsonify(Callback(status=1, description="Some fields required!").dict())
    
    usrManager = UserManager()
    callback   = usrManager.AddUser(username, email, password)

    logger.debug("Register user: end")
    return jsonify(callback.dict())

@userBlueprint.route('/user', methods=['PATCH'])
@cross_origin()
@loginRequired(cfg.ROLES.ADMIN)
def setUserRole():
    logger.debug("Update user: begin")
    
    if "data" not in request.json:
        logger.warn("'data' field needed")
        return jsonify(Callback(status=1, description="'data' field required").dict())
    data     = request.json["data"]

    username = data["name"]
    newRole  = data["role"]

    logger.debug("CHECK BEGIN")
    logger.debug(data)
    logger.debug(username)
    logger.debug(newRole)
    logger.debug("CHECK END")

    usrManager = UserManager()
    userStatus = usrManager.GetUser(username=username)
    if userStatus.status != 0:
        userStatus.data = None
        return jsonify(userStatus.dict())
    
    user       = userStatus.data
    callback   = usrManager.SetRole(user, newRole)

    logger.debug("Update user: end")
    return jsonify(callback.dict())

@userBlueprint.route('/user', methods=['DELETE'])
@cross_origin()
@loginRequired(cfg.ROLES.STUDENT)
def removeUser():
    logger.debug("Remove user: begin")
    
    sid = request.args.get('sid')

    usrManager = UserManager()

    userStatus = usrManager.GetUser(sid=sid)
    user       = userStatus.data

    callback   = usrManager.RemoveUser(user)

    logger.debug("Remove user: end")
    return jsonify(callback.dict())

@userBlueprint.route('/users', methods=['GET'])
@cross_origin()
@loginRequired(cfg.ROLES.STUDENT)
def userList():
    logger.debug("List users: begin")

    usrManager = UserManager()
    callback   = usrManager.ListUsers()
    
    logger.debug("List users: end")
    return jsonify(callback.dict())

