import random
import string

from flask import jsonify


class ControllerClass:
    @staticmethod
    def parametersissetPOST(parameters, datajson):
        for parameter in parameters:
            if parameter not in datajson:
                return False
        return True

