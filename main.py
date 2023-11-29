from model import app, db
from view import presenting
from view import collecting

if __name__ == '__main__': #Überprüft ob die Python Datei direkt ausgeführt wird
    with app.app_context():  # Erstellt einen Anwendungscontext
        db.create_all()  # Erstellt die Datenbanktabellen
    app.run(host="192.168.178.76", port=8000, debug=True)
