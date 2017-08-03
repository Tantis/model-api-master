import os
import random
import time
from datetime import datetime

import requests
from flask import Markup, jsonify, render_template, request

from server import app, db
from server.utils.handler import _parent_resoves



@app.route("/")
@app.route("/index/")
def company_index():
    

    # 查询MENU
    menu_data = _parent_resoves()
    
    logo_img  = "http://web.liuyu.info//static/img/1494337395_83468.png"

    return render_template('index.html', menu=menu_data, logo = logo_img)
