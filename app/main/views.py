# -*- coding: utf-8 -*-
import os
from datetime import datetime
from flask import render_template, session, redirect, url_for

from . import main


@main.route("/", methods=["GET", "POST"])
def index():
    env = os.environ.get("DEV_DATABASE_URL")
    return render_template("index.html", env=env)



