# Datenhaltung
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///tasks.db'
app.config['TEMPLATES_AUTO_RELOAD'] = True
db = SQLAlchemy(app)

class Task(db.Model):  # Hier wird eine Datenbanktabelle definiert, die den Namen "Task" hat und von db.Model erbt
    id = db.Column(db.Integer, primary_key=True)
    vorgang = db.Column(db.String(10), nullable=False)
    AMTNR = db.Column(db.String(10), nullable=True)
    GGNR = db.Column(db.String(10), nullable=False)
    user = db.Column(db.String(20), nullable=True)
    leader = db.Column(db.String(20), nullable=False)
    typ = db.Column(db.String(5), nullable=False)
    kat = db.Column(db.Integer, default=1)
    owner = db.Column(db.String(10), nullable=True)
    creationDate = db.Column(db.String(10), nullable=False)
    note = db.Column(db.String(500), nullable=True)
    EMPB = db.Column(db.Integer, default=0)
    m1 = db.Column(db.Integer, default=0)
    m1_worker = db.Column(db.String(10), nullable=True)
    m2 = db.Column(db.Integer, default=0)
    m2_worker = db.Column(db.String(10), nullable=True)
    m3 = db.Column(db.Integer, default=0)
    m3_worker = db.Column(db.String(10), nullable=True)
    m4 = db.Column(db.Integer, default=0)
    m4_worker = db.Column(db.String(10), nullable=True)
    pt = db.Column(db.Integer, default=0)
    pt_worker = db.Column(db.String(10), nullable=True)
    e1 = db.Column(db.Integer, default=0)
    e1_worker = db.Column(db.String(10), nullable=True)
    l1 = db.Column(db.Integer, default=0)
    l1_worker = db.Column(db.String(10), nullable=True)
    kt = db.Column(db.Integer, default=0)
    kt_worker = db.Column(db.String(10), nullable=True)
    desiredDate = db.Column(db.String(15), nullable=False)
    startDate = db.Column(db.String(15), nullable=False)
    completed = db.Column(db.Boolean, default=False)