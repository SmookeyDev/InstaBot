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
                db.set('categories', str(catlist).replace("'", "")[1 : -1])
        else:
            if request.form.get('checkuser'):
                db.set('checkuser', request.form.get('checkuser'))
            else:
                db.set('checkuser', 'off')
            if request.form.get('checkname'):
                db.set('checkname', request.form.get('checkname'))
            else:
                db.set('checkname', 'off')
            if request.form.get('checkbio'):
                db.set('checkbio', request.form.get('checkbio'))
            else:
                db.set('checkbio', 'off')
            if request.form.get('checklang'):
                db.set('checklang', request.form.get('checklang'))
            else:
                db.set('checklang', 'off')
            if request.form.get('checkcategories'):
                db.set('checkcategories', request.form.get('checkcategories'))
            else:
                db.set('checkcategories', 'off')