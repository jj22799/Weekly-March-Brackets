from flask import Blueprint, render_template, render_template_string, request, flash, jsonify, redirect, url_for
from flask_login import login_required, current_user
from .models import Note, Picks, Matchup, User, Pool, Link
from . import db
import json
import random
import string
from datetime import date

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


@views.route('/make-admin', methods=['GET', 'POST'])
@login_required
def make_admin():
    if request.method == 'POST':
        user_email = request.form.get('userEmail')
        
        if request.form.get('giveAdminAccess') == 'True':
            give_admin_access = True
        else:
            give_admin_access = False

        user = db.session.query(User).filter(User.email == user_email).first()
        user.is_admin = give_admin_access
        db.session.add(user)
        db.session.commit()
            
        return redirect(url_for('views.home'))
    
    # TODO: This needs to say - if current_user.is_admin:
    if True:
        return render_template("make_admin.html", user=current_user)
    else:
        html_string = '{% extends "base.html" %} {% block title %}Pools' \
            '{% endblock %} {% block content%} </br>' \
            '<h1 align="center">Make Admin</h1></br>' \
            'Access denied.  Admin access required.' \
            '{% endblock %}'
        return render_template_string(html_string, user=current_user)


@views.route('/admin', methods=['GET'])
@login_required
def admin():
    if current_user.is_admin:
        return render_template("admin.html", user=current_user)
    else:
        html_string = '{% extends "base.html" %} {% block title %}Pools' \
            '{% endblock %} {% block content%} </br>' \
            '<h1 align="center">Admin</h1></br>' \
            'Access denied.  Admin access required.' \
            '{% endblock %}'
        return render_template_string(html_string, user=current_user)


@views.route('/admin/enter_teams', methods=['GET', 'POST'])
@login_required
def enter_teams():
    if request.method == 'POST':
        # Get the teams entered from the form.
        team_name1 = request.form.get('teamName1')
        team_name2 = request.form.get('teamName2')
        team_name3 = request.form.get('teamName3')
        team_name4 = request.form.get('teamName4')
        team_name5 = request.form.get('teamName5')
        team_name6 = request.form.get('teamName6')
        team_name7 = request.form.get('teamName7')
        team_name8 = request.form.get('teamName8')
        team_name9 = request.form.get('teamName9')
        team_name10 = request.form.get('teamName10')
        team_name11 = request.form.get('teamName11')
        team_name12 = request.form.get('teamName12')
        team_name13 = request.form.get('teamName13')
        team_name14 = request.form.get('teamName14')
        team_name15 = request.form.get('teamName15')
        team_name16 = request.form.get('teamName16')
        team_name17 = request.form.get('teamName17')
        team_name18 = request.form.get('teamName18')
        team_name19 = request.form.get('teamName19')
        team_name20 = request.form.get('teamName20')
        team_name21 = request.form.get('teamName21')
        team_name22 = request.form.get('teamName22')
        team_name23 = request.form.get('teamName23')
        team_name24 = request.form.get('teamName24')
        team_name25 = request.form.get('teamName25')
        team_name26 = request.form.get('teamName26')
        team_name27 = request.form.get('teamName27')
        team_name28 = request.form.get('teamName28')
        team_name29 = request.form.get('teamName29')
        team_name30 = request.form.get('teamName30')
        team_name31 = request.form.get('teamName31')
        team_name32 = request.form.get('teamName32')
        team_name33 = request.form.get('teamName33')
        team_name34 = request.form.get('teamName34')
        team_name35 = request.form.get('teamName35')
        team_name36 = request.form.get('teamName36')
        team_name37 = request.form.get('teamName37')
        team_name38 = request.form.get('teamName38')
        team_name39 = request.form.get('teamName39')
        team_name40 = request.form.get('teamName40')
        team_name41 = request.form.get('teamName41')
        team_name42 = request.form.get('teamName42')
        team_name43 = request.form.get('teamName43')
        team_name44 = request.form.get('teamName44')
        team_name45 = request.form.get('teamName45')
        team_name46 = request.form.get('teamName46')
        team_name47 = request.form.get('teamName47')
        team_name48 = request.form.get('teamName48')
        team_name49 = request.form.get('teamName49')
        team_name50 = request.form.get('teamName50')
        team_name51 = request.form.get('teamName51')
        team_name52 = request.form.get('teamName52')
        team_name53 = request.form.get('teamName53')
        team_name54 = request.form.get('teamName54')
        team_name55 = request.form.get('teamName55')
        team_name56 = request.form.get('teamName56')
        team_name57 = request.form.get('teamName57')
        team_name58 = request.form.get('teamName58')
        team_name59 = request.form.get('teamName59')
        team_name60 = request.form.get('teamName60')
        team_name61 = request.form.get('teamName61')
        team_name62 = request.form.get('teamName62')
        team_name63 = request.form.get('teamName63')
        team_name64 = request.form.get('teamName64')
        
        # Create Matchup objects to be added to the database.
        new_matchup1 = Matchup(game=1, team1=team_name1, team2=team_name2)
        new_matchup2 = Matchup(game=2, team1=team_name3, team2=team_name4)
        new_matchup3 = Matchup(game=3, team1=team_name5, team2=team_name6)
        new_matchup4 = Matchup(game=4, team1=team_name7, team2=team_name8)
        new_matchup5 = Matchup(game=5, team1=team_name9, team2=team_name10)
        new_matchup6 = Matchup(game=6, team1=team_name11, team2=team_name12)
        new_matchup7 = Matchup(game=7, team1=team_name13, team2=team_name14)
        new_matchup8 = Matchup(game=8, team1=team_name15, team2=team_name16)
        new_matchup9 = Matchup(game=9, team1=team_name17, team2=team_name18)
        new_matchup10 = Matchup(game=10, team1=team_name19, team2=team_name20)
        new_matchup11 = Matchup(game=11, team1=team_name21, team2=team_name22)
        new_matchup12 = Matchup(game=12, team1=team_name23, team2=team_name24)
        new_matchup13 = Matchup(game=13, team1=team_name25, team2=team_name26)
        new_matchup14 = Matchup(game=14, team1=team_name27, team2=team_name28)
        new_matchup15 = Matchup(game=15, team1=team_name29, team2=team_name30)
        new_matchup16 = Matchup(game=16, team1=team_name31, team2=team_name32)
        new_matchup17 = Matchup(game=17, team1=team_name33, team2=team_name34)
        new_matchup18 = Matchup(game=18, team1=team_name35, team2=team_name36)
        new_matchup19 = Matchup(game=19, team1=team_name37, team2=team_name38)
        new_matchup20 = Matchup(game=20, team1=team_name39, team2=team_name40)
        new_matchup21 = Matchup(game=21, team1=team_name41, team2=team_name42)
        new_matchup22 = Matchup(game=22, team1=team_name43, team2=team_name44)
        new_matchup23 = Matchup(game=23, team1=team_name45, team2=team_name46)
        new_matchup24 = Matchup(game=24, team1=team_name47, team2=team_name48)
        new_matchup25 = Matchup(game=25, team1=team_name49, team2=team_name50)
        new_matchup26 = Matchup(game=26, team1=team_name51, team2=team_name52)
        new_matchup27 = Matchup(game=27, team1=team_name53, team2=team_name54)
        new_matchup28 = Matchup(game=28, team1=team_name55, team2=team_name56)
        new_matchup29 = Matchup(game=29, team1=team_name57, team2=team_name58)
        new_matchup30 = Matchup(game=30, team1=team_name59, team2=team_name60)
        new_matchup31 = Matchup(game=31, team1=team_name61, team2=team_name62)
        new_matchup32 = Matchup(game=32, team1=team_name63, team2=team_name64)
        
        # Create list of all matchups entered.
        new_matchups = [new_matchup1, new_matchup2, new_matchup3, new_matchup4,
                        new_matchup5, new_matchup6, new_matchup7, new_matchup8,
                        new_matchup9, new_matchup10, new_matchup11, new_matchup12,
                        new_matchup13, new_matchup14, new_matchup15, new_matchup16,
                        new_matchup17, new_matchup18, new_matchup19, new_matchup20,
                        new_matchup21, new_matchup22, new_matchup23, new_matchup24,
                        new_matchup25, new_matchup26, new_matchup27, new_matchup28,
                        new_matchup29, new_matchup30, new_matchup31, new_matchup32]
        
        # List of updated matchups or new matchups to commit to database.
        needed_matchups = []
        
        for new_matchup in new_matchups:
            # Look for a machup in the database with the same year and game number.
            matchups = db.session.query(Matchup).filter(Matchup.game == new_matchup.game).all()
            matchup = None
            if len(matchups) > 0:
                if matchups[0].date.year == date.today().year:
                    matchup = matchups[0]
            
            # If there is a matchup in the database, it needs to be updated.
            if matchup != None:
                if new_matchup.team1 != '':
                    matchup.team1 = new_matchup.team1
                if new_matchup.team2 != '':
                    matchup.team2 = new_matchup.team2
                needed_matchups.append(matchup)
                #TODO: Look in all Picks for the replaced team name and updated them too.
            # If there is not a matching matchup in the database, add a new one.
            else:
                needed_matchups.append(new_matchup)

        db.session.add_all(needed_matchups)
        db.session.commit()
            
        return redirect('/admin/test')
    
    if current_user.is_admin:
        return render_template("enter_teams.html", user=current_user)
    else:
        html_string = '{% extends "base.html" %} {% block title %}Enter Teams' \
            '{% endblock %} {% block content%} </br>' \
            '<h1 align="center">Enter Teams</h1></br>' \
            'Access denied.  Admin access required.' \
            '{% endblock %}'
        return render_template_string(html_string, user=current_user)


@views.route('/admin/round1', methods=['GET', 'POST'])
@login_required
def round1():
    
    # List of all matchups in Round of 64 in current year.
    # This will need to be used in a GET and POST request.
    matchups = []
    
    for i in range(32):
        # Get game 1-32 for the current year and add them to matchups.
        matchups_all = db.session.query(Matchup).filter(Matchup.game == i+1).all()
        for each in matchups_all:
            if each.date.year == date.today().year:
                matchups.append(each)
    
    if request.method == 'POST':
        allGamesFinal = True
        for i in range(32):
            winner = request.form.get('game' + str(i+1))
            if winner == 'team1':
                matchups[i].winner = matchups[i].team1
            elif winner == 'team2':
                matchups[i].winner = matchups[i].team2
            else:
                matchups[i].winner = None
                allGamesFinal = False
        
        # Check if a winner is selected for all matchups and create
        # all matchups for next round if they are all final.
        if allGamesFinal:
            print("Creating matchups for Round of 32...")
            for i in range(16):
                new_matchup = Matchup(game=33+i, team1=matchups[2*i].winner, team2=matchups[2*i+1].winner)
                matchups.append(new_matchup)
                print('Added game ' + str(new_matchup.game) + ' - ' + new_matchup.team1 + ' - ' + new_matchup.team2)
        
        db.session.add_all(matchups)
        db.session.commit()
        
        return redirect('/admin/round1')
        
    if current_user.is_admin:
        html_string = '{% extends "base.html" %} {% block title %}Select Winners' \
            '{% endblock %} {% block content%} </br>' \
            '<h1 align="center">Select Round of 64 Winners</h1></br>' \
            '<form method="POST">'

        for i in range(32):
            html_string += '<h4>Game ' + str(i+1) + '</h4>'
            
            # Create radio buttons for each team in each matchup with winner checked.
            if matchups[i].winner == matchups[i].team1:
                html_string += '<input type="radio" id="team' + str(2*i + 1) + '" name="game' + str(i+1) + '" value="team1" checked>' \
                               '<label for="team1">&nbsp ' + str(matchups[i].team1) + '</label><br>' \
                               '<input type="radio" id="team' + str(2*i + 2) + '" name="game' + str(i+1) + '" value="team2">' \
                               '<label for="team2">&nbsp ' + str(matchups[i].team2) + '</label><br>' \
                               '<input type="radio" id="none' + str(i+1) + '" name="game' + str(i+1) + '" value="none">' \
                               '<label for="none">&nbsp None</label><br><br>'
            elif matchups[i].winner == matchups[i].team2:
                html_string += '<input type="radio" id="team' + str(2*i + 1) + '" name="game' + str(i+1) + '" value="team1">' \
                               '<label for="team1">&nbsp ' + str(matchups[i].team1) + '</label><br>' \
                               '<input type="radio" id="team' + str(2*i + 2) + '" name="game' + str(i+1) + '" value="team2" checked>' \
                               '<label for="team2">&nbsp ' + str(matchups[i].team2) + '</label><br>' \
                               '<input type="radio" id="none' + str(i+1) + '" name="game' + str(i+1) + '" value="none">' \
                               '<label for="none">&nbsp None</label><br><br>'
            else:
                html_string += '<input type="radio" id="team' + str(2*i + 1) + '" name="game' + str(i+1) + '" value="team1">' \
                               '<label for="team1">&nbsp ' + str(matchups[i].team1) + '</label><br>' \
                               '<input type="radio" id="team' + str(2*i + 2) + '" name="game' + str(i+1) + '" value="team2">' \
                               '<label for="team2">&nbsp ' + str(matchups[i].team2) + '</label><br>' \
                               '<input type="radio" id="none' + str(i+1) + '" name="game' + str(i+1) + '" value="none" checked>' \
                               '<label for="none">&nbsp None</label><br><br>'

        html_string += '<button type="submit" class="btn btn-primary">Submit</button>' \
                       '</form><br />' \
                       '{% endblock %}'
        return render_template_string(html_string, user=current_user)
    
    # User is not admin and shouldn't have access to this page.
    else:
        html_string = '{% extends "base.html" %} {% block title %}Select Winners' \
            '{% endblock %} {% block content%} </br>' \
            '<h1 align="center">Select Round of 64 Winners</h1></br>' \
            'Access denied.  Admin access required.' \
            '{% endblock %}'
        return render_template_string(html_string, user=current_user)


@views.route('/admin/test', methods=['GET'])
@login_required
def test():
    if current_user.is_admin:
        html_string = '{% extends "base.html" %} {% block title %}Test' \
            '{% endblock %} {% block content%} </br>' \
            '<h1 align="center">Test</h1></br>'
        
        matchups = db.session.query(Matchup)
        for each in matchups:
            html_string += str(each.game) + ' | ' \
                           + str(each.date.year) + ' | '\
                           + str(each.team1) + ' | ' \
                           + str(each.team2) + ' | ' \
                           + str(each.winner) + '</br>'
        
        html_string += '</br></br>{% endblock %}'
        
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
