from flask import jsonify

from .UserController import UserController

class Tools:
    def userExist(self, email, data):

        utilisateur = UserController()

        userId = utilisateur.getUserUUID(email)

        if not userId:
            return jsonify({"status": "failed", "message": "User not found"})
        if data["userUUid"] != userId:
            return jsonify({"status": "failed", "message": "Invalid user"})
        return None

    def getUserUUID(self, email):
        utilisateur = UserController()
        userId = utilisateur.getUserUUID(email)
        return userId