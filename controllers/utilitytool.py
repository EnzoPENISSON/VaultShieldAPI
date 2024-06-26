import string
import uuid
import random

from flask import jsonify

from .UserController import UserController

class UtilityTool:
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

    def longUUIDGenerator(self):
        uu1 = str(uuid.uuid4())
        uu2 = str(uuid.uuid4())
        return uu1+"-"+uu2

    def split_and_convert_two_uuids(self, combined_uuid):
        # Split the combined UUID string
        parts = combined_uuid.split('-')

        if len(parts) != 10:
            raise ValueError('badly formed combined UUID string')

        # Reassemble the parts into two valid UUID strings
        uuid_str1 = '-'.join(parts[:5])
        uuid_str2 = '-'.join(parts[5:])

        # Convert strings to UUID objects
        uuid_obj1 = uuid.UUID(uuid_str1)
        uuid_obj2 = uuid.UUID(uuid_str2)

        return uuid_obj1, uuid_obj2

    def generate_otp(self):
        """Generate a 6-digit OTP"""
        digits = string.digits
        otp = ''.join(random.choice(digits) for _ in range(8))
        return otp

    def generate_random_string(self):
        # Generate a random number of elements between 1 and 10
        num_elements = random.randint(10, 15)

        # Create a list of random lowercase letters
        elements = ["•" for _ in range(num_elements)]

        # Join the elements with a period
        result = "".join(elements)

        return result