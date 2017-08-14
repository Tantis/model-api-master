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

    treeResult = db.query("SELECT * FROM category_directions_items WHERE category_direction_id = 2;")
    if not treeResult:
        pass
    logoPng = db.query("SELECT * FROM category_directions_items WHERE category_direction_id = 2;")
    logoPng = {i["name"]: i["value"] for i in logoPng}
    


    return render_template('index.html', menu=treeResult, logo=logoPng)
