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

    return render_template("home.html", user=current_user)

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

@views.route('/pools', methods=['GET'])
@login_required
def pools():
    if request.method == 'GET':
        html_string = '{% extends "base.html" %} {% block title %}Pools' \
            '{% endblock %} {% block content%} </br>' \
            '<h1 align="center">Pools</h1></br>' \
            '<ul class="list-group list-group-flush" id="pools">'
        
        # Get a list of pools from the database.
        pools_list = db.session.query(Pool)
        for each in pools_list:
            html_string += '<li class="list-group-item">' + each.pool_name + '</li>'
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
