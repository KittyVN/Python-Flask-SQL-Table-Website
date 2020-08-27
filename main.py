#!C:\Program Files\Python\python.exe

from flask import Flask, url_for, request, render_template, redirect
import pyodbc

database = "DB"
server = "SERVER"
conn_str = (
    r'Driver={SQL Server};'
    r'Server='+server+';'
    r'Database='+database+';'
    r'Trusted_Connection=yes;'
    )
tabelleKunde=""



app = Flask(__name__)

@app.route('/')
def index():
    return render_template('homepage.html')


@app.route('/kunden',methods=['POST','GET'])
def kunden():
    conn = pyodbc.connect(conn_str, autocommit=True)
    cursor = conn.cursor()
    kunID = 0


#Wenn das HTML Form ein Post schickt wird entschieden gibt es eine kundenID oder nicht,
# denn wenn es eine gibt möchte ich den Eintrag mit dieser ID bearbeiten, wenn aber keine existiert dann
 # soll das Form einen neuen Eintrag erstellen.
    if request.method == 'POST':
           try:
                kunID = request.form['ID']
           except:
                pass

           vorname = request.form['vorname']
           nachname = request.form['nachname']
           geschlecht = request.form['geschlecht']
           geburtsdatum = request.form['geburtsdatum']
           vip = str(request.form['vip'])

           if int(kunID) > 0:
                cursor.execute(
                    "UPDATE tblKunde SET kunVorname = '" + vorname + "', kunNachname = '" + nachname + "', kunGeburtsdatum = '" + geburtsdatum + "',kunGeschlecht = '" + geschlecht + "', kunVIP = '" + vip + "'  Where kunID =  " + kunID + "")
                return render_template('KundeBearbeitet.html')
           elif int(kunID) == 0:
                cursor.execute(
                    "INSERT INTO tblKunde (kunVorname,kunNachname,kunGeschlecht,kunGeburtsdatum,kunVIP) VALUES ('" + vorname + "','" + nachname + "','" + geschlecht + "','" + geburtsdatum + "','" + vip + "')")
                return render_template('KundeCreate.html')


#Wir schauen uns in der URL die mitgegebenen Werte an wenn es eine ID und einnen delBool Wert mit 1 gibt wird
# der gewählte Eintrag aus der Tabelle gelöscht.
# Wenn delBool aber 0 ist will man den ausgewählten Eintrag bearbeiten.
# Also hier wird das Bearbeitungsform aufgerufen und oben wird es dann in wirklichkeit bearbeitet.
    if request.args.get('kunID'):
        kunID = int(request.args.get('kunID'))
        delBool = int(request.args.get('del'))
        if kunID >=1 & delBool== 1:
            cursor.execute("DELETE from tblKunde WHERE kunID = '" + str(kunID) + "'")
            return render_template('KundeDelete.html')
        elif kunID>=1 & delBool==0:
            cursor.execute("SELECT kunVorname,kunNachname,kunGeburtsdatum,kunVIP FROM tblKunde WHERE kunID ="+str(kunID))

            for row in cursor:
                columncounter = 0
                for x in row:
                    if columncounter == 0:
                        tempVorname = str(x)
                    if columncounter == 1:
                        tempNachname = str(x)
                    if columncounter == 2:
                        tempGeburtsdatum = x
                    if columncounter == 3:
                        tempVIP = x
                    columncounter = columncounter + 1

            return render_template('index1.html',kundenID = kunID,kundenVorname = tempVorname,kundenNachname = tempNachname,kundenGeburtsdatum=tempGeburtsdatum,kundenVIP =tempVIP)
        else:
            return "Incorrect ID for more Informations contact the IM at DW 455"


# Hier wird einfach die Tabelle generell für die Seite erstellt
    cursor.execute("SELECT kunID,kunVorname,kunNachname,kunGeschlecht,kunGeburtsdatum,kunVIP FROM tblKunde")
    tabelleKunde = """
        <table>
        <tr>
        <th>Delete</th>
        <th>Update</th>
        <th>ID</th>
        <th>Vorname</th>
        <th>Nachname</th>
        <th> Geschlecht </th>
        <th>Geburtsdatum</th>
        <th>VIP</th>
        </tr>"""
    for row in cursor:
        tabelleKunde = tabelleKunde + "<tr>"
        columncounter = 0
        for x in row:
            if columncounter == 0:
                tabelleKunde = tabelleKunde + '<td><a href="kunden?kunID='+str(x)+'&del=1">Delete</a></td>'
                tabelleKunde = tabelleKunde + '<td><a href="kunden?kunID='+str(x)+'&del=0">Update</a></td>'
            tabelleKunde = tabelleKunde + "<td>" + str(x) + "</td>"
            columncounter= columncounter+1
        tabelleKunde = tabelleKunde + "</tr>"

    conn.close
    return """<html><head>
        <meta charset="UTF-8">
        <title>Kunden</title>
        <link href="static/style.css" rel="stylesheet">
        </head>
        <body>
        <div class="container">
        <h1>Kundenliste</h1>
        """ + tabelleKunde + """ 
        </table>
        <input class="button" type="button" value="Zurück zu Auswahl" onclick="window.location.href='/'" />
        </div>
        </body>
        </html>"""

@app.route('/neuerKunde')
def neuerKunde():
    return render_template('index.html')

@app.route('/neuesProdukt')
def neuesProdukt():
    return render_template('newProd.html')


#Ich hole mir hier alle IDs damit ich dann im HTML Form ein Dropdown mit allen Einträgen haben kann
@app.route('/neueBestellung')
def neueBestellung():
    conn = pyodbc.connect(conn_str, autocommit=True)
    cursor = conn.cursor()

    cursor.execute("SELECT proID FROM tblProdukte")
    produkte = []
    for x in cursor:
        for y in x:
            produkte.append(y)

    cursor.execute("SELECT kunID FROM tblKunde")
    kunden = []
    for x in cursor:
        for y in x:
            kunden.append(y)


    return render_template('bestellungNeu.html', produkte = produkte,kunden=kunden)


@app.route('/produkte',methods=['POST','GET'])
def prod():
    conn = pyodbc.connect(conn_str, autocommit=True)
    cursor = conn.cursor()
    proID = 0

    if request.method == 'POST':
        try:
            proID = request.form['ID']
        except:
            pass

        bezeichnung = request.form['bezeichnung']
        kosten = str(request.form['kosten'])


        if int(proID) > 0:
            cursor.execute(
                "UPDATE tblProdukte SET proBezeichnung = '" + bezeichnung + "', proKosten = '" + kosten + "'  Where proID =  " + proID + "")
            return render_template('ProduktBearbeitet.html')
        elif int(proID) == 0:
            cursor.execute(
                "INSERT INTO tblProdukte (proBezeichnung,proKosten) VALUES ('" + bezeichnung + "','" + kosten + "')")
            return render_template('ProduktCreate.html')

    if request.args.get('proID'):
        proID = int(request.args.get('proID'))
        delBool = int(request.args.get('del'))
        if proID >= 1 & delBool == 1:
            cursor.execute("DELETE from tblProdukte WHERE proID = '" + str(proID) + "'")
            return render_template('ProduktDelete.html')
        elif proID >= 1 & delBool == 0:
            cursor.execute(
                "SELECT proBezeichnung,proKosten FROM tblProdukte WHERE proID =" + str(proID))

            for row in cursor:
                columncounter = 0
                for x in row:
                    if columncounter == 0:
                        tempBezeichnung = str(x)
                    if columncounter == 1:
                        tempKosten = str(x)
                    columncounter = columncounter + 1

            return render_template('newProd1.html', produktID=proID, produktBezeichnung=tempBezeichnung,
                                   produktKosten=tempKosten)
        else:
            return "Incorrect ID for more Informations contact the IM at DW 455"

    cursor.execute("SELECT proID,proBezeichnung,proKosten FROM tblProdukte")
    tabelleProdukte = """
           <table>
           <tr>
           <th>Delete</th>
           <th>Update</th>
           <th>ID</th>
           <th>Bezeichnung</th>
           <th>Kosten</th>
           </tr>"""
    for row in cursor:
        tabelleProdukte = tabelleProdukte + "<tr>"
        columncounter = 0
        for x in row:
            if columncounter == 0:
                tabelleProdukte = tabelleProdukte + '<td><a href="produkte?proID=' + str(x) + '&del=1">Delete</a></td>'
                tabelleProdukte = tabelleProdukte + '<td><a href="produkte?proID=' + str(x) + '&del=0">Update</a></td>'
            tabelleProdukte = tabelleProdukte + "<td>" + str(x) + "</td>"
            columncounter = columncounter + 1
        tabelleProdukte = tabelleProdukte + "</tr>"

    conn.close
    return """<html><head>
           <meta charset="UTF-8">
           <title>Produkte</title>
           <link href="static/style.css" rel="stylesheet">
           </head>
           <body>
           <div class="container">
            <h1>Produktliste</h1>
           """ + tabelleProdukte + """ 
           </table>
           <input class="button" type="button" value="Zurück zu Auswahl" onclick="window.location.href='/'" />
           </div>
           </body>
           </html>"""


@app.route('/bestellungen', methods=['POST','GET'])
def bestellungen():
    conn = pyodbc.connect(conn_str, autocommit=True)
    cursor = conn.cursor()
    besID = 0


    if request.method == 'POST':
        try:
            besID = request.form['ID']
        except:
            pass

        menge = str(request.form['menge'])
        kunIDRef = str(request.form['kunID'])
        proIDRef = str(request.form['proID'])


        if int(besID) > 0:
            cursor.execute(
                "UPDATE tblBestellung SET besMenge = '" + menge + "', beskunIDRef = '" + kunIDRef + "', besproIDRef ='" +proIDRef +"'  Where besID =  " + besID + "")
            return render_template('BestellungBearbeitet.html')
        elif int(besID) == 0:
            cursor.execute(
                "INSERT INTO tblBestellung (besMenge,beskunIDRef,besproIDRef) VALUES ('" + menge + "','" + kunIDRef + "','" + proIDRef+"')")
            return render_template('BestellungCreate.html')

    if request.args.get('besID'):
        besID = int(request.args.get('besID'))
        delBool = int(request.args.get('del'))
        if besID >= 1 & delBool == 1:
            cursor.execute("DELETE from tblBestellung WHERE besID = '" + str(besID) + "'")
            return render_template('BestellungDelete.html')
        elif besID >= 1 & delBool == 0:
            cursor.execute(
                "SELECT besMenge,beskunIDRef,besproIDRef FROM tblBestellung WHERE besID =" + str(besID))

            for row in cursor:
                columncounter = 0
                for x in row:
                    if columncounter == 0:
                        tempMenge = str(x)
                    if columncounter == 1:
                        tempKun = str(x)
                    if columncounter == 2:
                        tempPro = str(x)
                    columncounter = columncounter + 1


            cursor.execute("SELECT proID FROM tblProdukte")
            produkte = []
            for x in cursor:
                for y in x:
                    produkte.append(y)

            cursor.execute("SELECT kunID FROM tblKunde")
            kunden = []
            for x in cursor:
                for y in x:
                    kunden.append(y)

            return render_template('bestellungNeu1.html', bestellungID=besID, bestellungMenge=tempMenge,
                                   bestellungKun=tempKun,bestellungPro = tempPro,produkte = produkte,kunden=kunden)
        else:
            return "Incorrect ID for more Informations contact the IM at DW 455"



    cursor.execute("SELECT besID,besMenge,beskunIDRef,tblKunde.kunVorname,tblKunde.kunNachname,besproIDRef,proBezeichnung FROM (tblBestellung INNER JOIN tblKunde ON tblBestellung.beskunIDRef = tblKunde.kunID) INNER JOIN tblProdukte ON tblBestellung.besproIDRef = tblPRodukte.proID")
    tabelleBestellung = """
               <table>
               <tr>
               <th>Delete</th>
               <th>Update</th>
               <th>ID</th>
               <th>Menge</th>
               <th>Kunden ID</th>
               <th> Vorname</th>
               <th> Nachname</th>
               <th>Produkt ID</th>
               <th>Bezeichnung</th>
               </tr>"""
    for row in cursor:
        tabelleBestellung = tabelleBestellung + "<tr>"
        columncounter = 0
        for x in row:
            if columncounter == 0:
                tabelleBestellung = tabelleBestellung + '<td><a href="bestellungen?besID=' + str(x) + '&del=1">Delete</a></td>'
                tabelleBestellung = tabelleBestellung + '<td><a href="bestellungen?besID=' + str(x) + '&del=0">Update</a></td>'
            tabelleBestellung = tabelleBestellung + "<td>" + str(x) + "</td>"
            columncounter = columncounter + 1
        tabelleBestellung = tabelleBestellung + "</tr>"

    conn.close
    return """<html><head>
               <meta charset="UTF-8">
               <title>Bestellungen</title>
               <link href="static/style.css" rel="stylesheet">
               </head>
               <body>
               <div class="container">
                <h1>Bestellungen</h1>
               """ + tabelleBestellung + """ 
               </table>
               <input class="button" type="button" value="Zurück zu Auswahl" onclick="window.location.href='/'" />
               </div>
               </body>
               </html>"""


if __name__ == '__main__':
    app.run(debug=False)

