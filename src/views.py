from flask import Blueprint, render_template, url_for
import os
views = Blueprint('views', __name__)

@views.route('/<team>/<type>/<name>')
def article(team, type, name):
    print(team + ' ' + type + ' ' + name)

    cpath = os.path.dirname(os.path.realpath(__file__))
    spath = url_for('static', filename='articles/'+team+'/'+type+'/'+name)
    path = cpath + spath + '/article.html'

    f = open(path, 'r')
    content = f.read()
    f.close()

    return render_template('article.html', content=content)