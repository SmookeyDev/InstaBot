import os
from flask import Flask, redirect, url_for, request, render_template, jsonify
from includes.db import Sql
from includes.utils import utils
import logging
from termcolor import colored
import bot
import threading
import sqlite3
import pandas as pd

db = Sql()
utils = utils()

app = Flask(__name__)

##Start system
utils.start()


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
    if db.get('botprocess') == 'on':
        buttonname = "Desligar InstaBot"
        buttonclass = "btn btn-danger btn-round"
    else:
        buttonname = "Iniciar InstaBot"
        buttonclass = "btn btn-success btn-round"
    return jsonify(buttonname=buttonname, buttonclass=buttonclass)

@app.route('/startbot')
def startbot():
    db.set('botprocess', 'on')
    if db.get('resetbot') == '':
        db.set('resetbot', '0')
    utils.start()
    with open('./includes/usernames.txt', 'a') as arq:
        user = db.get('usersearch')
        if user not in open('./includes/usernames.txt', 'r').read():
            arq.write('{}\n'.format(user))
    s = threading.Thread(target=bot.processbot)
    s.start()
    return 'ok', 200


@app.route('/stopbot')
def stopbot():
    db.set('botprocess', 'off')
    with open("./includes/usernames.txt",'r') as f:
        with open("./includes/empty-dontdelete.txt",'w') as f1:
            f.next()
            for line in f:
                f1.write(line)
    return 'ok', 200

@app.route('/buttondelete')
def buttondelete():
    db.set('botprocess', 'off')
    if db.get('resetbot') == '':
        db.set('resetbot', '0')
    else:
        db.set('resetbot', '{}'.format(int(db.get('resetbot')) + 1))
    db.set('checked', '0')
    db.set('saved', '0')
    db.set('approved', '0')
    db.set('row', '0')
    try:
        os.remove('./includes/usernames.txt')
    except:
        pass
    conn = sqlite3.connect('excel.db')
    conne = conn.cursor()
    df = pd.read_sql('SELECT * FROM SAVED', conn)
    df.to_csv('saved-{}.csv'.format(db.get('resetbot')))

    df = pd.read_sql('SELECT * FROM APPROVED', conn)
    df.to_csv('approved-{}.csv'.format(db.get('resetbot')))
    conne.execute('DELETE FROM SAVED')
    conn.commit()
    conne.execute('DELETE FROM APPROVED')
    conn.commit()

    return 'ok', 200


@app.route('/home', methods=['GET', 'POST'])
def home():
    if db.get('checked') == '':
        db.set('checked', '0')
    if db.get('saved') == '':
        db.set('saved', '0')
    if db.get('approved') == '':
        db.set('approved', '0')
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
    db.set('botprocess', 'off')
    app.run(host='127.0.0.1', port='3000', debug=True)