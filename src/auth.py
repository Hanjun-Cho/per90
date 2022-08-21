from flask import Blueprint, render_template, url_for, request, make_response, jsonify, redirect
from flask_login import login_user, logout_user, current_user
from .model import Users, Comments
import os
from . import db
from bcrypt import hashpw, checkpw, gensalt
auth = Blueprint('auth', __name__)

@auth.route('/signup')
def signup():
    if request.args:
        data = request.args.get('data')
        splits = data.split(',')

        email = splits[0]
        username = splits[1]
        password = splits[2]

        if email is None or len(email) == 0:
            res = make_response(jsonify(['error', 'email too short'], 200))
            return res
        elif username is None or len(username) <= 3:
            res = make_response(jsonify(['error', 'username too short (at least 3 characters)'], 200))
            return res
        elif password is None or len(password) < 8:
            res = make_response(jsonify(['error', 'password too short (at 8 characters)'], 200))
            return res

        user = Users.query.filter_by(email=email).first()

        if user is not None:
            res = make_response(jsonify(['error', 'user with email already exists'], 200))
            return res
        else:
            user = Users.query.filter_by(username=username).first()

            if user is not None:
                res = make_response(jsonify(['error', 'username already taken'], 200))
                return res
            else:
                hash = hashpw(password.encode(), gensalt())
                user = Users(email=email, username=username, password=hash)
                login_user(user)
                db.session.add(user)
                db.session.commit()
                res = make_response(jsonify(['success', 'account created successfully'], 200))
                return res
    return res

@auth.route('/login')
def login():
    if request.args:
        data = request.args.get('data')
        splits = data.split(',')

        email = splits[0]
        password = splits[1]

        if email is None or len(email) == 0:
            res = make_response(jsonify(['error', 'email too short'], 200))
            return res
        elif password is None or len(password) < 8:
            res = make_response(jsonify(['error', 'password too short'], 200))
            return res
        
        user = Users.query.filter_by(email=email).first()

        if user is None:
            res = make_response(jsonify(['error', 'email doesnt exist'], 200))
            return res
        elif user is not None:
            if checkpw(password.encode(), user.password):
                login_user(user)
                res = make_response(jsonify(['success', 'logged into account'], 200))
                return res
            else:
                res = make_response(jsonify(['error', 'password is incorrect'], 200))
                return res
    return res

@auth.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('views.home'))

@auth.route('/check_email')
def check_email():
    if request.args:
        email = request.args.get("email")
        user = Users.query.filter_by(email=email).first()

        if user is not None:
            res = make_response(jsonify("exists", 200))
        else:
            res = make_response(jsonify("doesnt exist", 200))
    return res

@auth.route('/save_account')
def save_account():
    if request.args:
        data = request.args.get("data");
        splits = data.split(',')

        email = splits[0]
        username = splits[1]
        password = splits[2]
        password_conf = splits[3]

        print(data)

        if email is None or len(email) == 0:
            res = make_response(jsonify(['error', 'email too short'], 200))
            return res

        user = Users.query.filter_by(email=email).first()

        if email != current_user.email:
            if user is not None:
                res = make_response(jsonify(['error', 'email already taken'], 200))
                return res
            else:
                cur_user = Users.query.filter_by(email=current_user.email).first()
                cur_user.email = email
                db.session.commit()

        if username != current_user.username:
            if username is None or len(username) == 0:
                res = make_response(jsonify(['error', 'username too short (at least 3 characters)'], 200))
                return res

            user = Users.query.filter_by(username=username).first()

            if user is not None:
                res = make_response(jsonify(['error', 'username already taken'], 200))
                return res
            else:
                comments = Comments.query.filter_by(sender=current_user.username).all()
                
                cur_user = Users.query.filter_by(email=current_user.email).first()
                cur_user.username = username
                for i in comments:
                    i.sender = username
                db.session.commit()

        if len(password) == 0:
            res = make_response(jsonify(['success', ''], 200))
            return res
        if password != password_conf:
            res = make_response(jsonify(['error', 'password dont match'], 200))
            return res
        else:
            cur_user = Users.query.filter_by(email=current_user.email).first()
            cur_user.password = hashpw(password, gensalt())
            db.session.commit()
            res = make_response(jsonify(['success', ''], 200))
            return res
    return res

@auth.route('/delete_account')
def delete_account():
    comments = Comments.query.filter_by(sender=current_user.username).all()

    for i in comments:
        i.sender='deleted account'

    user = Users.query.filter_by(email=current_user.email).delete()
    db.session.commit()
    logout_user()
    return redirect(url_for('views.home'))