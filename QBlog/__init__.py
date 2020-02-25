"""
The flask application package.
"""

from flask import Flask

UPLOAD_FOLDER = 'C:/inetpub/wwwroot/your upload folder'

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER # 上传文件路径
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024 # 上传文件限制16M
app.config['JSON_AS_ASCII'] = False # jsonify可包含中文

import QBlog.views
from QBlog.database import init_db

init_db() #创建数据库
