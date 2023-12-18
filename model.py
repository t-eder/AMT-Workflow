# Datenhaltung
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin, login_user, LoginManager, login_required, logout_user, current_user

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///Databank.db'
app.config['TEMPLATES_AUTO_RELOAD'] = True
app.config['SECRET_KEY'] = 'SECRETKEY_GREIPL'
db = SQLAlchemy(app)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"

# Entwurf einer Datenbank
# 1. Entity Relationship Model ERM
# 2. Relationales Model

class Task(db.Model):  # Hier wird eine Datenbanktabelle definiert, die den Namen "Task" hat und von db.Model erbt
    id = db.Column(db.Integer, primary_key=True)
    state = db.Column(db.Integer, default=0)
        # 1 = Erfasst, 2 = Bewertet, 3 = aufbereit, 4 = Bestände erfasst, 5 = kalkuliert, 6 = Freigegeben, 7 = terminiert, 8 = Kick off,
        # 9 = AMT eingepflegt, 10 = QS Freigegeben, 11 = FAs angepasst

    # Daten aus Backoffice
    typ = db.Column(db.String(5), nullable=False)
    GGNR = db.Column(db.String(10), nullable=False)  # Greiplnummer
    REV = db.Column(db.String(10), nullable=True)  # Aktuelle Revision (aus Infra ziehen!)
    REV_new = db.Column(db.String(10), nullable=True)  # Neue Revision (Aus Kundendaten entnehmen)
    AMTNR = db.Column(db.String(10), nullable=True)  # Änderungsmitteilungsnummer (automatisch vergeben?)
    vorgang = db.Column(db.String(10), nullable=False)  # Vorgangsnummer (aus Infra möglich?)
    leader = db.Column(db.String(20), nullable=False)  # Zuständiger Projektleiter
    user = db.Column(db.String(20), nullable=True)  # Ersteller der ÄMT (Backoffice)
    kat = db.Column(db.Integer, default=1)  # Kategorie des Teils (1 bis 3)
    location = db.Column(db.String(3), nullable=True)  # Fertigungsort
    order = completed = db.Column(db.Boolean, default=True)  # Offene Kundenaufträge Ja/Nein
    creationDate = db.Column(db.String(10), nullable=False)  # Erstellungsdatum
    change = db.Column(db.Boolean, default=True)  # Änderung intern = 0 , Änderung extern = 1

    # Daten aus der Bewertung Projektleitung
    change_kat = db.Column(db.Boolean, default=False)  # 0 = Kategorie A ; 1 = Kategorie B


    # Daten aus Aufbereitung ÄMT KAT A -> PL KAT B -> TAV

    owner = db.Column(db.String(10), nullable=True)  # Hauptverantwortlich TAV

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
    desiredDate = db.Column(db.String(15), nullable=True)
    startDate = db.Column(db.String(15), nullable=True)
    comment = db.Column(db.String(100), nullable=True)
    completed = db.Column(db.Boolean, default=False)

class AMT_PARTS(db.Model):  # Zuordnung der betroffenen Teile zu der AMTNR
    # Pflege im Prozessschritt Aufarbeitung durch TAV oder PL
    id = db.Column(db.Integer, primary_key=True)
    AMTNR_PART = db.Column(db.String(10), db.ForeignKey('task.AMTNR'))
    GGNR_PART = db.Column(db.String(10), nullable=True)
    REV_PART = db.Column(db.String(10), nullable=True)  # Aktuelle Revision (aus Infra ziehen!)
    REV_new_PART = db.Column(db.String(10), nullable=True)  # Neue Revision (Aus Kundendaten entnehmen)
    note_PART = db.Column(db.String(30), nullable=True)
    valid_PART = db.Column(db.Boolean, default=False)  # 0 = ab Neuauftrag ; 1 = Sofortänderung
    stock_PART = db.Column(db.String(25), nullable=True)
    productionstock_PART = db.Column(db.String(25), nullable=True)
    orderstock_PART = db.Column(db.String(25), nullable=True)

    task = db.relationship('Task', backref=db.backref('additional_data', uselist=False, lazy=True))

class user(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    usermail = db.Column(db.String(50), nullable=False, unique=True)
    username =db.Column(db.String(20), nullable=False)
    password = db.Column(db.String(80), nullable=False)
    role = db.Column(db.String(5), nullable=True)
    # Nuterrollen:
    # BO = Backoffice; PM = Projektmanagement; PPS = Produktionsplanung und Steuerung;
    # TAV = Arbeitsvorbereitung; QS = Qualitätssicherung; ADMIN = Alles
