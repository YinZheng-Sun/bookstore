from flask import Blueprint
from flask import request
from flask import jsonify
from be.model import userManager

bp_auth = Blueprint("auth", __name__, url_prefix="/auth")


@bp_auth.route("/login/<string:user_id>/<string:password>/<string:terminal>", methods=["GET"])
def login(user_id,password,terminal):
    # user_id = request.json.get("user_id", "")
    # password = request.json.get("password", "")
    # terminal = request.json.get("terminal", "")
    u = userManager.userManager()
    code, message, token = u.login(user_id=user_id, password=password, terminal=terminal)
    return jsonify({"message": message, "token": token}), code


@bp_auth.route("/logout", methods=["POST"])
def logout():
    user_id: str = request.json.get("user_id")
    token: str = request.headers.get("token")
    u = userManager.userManager()
    code, message = u.logout(user_id=user_id, token=token)
    return jsonify({"message": message}), code


@bp_auth.route("/register/<string:user_id>/<string:password>", methods=["GET"])
def register(user_id,password):
    print("here")
    print(user_id)
    print(password)
    # user_id = request.json.get("user_id", "")
    # password = request.json.get("password", "")
    u = userManager.userManager()
    code, message = u.register(user_id=user_id, password=password)
    return jsonify({"message": message}), code


@bp_auth.route("/unregister/<string:user_id>/<string:password>", methods=["GET"])
def unregister(user_id,password):
    # user_id = request.json.get("user_id", "")
    # password = request.json.get("password", "")
    u = userManager.userManager()
    code, message = u.unregister(user_id=user_id, password=password)
    return jsonify({"message": message}), code


@bp_auth.route("/password/<string:user_id>/<string:old_password>/<string:new_password>", methods=["GET"])
def change_password(user_id,old_password,new_password):
    # user_id = request.json.get("user_id", "")
    # old_password = request.json.get("oldPassword", "")
    # new_password = request.json.get("newPassword", "")
    u = userManager.userManager()
    code, message = u.change_password(user_id=user_id, old_password=old_password, new_password=new_password)
    return jsonify({"message": message}), code
