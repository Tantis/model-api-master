
import os
import random
import time
import requests

from server import db
from datetime import datetime
from server import adminPrmary
from flask import Markup, jsonify, render_template, request
from flask import session


@adminPrmary.route("/login/")
def login():

    return render_template('/login/login.html')

@adminPrmary.route("/")
def index():
    session["User"] = {"user_id": "ly"}
    return jsonify(session["User"])
    


