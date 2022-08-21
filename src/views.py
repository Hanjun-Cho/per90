from flask import Blueprint, render_template, url_for
from flask_login import login_required
from .model import Articles
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
    article = Articles.query.filter_by(directory=directory).first()
    article.views += 1
    db.session.commit()

    return render_template('article.html', content=content, meta=meta, title=article.title, author=article.author)

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