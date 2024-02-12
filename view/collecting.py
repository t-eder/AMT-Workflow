from flask import render_template
from flask import request
from flask import redirect,flash
import datetime as dt
from model import app, db, Task, AMT_PARTS, user, login_manager
from flask_bcrypt import Bcrypt
from flask_login import UserMixin, login_user, LoginManager, login_required, logout_user, current_user

bcrypt = Bcrypt(app)

@login_manager.user_loader
def load_user(user_id):
    return user.query.get(int(user_id))
@app.route('/login/get', methods=['POST'])
def getlogin():
    usermail = request.form.get('usermail')
    password = request.form.get('password')

    user_obj = user.query.filter_by(usermail=usermail).first()

    if user_obj and bcrypt.check_password_hash(user_obj.password, password):
        # Der Benutzer und das Passwort stimmen überein
        print("Benutzer und Passwort richtig!")
        print(user_obj.usermail)
        login_user(user_obj)
        flash("Erfolgreich angemeldet.", "info")
        return redirect('/')
    else:
        # Benutzer oder Passwort sind falsch
        print("Benutzer oder Passwort falsch!")
        return redirect('/login')

@app.route('/logout/get', methods=['GET', 'POST'])
@login_required
def getlogout():
    logout_user()
    flash("Erfolgreich abgemeldet.", "info")
    return redirect('/login')
@app.route('/signup/get', methods=['POST'])
def getsignup():
    usermail = request.form.get('usermail')
    username = usermail[:usermail.find("@")]
    password = request.form.get('password')
    hashed_password = bcrypt.generate_password_hash(password)
    new_user = user(usermail=usermail, username=username, password=hashed_password)
    db.session.add(new_user)
    db.session.commit()
    flash("Erfolgreich registriert, bitte anmelden.", "info")
    return redirect('/')

@app.route('/user/edit/<int:id>',methods=['POST', 'GET'])
def user_edit(id):
    # amt_parts = AMT_PARTS.query.get(PARTid)
    User = user.query.get(id)
    User.role = request.form.get('role')
    db.session.commit()
    return redirect('/user')

@app.route('/add', methods=['POST'])
def add_task():
    vorgang = request.form.get('vorgang')
    user = current_user.username

    note = request.form.get('note')
    date = dt.datetime.now()
    date = date.strftime("%d.%m.%y - %H:%M")
    if note:
        comment = note + ";" + current_user.username + ";" + date + ";"
    AMTNR = request.form.get('AMTNR')
    GGNR = request.form.get('GGNR')
    creationDate = dt.date.today()
    creationDate = creationDate.strftime("%d.%m.%y")
    owner = ""
    startDate = "Offen"

    EMPB = 0
    if request.form.getlist('EMPB'):
        EMPB = 1

    typ = request.form.getlist('typ')
    typ = "".join(typ)

    kat = request.form.getlist('kat')
    kat = "".join(kat)

    m1_worker = ""
    m2_worker = ""
    m3_worker = ""
    m4_worker = ""
    pt_worker = ""
    e1_worker = ""
    l1_worker = ""
    kt_worker = ""
    m1 = 0
    m2 = 0
    m3 = 0
    m4 = 0
    pt = 0
    e1 = 0
    l1 = 0
    kt = 0
    if request.form.getlist('m1'):  # Checkboxen abfragen und in die Integer 1 schreiben 0=nicht benötigt 1=Offen 2=Erledigt
        m1 = 1
    if request.form.getlist('m2'):
        m2 = 1
    if request.form.getlist('m3'):
        m3 = 1
    if request.form.getlist('m4'):
        m4 = 1
    if request.form.getlist('pt'):
        pt = 1
    if request.form.getlist('e1'):
        e1 = 1
    if request.form.getlist('l1'):
        l1 = 1
    if request.form.getlist('kt'):
        kt = 1

    state = 1

    new_task = Task(
        vorgang=vorgang,
        user=user,
        note=note,
        comment=0,
        leader=0,
        typ=typ,
        kat=kat,
        creationDate=creationDate,
        AMTNR=AMTNR,
        GGNR=GGNR,
        EMPB=EMPB,
        owner=owner,
        m1=m1,
        m2=m2,
        m3=m3,
        m4=m4,
        pt=pt,
        e1=e1,
        l1=l1,
        kt=kt,
        startDate=startDate,
        m1_worker=m1_worker,
        m2_worker=m2_worker,
        m3_worker=m3_worker,
        m4_worker=m4_worker,
        pt_worker=pt_worker,
        e1_worker=e1_worker,
        l1_worker=l1_worker,
        kt_worker=kt_worker,
        state=state
    )
    # Änderung in die Datenbank übertragen
    db.session.add(new_task)
    # Bestätigt die Änderung
    db.session.commit()

    return redirect('/')

@app.route('/edit/<int:id>', methods=['POST'])
def edit(id):
    task = Task.query.get(id)  # Holen Sie sich den vorhandenen Eintrag aus der Datenbank basierend auf der übergebenen ID
    if task:
        task.vorgang = request.form.get('vorgang') #  extrahiert den Wert, der im HTML-Formular mit dem Namen 'Vorgang' eingegeben wurde
        task.owner = request.form.get('owner')
        task.leader = request.form.get('leader')
        task.m1_worker = request.form.get('m1_worker')
        task.m2_worker = request.form.get('m2_worker')
        task.m3_worker = request.form.get('m3_worker')
        task.m4_worker = request.form.get('m4_worker')
        task.pt_worker = request.form.get('pt_worker')
        task.e1_worker = request.form.get('e1_worker')
        task.l1_worker = request.form.get('l1_worker')
        task.kt_worker = request.form.get('kt_worker')
        task.note = request.form.get('note')

        task.state = 3

        if task.startDate == "Offen" and int(task.m1) > 1 or int(task.m2) > 1 or int(task.m3) > 1 or int(task.m4) > 1 or int(task.pt) > 1 or int(task.e1) > 1 or int(task.l1) > 1 or int(task.kt) > 1:
            startDate = dt.date.today()
            task.startDate = startDate.strftime("%d.%m.%y")

        db.session.commit() # Bestätigt die Änderung

    return redirect('/')

@app.route('/categorize/add/<int:id>', methods=['POST'])
def categorize_add(id):
    task = Task.query.get(id)  # Holen Sie sich den vorhandenen Eintrag aus der Datenbank basierend auf der übergebenen ID
    if task:
        date = dt.datetime.now()
        date = date.strftime("%d.%m.%y - %H:%M")
        if request.form.get('note'):
            task.note = request.form.get('note')
            task.comment = task.comment + task.note + ";" + current_user.username + ";" + date + ";"
        change_kat = request.form.getlist('change_kat')

        if "A" in change_kat:
            task.change_kat = False
        else:
            task.change_kat = True

        task.state = 2
        db.session.commit()  # Bestätigt die Änderung

    if task.change_kat == True:
        return redirect('/PM')
    else:
        return redirect(f'/process/{id}')

@app.route('/calculate/add/<int:id>', methods=['POST'])
def calculate_add(id):
    task = Task.query.get(id)  # Holen Sie sich den vorhandenen Eintrag aus der Datenbank basierend auf der übergebenen ID
    if task:
        date = dt.datetime.now()
        date = date.strftime("%d.%m.%y - %H:%M")
        if request.form.get('note'):
            task.note = request.form.get('note')
            task.comment = task.comment + task.note + ";" + current_user.username + ";" + date + ";"


        task.state = 5
        db.session.commit()  # Bestätigt die Änderung

    return redirect('/PM')

@app.route('/release/add/<int:id>', methods=['POST'])
def release_add(id):
    task = Task.query.get(id)  # Holen Sie sich den vorhandenen Eintrag aus der Datenbank basierend auf der übergebenen ID
    if task:
        date = dt.datetime.now()
        date = date.strftime("%d.%m.%y - %H:%M")
        if request.form.get('note'):
            task.note = request.form.get('note')
            task.comment = task.comment + task.note + ";" + current_user.username + ";" + date + ";"

        task.state = 6
        db.session.commit()  # Bestätigt die Änderung

    return redirect('/PM')

@app.route('/process/add/<int:id>', methods=['POST'])
def process_add(id):
        task = Task.query.get(id)  # Holen Sie sich den vorhandenen Eintrag aus der Datenbank basierend auf der übergebenen ID
        if task:
            m1 = request.form.getlist('m1')
            task.m1 = "".join(m1)

            m2 = request.form.getlist('m2')
            task.m2 = "".join(m2)

            m3 = request.form.getlist('m3')
            task.m3 = "".join(m3)

            m4 = request.form.getlist('m4')
            task.m4 = "".join(m4)

            pt = request.form.getlist('pt')
            task.pt = "".join(pt)

            e1 = request.form.getlist('e1')
            task.e1 = "".join(e1)

            l1 = request.form.getlist('l1')
            task.l1 = "".join(l1)

            kt = request.form.getlist('kt')
            task.kt = "".join(kt)

            date = dt.datetime.now()
            date = date.strftime("%d.%m.%y - %H:%M")
            if request.form.get('note'):
                task.note = request.form.get('note')
                task.comment = task.comment + task.note + ";" + current_user.username + ";" + date + ";"

            task.state = 3
            db.session.commit()  # Bestätigt die Änderung

        if task.change_kat == False:
            return redirect('/PM')
        else:
            return redirect(f'/tav')


@app.route('/date/add/<int:id>', methods=['POST'])
def date_add(id):
        task = Task.query.get(id)  # Holen Sie sich den vorhandenen Eintrag aus der Datenbank basierend auf der übergebenen ID
        if task:
            if task:
                date = dt.datetime.now()
                date = date.strftime("%d.%m.%y - %H:%M")
                if request.form.get('note'):
                    task.note = request.form.get('note')
                    task.comment = task.comment + task.note + ";" + current_user.username + ";" + date + ";"
            desiredDate = request.form.get('desiredDate')
            desiredDateObject = dt.datetime.strptime(desiredDate, "%Y-%m-%d").date()
            task.desiredDate = desiredDateObject.strftime("%d.%m.%y")
            task.state = 7

            db.session.commit()  # Bestätigt die Änderung

        return redirect('/PPS')

@app.route('/GETAddPart/<int:id>', methods=['POST', 'GET'])
def AddPart(id):
    task = Task.query.get(id)
    print(request.form)

    AMTNR_PART = task.AMTNR
    GGNR_PART = request.form.get('GGNR_PART')
    REV_PART = request.form.get('REV_PART')
    note_PART = request.form.get('note_PART')
    valid = request.form.get('valid_PART')

    if "0" in valid:
        valid_PART = False
    else:
        valid_PART = True

    NEW_AMT_PARTS = AMT_PARTS(
        GGNR_PART=GGNR_PART,
        AMTNR_PART=AMTNR_PART,
        REV_PART=REV_PART,
        note_PART=note_PART,
        valid_PART=valid_PART
    )
    # Änderung in die Datenbank übertragen
    db.session.add(NEW_AMT_PARTS)
    # Bestätigt die Änderung
    db.session.commit()

    return redirect(f'/process/{id}')

@app.route('/process/part/delete/<int:PARTid>/<int:id>', methods=['POST', 'GET'])
def DeletePart(PARTid,id):
    amt_parts = AMT_PARTS.query.get(PARTid)

    db.session.delete(amt_parts)
    db.session.commit()

    return redirect(f'/process/{id}')

@app.route('/stockrecord/part/addstock/<int:PARTid>/<int:id>', methods=['POST', 'GET'])
def AddStock(id,PARTid):
    amt_parts = AMT_PARTS.query.get(PARTid)
    amt_parts.stock_PART = request.form.get('stock_PART')
    amt_parts.productionstock_PART = request.form.get('productionstock_PART')
    amt_parts.orderstock_PART = request.form.get('orderstock_PART')

    db.session.commit()

    return redirect(f'/stockrecord/{id}')

@app.route('/stockrecord/add/<int:id>', methods=['POST', 'GET'])
def stockrecord_add(id):
    task = Task.query.get(id)
    date = dt.datetime.now()
    date = date.strftime("%d.%m.%y - %H:%M")
    if request.form.get('note'):
        task.note = request.form.get('note')
        task.comment = task.comment + task.note + ";" + current_user.username + ";" + date + ";"
    task.state = 4
    db.session.commit()  # Bestätigt die Änderung

    return redirect('/PPS')

@app.route('/complete/<int:id>')  #Wenn  URL /complete + Zahl(ID) wird aufgerufen wird
def complete_task(id):
    task = Task.query.get(id)
    if task:
        task.completed = True
        db.session.commit()
    return redirect('/')

@app.route('/complete/m1/<int:id>')  #Wenn  URL /complete/m1 + Zahl(ID) wird aufgerufen wird
def complete_m1(id):
    task = Task.query.get(id)
    if task:
        task.m1 = 2
        db.session.commit()
    return redirect('/')

@app.route('/complete/m2/<int:id>')  #Wenn  URL /complete/m2 + Zahl(ID) wird aufgerufen wird
def complete_m2(id):
    task = Task.query.get(id)
    if task:
        task.m2 = 2
        db.session.commit()
    return redirect('/')

@app.route('/complete/m3/<int:id>')  #Wenn  URL /complete/m3 + Zahl(ID) wird aufgerufen wird
def complete_m3(id):
    task = Task.query.get(id)
    if task:
        task.m3 = 2
        db.session.commit()
    return redirect('/')

@app.route('/complete/m4/<int:id>')  #Wenn  URL /complete/m3 + Zahl(ID) wird aufgerufen wird
def complete_m4(id):
    task = Task.query.get(id)
    if task:
        task.m4 = 2
        db.session.commit()
    return redirect('/')

@app.route('/complete/pt/<int:id>')  #Wenn  URL /complete/m3 + Zahl(ID) wird aufgerufen wird
def complete_pt(id):
    task = Task.query.get(id)
    if task:
        task.pt = 2
        db.session.commit()
    return redirect('/')

@app.route('/complete/e1/<int:id>')  #Wenn  URL /complete/m3 + Zahl(ID) wird aufgerufen wird
def complete_e1(id):
    task = Task.query.get(id)
    if task:
        task.e1 = 2
        db.session.commit()
    return redirect('/')

@app.route('/complete/l1/<int:id>')  #Wenn  URL /complete/m3 + Zahl(ID) wird aufgerufen wird
def complete_l1(id):
    task = Task.query.get(id)
    if task:
        task.l1 = 2
        db.session.commit()
    return redirect('/')

@app.route('/complete/kt/<int:id>')  #Wenn  URL /complete/m3 + Zahl(ID) wird aufgerufen wird
def complete_kt(id):
    task = Task.query.get(id)
    if task:
        task.kt = 2
        db.session.commit()
    return redirect('/')
