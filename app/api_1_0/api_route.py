# -*- coding: utf-8 -*-
from flask_restful import Api
from app.api_1_0 import api_1_0
from .api_user import getUser

api_user = Api(api_1_0)

api_user.add_resource(getUser, '/getuser', )
