import os
from flask import Flask, redirect, url_for, request, render_template, jsonify
from includes.db import Sql
from includes.utils import utils
import logging
from termcolor import colored

db = Sql()
utils = utils()

app = Flask(__name__)

##VARIABLES
botprocess = "off"

##starting system
log = logging.getLogger('werkzeug')
log.setLevel(logging.ERROR)
os.system('cls' if os.name == 'nt' else 'clear')
print("""  ________             _____       ________      _____ 
  ____  _/_______________  /______ ___  __ )_______  /_
  __  / __  __ \_  ___/  __/  __ `/_  __  |  __ \  __/
  __/ /  _  / / /(__  )/ /_ / /_/ /_  /_/ // /_/ / /_  
  /___/  /_/ /_//____/ \__/ \__,_/ /_____/ \____/\__/
                                              
""")
print( f' - Developer:', colored('@xSmookeyBR', 'blue'))
print(' -', colored('InstaBot iniciado, os resultados serão mostrados nessa tela.', 'green'))
print(" =================================================================\n")


@app.route('/')
def route_default():
    return redirect(url_for('home'))

@app.route('/counters')
def counter():
    form = request.args
    for i in form:
        return db.get(form.get(i))

@app.route('/startbutton')
def startbutton():
    if utils.botprocess == 'on':
        buttonname = "Desligar InstaBot"
        buttonclass = "btn btn-danger btn-round"
    else:
        buttonname = "Iniciar InstaBot"
        buttonclass = "btn btn-success btn-round"
    return jsonify(buttonname=buttonname, buttonclass=buttonclass)

@app.route('/startbot')
def startbot():
    utils.botprocess = 'on'
    return 'ok', 200


@app.route('/stopbot')
def stopbot():
    utils.botprocess = 'off'
    return 'ok', 200


@app.route('/home', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        print(request.form)
    if db.get('checked') == None:
        db.set('checked', str(0))
    if db.get('saved') == None:
        db.set('saved', str(0))
    return render_template('pages/index.html', checked=db.get('checked'), saved=db.get('saved'), approved=db.get('approved'))

@app.route('/settings', methods=['GET', 'POST'])
def settings():
    if request.method == 'POST':
        if request.form.get('username'):
            db.set('username', request.form.get('username'))
            db.set('password', request.form.get('password'))
        elif request.form.get('usersearch'):
            form = request.form
            for i in form:
                if form.get(i) != "":
                    db.set(i, form.get(i))
                else:
                    db.set(i, '')
                if form.get('categories'):
                    catlist = []
                    for i in request.form.getlist('categories'):
                        catlist.append(i)
                    db.set('categories', str(catlist)[1 : -1].replace("'", ""))
                    continue

        else:
            if request.form.get('checkuser'):
                db.set('checkuser', 'on')
            else:
                db.set('checkuser', 'off')
            if request.form.get('checkname'):
                db.set('checkname', 'on')
            else:
                db.set('checkname', 'off')
            if request.form.get('checkbio'):
                db.set('checkbio', 'on')
            else:
                db.set('checkbio', 'off')
            if request.form.get('checklang'):
                db.set('checklang', 'on')
            else:
                db.set('checklang', 'off')
            if request.form.get('checkcategories'):
                db.set('checkcategories', 'on')
            else:
                db.set('checkcategories', 'off')
            if request.form.get('checkmedia'):
                db.set('checkmedia', 'on')
            else:
                db.set('checkmedia', 'off')

    lista = []
    categories = open('./includes/categories.txt', 'r')
    for line in categories.readlines():
        lista.append(line.strip())
    return render_template('pages/settings.html', username=db.get('username'), password=db.get('password'), usersearch=db.get('usersearch'), userkeywords=db.get('userkeywords'), namekeywords=db.get('namekeywords'), biokeywords=db.get('biokeywords'), langkeywords=db.get('langkeywords'), mediakeywords=db.get('mediakeywords'), categories=lista, cuser=verify(db.get('checkuser')), cname=verify(db.get('checkname')), cbio=verify(db.get('checkbio')), clang=verify(db.get('checklang')), ccategories=verify(db.get('checkcategories')), cmedia=verify(db.get('checkmedia')))



def verify(value):
    if value != "on":
        return ''
    else:
        return 'checked'


if __name__ == '__main__':
    app.run(host='127.0.0.1', port='3000', debug=True)
