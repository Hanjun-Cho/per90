from flask import Blueprint, render_template, url_for
from flask_login import login_required
from .model import Articles, Comments
import os
from . import db
views = Blueprint('views', __name__)

@views.route('/')
def home():
    articles = Articles.query.all()
    return render_template('home.html', articles=articles)

@views.route('/<type>/<year>/<month>/<day>/<title>')
def article(type, year, month, day, title):
    cpath = os.path.dirname(os.path.realpath(__file__))
    spath = url_for('static', filename='articles/'+type+'/'+year+'/'+month+'/'+day+'/'+title)
    path = cpath + spath + '/article.html'

    f = open(path, 'r')
    content = f.read()
    f.close()

    path = cpath + spath + '/meta.html'
    f = open(path, 'r')
    meta = f.read()
    f.close()

    directory = '/'+type+'/'+year+'/'+month+'/'+day+'/'+title
    ret = get_comments(directory)
    comments = ret[0]
    comments_dict = ret[1]
    depth = ret[2]
    article = Articles.query.filter_by(directory=directory).first()
    article.views += 1
    db.session.commit()
    return render_template('article.html', content=content, meta=meta, title=article.title, 
    author=article.author, commented=False, comments=comments, comments_dict=comments_dict
    , depth=depth)

@views.route('/<type>/<year>/<month>/<day>/<title>#comments')
def comment_article(type, year, month, day, title):
    cpath = os.path.dirname(os.path.realpath(__file__))
    spath = url_for('static', filename='articles/'+type+'/'+year+'/'+month+'/'+day+'/'+title)
    path = cpath + spath + '/article.html'

    f = open(path, 'r')
    content = f.read()
    f.close()

    path = cpath + spath + '/meta.html'
    f = open(path, 'r')
    meta = f.read()
    f.close()

    directory = '/'+type+'/'+year+'/'+month+'/'+day+'/'+title
    ret = get_comments(directory)
    comments = ret[0]
    comments_dict = ret[1]
    depth = ret[2]
    article = Articles.query.filter_by(directory=directory).first()
    article.views += 1
    db.session.commit()
    return render_template('article.html', content=content, meta=meta, title=article.title,
    author=article.author, commented=True, comments=comments, comments_dict=comments_dict
    , depth=depth)

def get_comments(directory):
    comments = Comments.query.filter_by(article=directory).all()
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
    d[str(key)] = depth

    comments = Comments.query.filter_by(parent=key).all()

    for i in comments:
        dfs_comments(i.key, v, ret, comments_dict, depth+1, d)
    
    return ret

@views.route('/player-analysis')
def player_analysis():
    articles = Articles.query.filter_by(type='player-analysis').all()
    return render_template('home.html', articles=articles)

@views.route('/match-analysis')
def match_analysis():
    articles = Articles.query.all()
    return render_template('home.html', articles=articles)

@views.route('/profile')
@login_required
def profile():
    return render_template('profile.html')