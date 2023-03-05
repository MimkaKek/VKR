from flask import jsonify, request, Blueprint
from app.managers import UserManager
from app.common import Callback
from app.common.logging import logger
from app.common.auth import loginRequired
import json

userBlueprint = Blueprint('user_blueprint', __name__)

@userBlueprint.route('/user', methods=['GET'])
def authenticate():
    logger.debug("Auth user: begin")
    usrManager = UserManager()
    callback   = usrManager.ValidateUser()
    logger.debug("Auth user: end")
    return jsonify(callback.dump())

@userBlueprint.route('/user', methods=['PUT'])
def register():
    logger.debug("Register user: begin")
    usrManager = UserManager()
    callback   = usrManager.AddUser()
    logger.debug("Register user: end")
    return jsonify(callback.dump())

@userBlueprint.route('/user', methods=['DELETE'])
@loginRequired()
def removeUser():
    logger.debug("Remove user: begin")
    usrManager = UserManager()
    callback   = usrManager.RemoveUser()
    logger.debug("Remove user: end")
    return jsonify(callback.dump())

@userBlueprint.route('/users', methods=['GET'])
@loginRequired()
def userList():
    logger.debug("List users: begin")
    usrManager = UserManager()
    callback   = usrManager.ListUsers()
    logger.debug("List users: end")
    return jsonify(callback.dump())

