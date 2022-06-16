from flask import Blueprint, render_template, render_template_string, request, flash, jsonify, redirect, url_for
from flask_login import login_required, current_user
from .models import Note, Picks, Pool, Link, User
from . import db
import json
import random
import string

views = Blueprint('views', __name__)


@views.route('/', methods=['GET', 'POST'])
@login_required
def home():
    if request.method == 'POST':
        note = request.form.get('note')

        if len(note) < 1:
            flash('Note is too short!', category='error')
        else:
            new_note = Note(data=note, user_id=current_user.id)
            db.session.add(new_note)
            db.session.commit()
            flash('Note added!', category='success')
    
    html_string = '{% extends "base.html" %} {% block title %}' \
        'Home{% endblock %} {% block content%}' \
        '<h1 align="center">OsterHoops</h1>'
    html_string += str(current_user.is_admin)
    html_string += '{% endblock %}'

    return render_template_string(html_string, user=current_user)

@views.route('/create-pool', methods=['GET', 'POST'])
@login_required
def create_pool():
    if request.method == 'POST':
        pool_name = request.form.get('poolName')

        if len(pool_name) < 1:
            flash('Pool name must be at least 1 character.', category='error')
        else:
            # Creates a 12 character alphanumeric code uniqe to the pool.
            characters = string.ascii_uppercase + string.digits
            password1 = ''.join(random.choice(characters) for i in range(12))
            
            # Create the pool and add it to the database.
            new_pool = Pool(pool_name=pool_name, password=password1)
            db.session.add(new_pool)
            db.session.commit()
            flash('Pool created!  Share this invite code: ' + password1
                  + '.  Anyone with this code can join your pool.', category='success')
            
            # Add the user that created the pool to it.
            pool_id = db.session.query(Pool.id).filter(Pool.password == password1).first()[0]
            new_link = Link(user_id=current_user.id, pool_id=pool_id)
            db.session.add(new_link)
            db.session.commit()
            
            return redirect(url_for('views.home'))

    return render_template("create_pool.html", user=current_user)

@views.route('/join-pool', methods=['GET', 'POST'])
@login_required
def join_pool():
    if request.method == 'POST':
        pool_password = request.form.get('poolPassword').strip(' ')

        if len(pool_password) != 12:
            flash('Pool password should be 12 characters.', category='error')
        else:
            # TODO: Update this chunk to add user to pool
            pool_id = db.session.query(Pool.id).filter(Pool.password == pool_password).first()[0]
            new_link = Link(user_id=current_user.id, pool_id=pool_id)
            db.session.add(new_link)
            db.session.commit()
            
            return redirect(url_for('views.home'))

    return render_template("join_pool.html", user=current_user)

@views.route('/pools', methods=['GET'])
@login_required
def pools():
    if request.method == 'GET':
        html_string = '{% extends "base.html" %} {% block title %}Pools' \
            '{% endblock %} {% block content%} </br>' \
            '<h1 align="center">Pools</h1></br>' \
            '<ul class="list-group list-group-flush" id="pools">'
        
        # Get a list of pools from the database that the current user is linked to.
        pool_ids = db.session.query(Link.pool_id).filter(Link.user_id == current_user.id)
        for each in pool_ids:
            pool_name = db.session.query(Pool.pool_name).filter(Pool.id == each[0]).first()[0]          
            html_string += '<li class="list-group-item">' + pool_name + '</li>'
        html_string += '</ul>' \
                       '{% endblock %}'

    return render_template_string(html_string, user=current_user)


@views.route('/delete-note', methods=['POST'])
def delete_note():
    note = json.loads(request.data)
    noteId = note['noteId']
    note = Note.query.get(noteId)
    if note:
        if note.user_id == current_user.id:
            db.session.delete(note)
            db.session.commit()

    return jsonify({})
