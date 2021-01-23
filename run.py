import os
from flask import Flask, redirect, url_for, request, render_template
from db import Sql

db = Sql()

app = Flask(__name__)


@app.route('/')
def route_default():
    return redirect(url_for('home'))

@app.route('/home', methods=['GET', 'POST'])
def home():
    return render_template('pages/index.html', checked=0, saved=0)

@app.route('/settings', methods=['GET', 'POST'])
def settings():
    if request.method == 'POST':
        if request.form.get('username'):
            db.set('username', request.form.get('username'))
            db.set('password', request.form.get('password'))
        elif request.form.get('usersearch'):
            if request.form.get('usersearch') != None:
                db.set('usersearch', request.form.get('usersearch'))
            if request.form.get('userkeywords') != None:
                db.set('userkeywords', request.form.get('userkeywords'))
            if request.form.get('namekeywords') != None:
                db.set('namekeywords', request.form.get('namekeywords'))
            if request.form.get('biokeywords') != None:
                db.set('biokeywords', request.form.get('biokeywords'))
            if request.form.get('langkeywords') != None:
                db.set('langkeywords', request.form.get('langkeywords'))
            if request.form.get('categories'):
                catlist = []
                for i in request.form.getlist('categories'):
                    catlist.append(i)
                db.set('categories', str(catlist)[1 : -1])
        else:
            print(request.form)



    lista = []
    categories = open('categories.txt', 'r')
    for line in categories.readlines():
        lista.append(line.strip())
    return render_template('pages/settings.html', username=db.get('username'), password=db.get('password'), usersearch=db.get('usersearch'), userkeywords=db.get('userkeywords'), namekeywords=db.get('namekeywords'), biokeywords=db.get('biokeywords'), langkeywords=db.get('langkeywords'), categories=lista)

@app.route('/teste', methods=['GET', 'POST'])
def teste():
    return render_template('all/ui-forms.html', checked=0, saved=0)



if __name__ == '__main__':
    app.run(host='127.0.0.1', port='3000', debug=True)
