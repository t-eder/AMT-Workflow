from flask import render_template
from flask import request
from flask import redirect, flash
import datetime as dt
from model import app, db, Task, AMT_PARTS, login_manager, user
from flask_login import UserMixin, login_user, LoginManager, login_required, logout_user, current_user
import sqlite3

@login_manager.user_loader
def load_user(user_id):
    print(user_id)
    return user.query.get(int(user_id))

@app.route('/')
def index(): #ruft alle Aufgaben aus der Datenbank ab und rendert dann ein HTML-Template, um die Aufgaben auf der Webseite anzuzeigen.
    print(current_user)
    tasks = Task.query.all()
    User = user.query.all()
    return render_template('index.html', tasks=tasks, User=User)

@app.route('/signup')
def signup(): #ruft alle Aufgaben aus der Datenbank ab und rendert dann ein HTML-Template, um die Aufgaben auf der Webseite anzuzeigen.
    tasks = Task.query.all()
    return render_template('signup.html', tasks=tasks)

@app.route('/login')
def login(): #ruft alle Aufgaben aus der Datenbank ab und rendert dann ein HTML-Template, um die Aufgaben auf der Webseite anzuzeigen.
    tasks = Task.query.all()
    print(current_user)
    return render_template('login.html', tasks=tasks)
@app.route('/user')
def users():
    User = user.query.all()
    return render_template('user.html', User=User)

@app.route('/help')
def help(): #ruft alle Aufgaben aus der Datenbank ab und rendert dann ein HTML-Template, um die Aufgaben auf der Webseite anzuzeigen.
    task = Task.query.get(1)
    return render_template('help.html', task=task)

@app.route('/PM')
@login_required
def PM(): #ruft alle Aufgaben aus der Datenbank ab und rendert dann ein HTML-Template, um die Aufgaben auf der Webseite anzuzeigen.
    if not (current_user.role == "PM" or current_user.role == "ADMIN"):
        flash("Keine Berechtigung.", "info")
        return render_template('nopermission.html')
    tasks = Task.query.all()
    return render_template('PM.html', tasks=tasks)
@app.route('/categorize/<int:id>')
def categorize(id):
    task = Task.query.get(id)
    desired_id = id
    task = Task.query.filter_by(id=desired_id).first() # Führen Sie eine Abfrage aus, um die Aufgabe mit der gewünschten ID zu finden
    amt_parts = AMT_PARTS.query.all()
    users = user.query.all()
    return render_template('categorize.html', task=task, amt_parts=amt_parts, user=users)

@app.route('/calculate/<int:id>')
def calculate(id):
    task = Task.query.get(id)
    desired_id = id
    task = Task.query.filter_by(id=desired_id).first() # Führen Sie eine Abfrage aus, um die Aufgabe mit der gewünschten ID zu finden
    amt_parts = AMT_PARTS.query.all()
    return render_template('calculate.html', task=task, amt_parts=amt_parts)

@app.route('/release/<int:id>')
def release(id):
    task = Task.query.get(id)
    desired_id = id
    task = Task.query.filter_by(id=desired_id).first() # Führen Sie eine Abfrage aus, um die Aufgabe mit der gewünschten ID zu finden
    amt_parts = AMT_PARTS.query.all()
    return render_template('release.html', task=task, amt_parts=amt_parts)

@app.route('/date/<int:id>')
def date(id):
    task = Task.query.get(id)
    desired_id = id
    task = Task.query.filter_by(id=desired_id).first() # Führen Sie eine Abfrage aus, um die Aufgabe mit der gewünschten ID zu finden
    amt_parts = AMT_PARTS.query.all()
    return render_template('date.html', task=task, amt_parts=amt_parts)

@app.route('/process/<int:id>')
def process(id):
    task = Task.query.get(id)
    desired_id = id
    task = Task.query.filter_by(id=desired_id).first() # Führen Sie eine Abfrage aus, um die Aufgabe mit der gewünschten ID zu finden


    amt_parts = AMT_PARTS.query.all()

    def sort_key(entry):
        if entry.parent is not None:
            numeric_part = ''.join(filter(str.isdigit, entry.parent))
            return (int(numeric_part) if numeric_part else 0, entry.parent)
        else:
            return (0, '')
    amt_parts.sort(key=sort_key)

    print(amt_parts)

    return render_template('process.html', task=task, amt_parts=amt_parts)

@app.route('/stockrecord/<int:id>')
def stockrecord(id):
    task = Task.query.get(id)
    desired_id = id
    task = Task.query.filter_by(id=desired_id).first() # Führen Sie eine Abfrage aus, um die Aufgabe mit der gewünschten ID zu finden
    amt_parts = AMT_PARTS.query.all()
    return render_template('stockrecord.html', task=task, amt_parts=amt_parts)

@app.route('/AddPart/<int:id>')
def Add_Part(id):
    task = Task.query.get(id)
    desired_id = id
    task = Task.query.filter_by(id=desired_id).first()
    return render_template('Add_Part.html', task=task)

@app.route('/PPS')
@login_required
def PPS(): #ruft alle Aufgaben aus der Datenbank ab und rendert dann ein HTML-Template, um die Aufgaben auf der Webseite anzuzeigen.
    if not (current_user.role == "PPS" or current_user.role == "ADMIN"):
        flash("Keine Berechtigung.", "info")
        return render_template('nopermission.html')
    tasks = Task.query.all()
    return render_template('PPS.html', tasks=tasks)
@app.route('/QS')
@login_required
def QS(): #ruft alle Aufgaben aus der Datenbank ab und rendert dann ein HTML-Template, um die Aufgaben auf der Webseite anzuzeigen.
    if not (current_user.role == "QS" or current_user.role == "ADMIN"):
        flash("Keine Berechtigung.", "info")
        return render_template('nopermission.html')
    tasks = Task.query.all()
    return render_template('QS.html', tasks=tasks)

@app.route('/done')
def done():
    tasks = Task.query.all()
    return render_template('done.html', tasks=tasks)

@app.route('/add_mask')
@login_required
def add_mask():
    if not (current_user.role == "BO" or current_user.role == "ADMIN"):
        flash("Keine Berechtigung.", "info")
        return render_template('nopermission.html')
    task = Task.query.all()
    return render_template('add_mask.html', task=task)

@app.route('/task_edit/<int:id>')
def edit_task(id):
    task = Task.query.get(id)
    desired_id = id # Ersetzen Sie 'desired_id' durch die ID, nach der Sie suchen möchten
    task = Task.query.filter_by(id=desired_id).first() # Führen Sie eine Abfrage aus, um die Aufgabe mit der gewünschten ID zu finden
    return render_template('edit_task.html', task=task)

@app.route('/tav')
@login_required
def tav(): #ruft alle Aufgaben aus der Datenbank ab und rendert dann ein HTML-Template, um die Aufgaben auf der Webseite anzuzeigen.
    if not (current_user.role == "TAV" or current_user.role == "ADMIN"):
        flash("Keine Berechtigung.", "info")
        return render_template('nopermission.html')
    tasks = Task.query.all()
    return render_template('TAV.html', tasks=tasks)

@app.route('/index/<int:id>')
def indexAMT(id):
    task = Task.query.get(id)
    desired_id = id # Ersetzen Sie 'desired_id' durch die ID, nach der Sie suchen möchten
    task = Task.query.filter_by(id=desired_id).first() # Führen Sie eine Abfrage aus, um die Aufgabe mit der gewünschten ID zu finden
    amt_parts = AMT_PARTS.query.all()
    return render_template('indexAMT.html', task=task, amt_parts=amt_parts)

@app.route('/data/<int:id>')
def task_data(id):
    task = Task.query.get(id)
    desired_id = id # Ersetzen Sie 'desired_id' durch die ID, nach der Sie suchen möchten
    task = Task.query.filter_by(id=desired_id).first() # Führen Sie eine Abfrage aus, um die Aufgabe mit der gewünschten ID zu finden

    # Geben Sie den Pfad zum Ordner an, den Sie öffnen möchten
    #folder_path = r'C:\Users\Tobias\Documents\Arduino'
    # Verwenden Sie os.system, um den Ordner im Datei-Explorer zu öffnen
    #subprocess.Popen(f'explorer "{folder_path}"')

    return "Folder opened successfully"
