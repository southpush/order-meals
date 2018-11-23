# -*- coding: utf-8 -*-
from .. import db
from ..models.User import User


def addUser(name):
    user = User(name=name)
    db.session.add(user)
    db.session.commit()

