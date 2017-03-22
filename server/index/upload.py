from server import app
from flask import request
from flask import jsonify
from server import db
from datetime import datetime
import requests
import time
import random

@app.route('/api/image/upload/', methods=['GET', 'POST'])
def uploads():
    """
    上传图片
    """
    current_time = int(time.time())
    try:
        if request.method == 'POST':
            f = request.files
            for item in f.listvalues():
                for value in item:
                    names = value.filename.split('.')[-1]
                    save_file_names = str(
                        int(time.time())) + "_" + str(random.randint(0, 100000)) + '.' + names
                    db.insert("""
                    INSERT INTO `work_image`
                                (
                                `image_url`,
                                `name`,
                                `create_time`)
                    VALUES (
                            :url,
                            :name,
                            :create_time);
                    """, {'create_time': current_time, 'name': value.filename.split('.')[0], 'url': '/static/img/%s' % save_file_names})
                    value.save('server/static/img/%s' % (save_file_names))
            return jsonify({'status': 200, 'data': save_file_names, 'msg': '成功'}), 200
        else:
            return jsonify({'status': 400, 'msg': '失败'}), 400
    except Exception as err:
        print(err)
        return jsonify({'status': 400, 'msg': '失败'}), 400


@app.route('/api/media/upload/', methods=['GET', 'POST'])
def uploadmedia():
    """
    上传视频
    """
    current_time = int(time.time())
    try:
        if request.method == 'POST':
            f = request.files
            for item in f.listvalues():
                for value in item:
                    names = value.filename.split('.')[-1]
                    save_file_names = str(
                        int(time.time())) + "_" + str(random.randint(0, 100000)) + '.' + names
                    db.insert("""
                    INSERT INTO `viedeo_url`
                                (
                                `video_url`,
                                `name`,
                                `create_time`)
                    VALUES (
                            :url,
                            :name,
                            :create_time);
                    """, {'create_time': current_time, 'name': value.filename.split('.')[0], 'url': '/static/video/%s' % save_file_names})
                    value.save('server/static/video/%s' % (save_file_names))
            return jsonify({'status': 200, 'data': save_file_names, 'msg': '成功'}), 200
        else:
            return jsonify({'status': 400, 'msg': '失败'}), 400
    except Exception as err:
        print(err)
        return jsonify({'status': 400, 'msg': '失败'}), 400