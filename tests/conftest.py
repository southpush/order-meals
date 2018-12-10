# -*- coding: utf-8 -*-
import pytest
from webtest import TestApp

from app import create_app
from app import db as _db

# from .factories import UserFactory
from app.models.user import user_personal


@pytest.fixture
def app():
    """An application for the tests."""
    _app = create_app('testing')
    ctx = _app.test_request_context()
    ctx.push()

    yield _app

    ctx.pop()


@pytest.fixture
def testapp(app):
    """A Webtest app."""
    return TestApp(app)


@pytest.fixture
def db(app):
    """A database for the tests."""
    _db.app = app
    with app.app_context():
        _db.create_all()

    yield _db

    # Explicitly close DB connection
    _db.session.close()
    # _db.drop_all()


@pytest.fixture(scope="module")
def user(db):
    """A user for the tests."""
    user = user_personal(password='myprecious', nickname="w45", head_img=0, openid="2525", phone="34698")
    db.session.commit()
    return user
