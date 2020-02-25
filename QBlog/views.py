"""
Routes and views for the flask application.
"""

from datetime import datetime
from sqlalchemy import func
from sqlalchemy import sql
from QBlog.database import db_session
from QBlog.models import Article, Querytojson
from werkzeug.utils import secure_filename
from flask import send_from_directory
from flask import render_template
from flask import jsonify
from flask import request
from QBlog import app
import html
import json
import os

@app.route('/',methods=["GET"])
@app.route('/home',methods=["GET","POST"])
def home():
    """Renders the home page.
       POST: return json data for article list
       GET: return index.html include article sum and top5 article list
    """
    count = db_session.query(func.count(Article.Id)).scalar() # select count(Article.Id) from t_article
    #count = db_session.query(func.count(Article.Id)).filter(sql.text(where)).params(dict).scalar()
    if request.method == 'POST':
        data = request.json
        if 'curr' in data:
            card = db_session.query(Article.Id, Article.Title, Article.Up_time).filter().limit(5).offset((int(data['curr'])-1)*5)
            jsonData_list = Querytojson(card)
            if len(jsonData_list) > 0:
                return jsonify(jsonData_list)
    else:
        card = db_session.query(Article.Id, Article.Title, Article.Up_time).filter().limit(5)
        return render_template(
            'index.html',
            year=datetime.now().year,
            count=int(count),
            cards=card
        )

@app.route('/about')
def about():
    """Renders the about page."""
    return render_template(
        'about.html',
        title='About',
        year=datetime.now().year
    )

@app.route('/article/<int:post_id>')
def article(post_id=1):
    """Renders the contact page."""
    count = db_session.query(func.count(Article.Id)).scalar()
    article = Article.query.filter(Article.Id == post_id).first() #different with db_session.query().filter()
    #print(article)
    url = 'https://habit.xiangyundiaocha.club/article/' + str(post_id)
    return render_template(
        'article.html',
        cards=article,
        url=url,
        count=int(count)
    )

@app.route('/search', methods=["POST"])
def search():
    """Renders the test page."""
    if request.method == 'POST':
        search = request.form.to_dict()
        serach_data = 'nothing'
        if 's' in search:
            serach_data = str(search['s'])
            result = db_session.query(Article.Id, Article.Title, Article.Up_time).filter(Article.Content.like("%"+serach_data+"%")).all()
            if len(result) > 0:
                jsonData_list = Querytojson(result)
                return render_template(
                    'search.html',
                    name=serach_data,
                    year=datetime.now().year,
                    ifdata=True,
                    cards=jsonData_list
                )
            else:
                return render_template(
                'search.html',
                name=serach_data,
                year=datetime.now().year,
                ifdata=False
            )
        else:
            return render_template(
                'search.html',
                name=serach_data,
                year=datetime.now().year,
                ifdata=False
            )


@app.route('/test')
def test():
    """Renders the test page."""
    return render_template(
        'test.html',
        title='Test',
        year=datetime.now().year
    )

@app.route('/api', methods=['GET','POST'])
def api():
    if request.method == 'POST':
        cards = [{'article_title':u"计算机视觉（一）RCNN"},
                 {'article_title':u"计算机视觉（二）Fast-RCNN"}
                ]
        return jsonify(cards),200
    else:
        return render_template(
        'api.html',
        title='API',
        year=datetime.now().year
    )

ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/upload',methods=["POST"])
def upload_file():
    """Renders the upload page."""
    result = {"code": 1,"msg": "fail"}
    if request.method == 'POST':
        if 'file' not in request.files:
            return result
        file = request.files['file']
        # if user does not select file, browser also
        # submit an empty part without filename
        if file.filename == '':
            return result
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename).replace('\\','/')) # windows:/app/uploads\\1.txt
            result ={"code": 0  # 0:success, other:fail
                     ,"msg": "success" # message for fail warn
                     ,"data": {
                         "src": 'your picture upload URL'+ filename
                         ,"title": filename
                         }
                     }
        return result
    else:
        return result

@app.errorhandler(404)
def page_not_found(error):
    return render_template('404.html'), 404

@app.teardown_appcontext
def shutdown_session(exception=None):
    db_session.remove()

