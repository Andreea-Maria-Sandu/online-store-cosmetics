# flask este un framework care ne ajuta sa creem o instanta web a aplicatiei
# render-template => HTML
# rquest => obiect care contine datele despre cererea HTTP facuta catre server, contine datele trimise de catre client 
# redirect => redirectionarea catre o alta pagina sau URL
# url_for => construieste URL-uri pe baza rutelor
# session => obiect care permite stocarea datelor de catre server, cum ar fi cereri/comenzi/starea autentificarii
# jsonify => returneaza raspunsuri JSON in API-uri

# flask_mysqldb => extensie pt Flask care faciliteaza conectarea cu MySql


#1. Implorturi necesare:
from flask import Flask, render_template, request, redirect, url_for, session ,jsonify
from flask_mysqldb import MySQL


#2. Initializarea aplicatiei Flask:
# creeaza o instanta Flask si seteaza o cheie secreta pentru sesiuni
app = Flask(__name__)
app.secret_key = 'cheia_secreta'


# 3.Configurare conexiunii MySQL
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'andreea' 
app.config['MYSQL_PASSWORD'] = '1234' 
app.config['MYSQL_DB'] = 'cosmetice'


# 4. Initializarea MySql(creeaza o instanta MySql si o asociaza aplicatiei Flask)
mysql = MySQL(app)


# 5. Rute si functionalitati:
# -> ruta de baza = te duce la pagina principala
@app.route('/')
def index():
    return render_template('start.html')


# -> ruta care te duge la pagina de login
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        # Verificăm dacă username-ul și parola sunt corecte în baza de date
        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM cosmetice.clienti WHERE username = %s AND password = %s", (username, password))
        user = cur.fetchone()
        cur.close()
        if user:
            # Dacă utilizatorul există în baza de date, îl autentificăm și redirecționăm către pagina comenzilor
            session['username'] = username
            session['password'] = password
            return redirect(url_for('comenzi'))
        else:
            # Dacă utilizatorul nu există în baza de date, afișăm un mesaj de eroare
            error = 'Username sau parola incorectă. Încercați din nou.'
            return render_template('login.html', error=error)
    return render_template('login.html')
from flask import jsonify

@app.route('/delete_command', methods=['POST'])
def delete_command():
    if request.method == 'POST':
        # Obținem datele (ID-ul comenzii și numele pizzei) din cererea POST
        data = request.get_json()
        nume_cosmetice = data.get('numecosmetice')
        id_comanda = data.get('idComanda')  # Obținem id-ul comenzii
        print(nume_cosmetice, id_comanda)
        # Obținem ID-ul produsului corespunzător numelui pizzei
        cur = mysql.connection.cursor()
        cur.execute("SELECT idprodus FROM cosmetice.produse WHERE nume = %s", (nume_cosmetice,)) #aflam id_produs
        id_produs = cur.fetchone()[0]
        cur.close()

        # Ștergem produsul din coș
        cur = mysql.connection.cursor()
        cur.execute("DELETE FROM cosmetice.cos WHERE idprodus = %s", (id_produs,)) 
        mysql.connection.commit()
        cur.close()

        cur = mysql.connection.cursor()
        cur.execute("SELECT idclient FROM cosmetice.comenzi WHERE idcomanda = %s", (id_comanda,))
        id_client = cur.fetchone()[0]
        mysql.connection.commit()
        cur.close()

        # Actualizăm prețul total al comenzii
        total_price = update_total_price(id_client=id_client)

        # Răspundem către client că operația a fost efectuată cu succes
        return jsonify({'success': True, 'newTotalPrice': total_price}), 200
    else:
        # Dacă cererea nu este de tip POST, răspundem cu o eroare
        return jsonify({'success': False}), 400

# o functie de agregare SUM()    

def update_total_price(id_client):
    # Obținem prețul total al comenzii
    cur = mysql.connection.cursor()
    cur.execute("SELECT SUM(pret) FROM cosmetice.produse JOIN cosmetice.cos ON produse.idprodus = cos.idprodus WHERE cos.idclient = %s", (id_client,))
    total_price = cur.fetchone()[0]
    cur.close()

    # Actualizăm prețul total al comenzii în baza de date
    cur = mysql.connection.cursor()
    cur.execute("UPDATE cosmetice.comenzi SET pret_comanda = %s WHERE idclient = %s", (total_price, id_client))
    mysql.connection.commit()
    cur.close()

    # Verificăm dacă id-ul clientului există în tabelul cos
    cur = mysql.connection.cursor()
    cur.execute("SELECT idcos FROM cosmetice.cos WHERE idclient = %s", (id_client,))
    result = cur.fetchone()
    cur.close()

    if result is None:  # Dacă id-ul clientului nu există în tabelul cos
        # Obținem id-ul comenzii asociate clientului
        cur = mysql.connection.cursor()
        cur.execute("SELECT idcomanda FROM cosmetice.comenzi WHERE idclient = %s", (id_client,))
        id_comanda = cur.fetchone()
        cur.close()

        # Schimbăm statusul curierului asociat comenzii în "liber"
        cur = mysql.connection.cursor()
        cur.execute("UPDATE cosmetice.curieri SET status = 'liber' WHERE idcurier = (SELECT idcurier FROM cosmetice.comenzi WHERE idcomanda = %s)", (id_comanda,))
        mysql.connection.commit()
        cur.close()

        # Ștergem comanda din baza de date
        cur = mysql.connection.cursor()
        cur.execute("DELETE FROM cosmetice.comenzi WHERE idcomanda = %s", (id_comanda,))
        mysql.connection.commit()
        cur.close()

    return total_price


# VIZUALIZAREA DATELOR DIN 3 TABELE: PRODUSE, CURIERI SI COMENZI


@app.route('/comenzi', methods=['GET', 'POST'])
def comenzi():
    # Verificăm dacă utilizatorul este autentificat
    if 'username' not in session:
        return redirect(url_for('login'))

    # Obținem username și password din sesiune
    username = session['username']
    password = session['password']
    print(username, password)
    # Obținem ID-ul clientului asociat username-ului din sesiune
    cur = mysql.connection.cursor()
    cur.execute("SELECT idclient FROM cosmetice.clienti WHERE username = %s", (username,))
    id_client = cur.fetchone()[0]
    cur.close()

    # Obținem detalii despre comanda clientului și produsele din coșul său
    cur = mysql.connection.cursor()
    cur.execute("""
        SELECT c.idcomanda, c.status, c.pret_comanda, c.adresa, ci.nume AS nume_curier, ci.nr_tel AS tel_curier, p.nume AS nume_produs
        FROM cosmetice.comenzi AS c
        JOIN cosmetice.curieri AS ci ON c.idcurier = ci.idcurier
        JOIN cosmetice.cos AS cos ON c.idclient = cos.idclient
        JOIN cosmetice.produse AS p ON cos.idprodus = p.idprodus
        WHERE c.idclient = %s
    """, (id_client,))
    comenzi = cur.fetchall()
    cur.close()

    # Returnăm șablonul HTML cu detalii despre comanda clientului
    return render_template('comenzi.html', comenzi=comenzi)


# UPPER = functie scalara 

@app.route('/menu')
def menu():
    cur = mysql.connection.cursor()
    cur.execute("SELECT idprodus, UPPER(nume) as nume, pret, brand FROM cosmetice.produse")
    produse = cur.fetchall()
    cur.close()
    return render_template('menu.html', produse=produse)




@app.route('/Ccomanda')
def creare_comanda_pagina():
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM cosmetice.produse")
    produse = cur.fetchall()
    cur.close()
    return render_template('creareComanda.html', produse=produse)


# ACTUALIZARE PRET COMANDA 


@app.route('/creare_comanda', methods=['POST'])
def creare_comanda():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        # Obținem idClient-ul asociat acestui nume de utilizator din baza de date
        cur = mysql.connection.cursor()
        cur.execute("SELECT idclient FROM cosmetice.clienti WHERE username = %s AND password = %s", (username, password))
        id_client = cur.fetchone()
        cur.close()

        # Obținem comenzile de cosmetice din formular
        comenzi = request.form.getlist('cosmetice')  # Obținem o listă cu comenzile selectate
        # Obținem id-ul primului curier cu status-ul "liber"
        cur = mysql.connection.cursor()
        cur.execute("SELECT idcurier FROM cosmetice.curieri WHERE status = 'liber' LIMIT 1")
        id_curier = cur.fetchone()
        cur.close()

        cur = mysql.connection.cursor()
        total_price = 0  # Inițializăm prețul total al comenzii
        for cosmetice in comenzi:
            cur.execute("SELECT idprodus, pret FROM cosmetice.produse WHERE nume = %s", (cosmetice,))
            result = cur.fetchone()
            if result:
                id_produs, pret = result
                total_price += pret  # Adăugăm prețul fiecărei cosmetice la prețul total
                # Inserăm comanda în baza de date
                cur.execute("INSERT INTO cosmetice.cos (idclient, idprodus) VALUES (%s, %s)", (id_client, id_produs))
        mysql.connection.commit()

        # Inserăm comanda în tabela comenzi
        cur.execute("INSERT INTO cosmetice.comenzi (idclient, idcurier, status, pret_comanda, adresa) VALUES (%s, %s, %s, %s, %s)", (id_client, id_curier, 'preparare', total_price, request.form['adresa']))
        mysql.connection.commit()
        cur.close()

        # După ce ai inserat comanda în baza de date, actualizează statusul curierului la "ocupat"
        cur = mysql.connection.cursor()
        cur.execute("UPDATE cosmetice.curieri SET status = 'ocupat' WHERE idcurier = %s", (id_curier,))
        mysql.connection.commit()
        cur.close()

        return redirect(url_for('index'))  # Redirecționăm utilizatorul către pagina principală după ce a creat comanda
    else:
        return redirect(url_for('creare_cont'))  # Dacă utilizatorul nu este autentificat, îl redirecționăm către pagina de creare a contului


@app.route('/Ccont')
def creare_cont():
    return render_template('creareCont.html')


# INSERARE DATE IN TABELUL CLIENTI


@app.route('/creare_cont', methods=['POST'])
def process_registration():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        nr_tel = request.form['nr_tel']
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO clienti (username, password , nr_tel) VALUES (%s, %s , %s)", (username, password , nr_tel))
        mysql.connection.commit()
        cur.close()

        return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
