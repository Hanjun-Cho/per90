from flask import Blueprint, render_template, url_for, request, redirect
from flask_login import login_required, current_user
from .model import Articles, Comments
import os
from . import db
comments = Blueprint('comments', __name__)

@comments.route('/make_comment', methods=['POST'])
@login_required
def make_comment():
    title = request.form.get('title')
    content = request.form.get('content')
    article = Articles.query.filter_by(title=title).first()
    comment = Comments(sender=current_user.username, article=article.directory, content=content)
    db.session.add(comment)

    split = article.directory.split('/')
    type = split[1]
    year = split[2]
    month = split[3]
    day = split[4]
    name = split[5]

    db.session.commit()
    return redirect(url_for('views.comment_article', type=type, year=year, month=month, day=day, title=name))