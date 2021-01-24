import os
from flask import Flask, redirect, url_for, request, render_template
from includes.db import Sql

db = Sql()

app = Flask(__name__)


@app.route('/')
def route_default():
    return redirect(url_for('home'))

@app.route('/home', methods=['GET', 'POST'])
def home():
    if db.get('checked') == None:
        db.set('checked', str(0))
    if db.get('saved') == None:
        db.set('saved', str(0))
    return render_template('pages/index.html', checked=db.get('checked'), saved=db.get('saved'))

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
                    db.set('categories', str(catlist)[1 : -1])
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

    lista = []
    categories = open('./includes/categories.txt', 'r')
    for line in categories.readlines():
        lista.append(line.strip())
    return render_template('pages/settings.html', username=db.get('username'), password=db.get('password'), usersearch=db.get('usersearch'), userkeywords=db.get('userkeywords'), namekeywords=db.get('namekeywords'), biokeywords=db.get('biokeywords'), langkeywords=db.get('langkeywords'), categories=lista, cuser=verify(db.get('checkuser')), cname=verify(db.get('checkname')), cbio=verify(db.get('checkbio')), clang=verify(db.get('checklang')), ccategories=verify(db.get('checkcategories')))



def verify(value):
    if value != "on":
        return ''
    else:
        return 'checked'


if __name__ == '__main__':
    app.run(host='127.0.0.1', port='3000', debug=True)
