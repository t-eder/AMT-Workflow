from flask import render_template
from flask import request
from flask import redirect
import datetime as dt
from model import app, db, Task, AMT_PARTS


@app.route('/')
def index(): #ruft alle Aufgaben aus der Datenbank ab und rendert dann ein HTML-Template, um die Aufgaben auf der Webseite anzuzeigen.
    tasks = Task.query.all()
    return render_template('index.html', tasks=tasks)

@app.route('/PM')
def PM(): #ruft alle Aufgaben aus der Datenbank ab und rendert dann ein HTML-Template, um die Aufgaben auf der Webseite anzuzeigen.
    tasks = Task.query.all()
    return render_template('PM.html', tasks=tasks)

@app.route('/categorize/<int:id>')
def categorize(id):
    task = Task.query.get(id)
    desired_id = id
    task = Task.query.filter_by(id=desired_id).first() # Führen Sie eine Abfrage aus, um die Aufgabe mit der gewünschten ID zu finden
    amt_parts = AMT_PARTS.query.all()
    return render_template('categorize.html', task=task, amt_parts=amt_parts)

@app.route('/process/<int:id>')
def process(id):
    task = Task.query.get(id)
    desired_id = id
    task = Task.query.filter_by(id=desired_id).first() # Führen Sie eine Abfrage aus, um die Aufgabe mit der gewünschten ID zu finden
    amt_parts = AMT_PARTS.query.all()
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
def PPS(): #ruft alle Aufgaben aus der Datenbank ab und rendert dann ein HTML-Template, um die Aufgaben auf der Webseite anzuzeigen.
    tasks = Task.query.all()
    return render_template('PPS.html', tasks=tasks)

@app.route('/QS')
def QS(): #ruft alle Aufgaben aus der Datenbank ab und rendert dann ein HTML-Template, um die Aufgaben auf der Webseite anzuzeigen.
    tasks = Task.query.all()
    return render_template('QS.html', tasks=tasks)

@app.route('/done')
def done():
    tasks = Task.query.all()
    return render_template('done.html', tasks=tasks)

@app.route('/add_mask')
def add_mask():
    tasks = Task.query.all()
    return render_template('add_mask.html', tasks=tasks)

@app.route('/task_edit/<int:id>')
def edit_task(id):
    task = Task.query.get(id)
    desired_id = id # Ersetzen Sie 'desired_id' durch die ID, nach der Sie suchen möchten
    task = Task.query.filter_by(id=desired_id).first() # Führen Sie eine Abfrage aus, um die Aufgabe mit der gewünschten ID zu finden
    return render_template('edit_task.html', task=task)

@app.route('/tav')
def tav(): #ruft alle Aufgaben aus der Datenbank ab und rendert dann ein HTML-Template, um die Aufgaben auf der Webseite anzuzeigen.
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
