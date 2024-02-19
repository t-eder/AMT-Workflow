# Readme
# Einrichtung Virtuelle Umgebung
### pip install flask sqlalchemy flask_sqlalchemy datetime flask_login flask_bcrypt flask_wtf wtforms email_validator

# Datenbank bearbeiten
## Löschen:
### import sqlite3
### connect = sqlite3.connect("instance/Databank.db")
### pointer = connect.cursor()
#### pointer.execute("DELETE FROM task")
### connect.commit()
### pointer.execute("SELECT * FROM task")
### inhalt = pointer.fetchall()
### print(inhalt)
### connect.close()