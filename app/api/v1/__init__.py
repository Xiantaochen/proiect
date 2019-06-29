
from flask import Blueprint
from app.api.v1 import test, user, client, token, verify




def create_blueprint_v1():
    bp_v1 = Blueprint('v1', __name__)
    test.api.register(bp_v1)
    user.api.register(bp_v1)
    client.api.register(bp_v1)
    token.api.register(bp_v1)
    verify.api.register(bp_v1)
    return bp_v1
