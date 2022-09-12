from flask import Blueprint, render_template, url_for, redirect
from flask_login import current_user
from .model import Articles, Comments
import os
from . import db
views = Blueprint('views', __name__)

@views.route('/')
def home():
    articles = Articles.query.all()
    return render_template('home.html', articles=articles)

@views.route('/analysis')
def analysis_tab():
    articles = Articles.query.filter_by(type='analysis').all()
    return render_template('home.html', articles=articles)

@views.route('/opinions')
def opinions_tab():
    articles = Articles.query.filter_by(type='opinions').all()
    return render_template('home.html', articles=articles)

@views.route('/profile')
def profile():
    if not current_user.is_authenticated:
        return redirect(url_for('views.home'))
    return render_template('profile.html')

@views.route('/<type>/<year>/<month>/<day>/<title>')
def opinion_article(type, year, month, day, title):
    return load_article('/'+type+'/'+year+'/'+month+'/'+day+'/'+title, False)

@views.route('/<type>/<subtype>/<year>/<month>/<day>/<title>')
def analysis_article(type, subtype, year, month, day, title):
    return load_article('/'+type+'/'+subtype+'/'+year+'/'+month+'/'+day+'/'+title, False)

def load_article(directory, comments_tf):
    cpath = os.path.dirname(os.path.realpath(__file__))
    spath = url_for('static', filename='articles/'+directory)
    path = cpath + spath + '/article.html'

    f = open(path, 'r')
    content = f.read()
    f.close()

    path = cpath + spath + '/meta.html'
    f = open(path, 'r')
    meta = f.read()
    f.close()

    article = Articles.query.filter_by(directory=directory).first()
    ret = get_comments(article.key)
    comments = ret[0]
    comments_dict = ret[1]
    depth = ret[2]
    article.views += 1
    db.session.commit()
    return render_template('article.html', content=content, meta=meta, title=article.title, 
    author=article.author, commented=comments_tf, comments=comments, comments_dict=comments_dict, depth=depth)

def get_comments(key):
    comments = Comments.query.filter_by(article=key).all()

    if len(comments) == 0:
        return [[], {}, {}]
    comments_dict = {}
    d = {}
    ret = []
    v = set()

    for i in comments[::-1]:
        if len(i.parent) == 0:
            dfs_comments(i.key, v, ret, comments_dict, 0, d)
    return [ret,comments_dict, d]

def dfs_comments(key, v, ret, comments_dict, depth, d):
    if(key in v):
        return 
    ret.append(Comments.query.filter_by(key=key).first())
    comments_dict[str(key)] = Comments.query.filter_by(key=key).first()
    d[str(key)] = min(6, depth)

    comments = Comments.query.filter_by(parent=key).all()

    for i in comments:
        dfs_comments(i.key, v, ret, comments_dict, depth+1, d)
    
    return ret