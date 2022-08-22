from flask import Blueprint, render_template, url_for, request, redirect
from flask_login import login_required, current_user
from .model import Articles, Comments
import os
from . import db
backend = Blueprint('backend', __name__)

@backend.route('/add_article', methods=['GET', 'POST'])
def add_article():
    if current_user.username == "1rrelevant":
        if request.method == 'POST':
            title = request.form.get('title')
            type = request.form.get('type')
            subtype = request.form.get('subtype')
            description = request.form.get('description')
            author = request.form.get('author')
            year = request.form.get('year')
            month = request.form.get('month')
            day = request.form.get('day')
            url_title = request.form.get('url_title')

            if type == 'opinions':
                cpath = os.path.dirname(os.path.realpath(__file__))
                directory = '/'+type+'/'+year+'/'+month+'/'+day+'/'+url_title
                spath = url_for('static', filename='articles/'+directory)
                if os.path.exists(cpath+spath) != True:
                    os.makedirs(cpath+spath)

                article = Articles(title=title, type=type, description=description, author=author, directory=directory, views=0)
                db.session.add(article)
                db.session.commit()
            else:
                cpath = os.path.dirname(os.path.realpath(__file__))
                directory = '/'+type+'/'+subtype+'/'+year+'/'+month+'/'+day+'/'+url_title
                spath = url_for('static', filename='articles/'+directory)
                if os.path.exists(cpath+spath) != True:
                    os.makedirs(cpath+spath)

                article = Articles(title=title, type=type, description=description, author=author, directory=directory, views=0)
                db.session.add(article)
                db.session.commit()
        return render_template('add_article.html')
    return redirect(url_for('views.home'))