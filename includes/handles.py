from includes.db import Sql, Sql2
from textblob import TextBlob
import openpyxl as op
import json
from termcolor import colored

db = Sql()
db2 = Sql2()

class hands:
    def __init__(self):
        pass

    def strConvert(self, string):
        result = list(string.split(', '))
        return result

    def checklang(self, user_info):
        if db.get('checklang') == "on":
            try:
                lang = TextBlob(user_info['biography']).detect_language()
            except:
                lang = ""
            if any(i in lang for i in self.strConvert(db.get('langkeywords'))):
                return(lang)
    
    def saveexcel(self, jsonx, name):
        wb = op.Workbook()
        sheet = wb.active
        sheet.title = "InstaBot"
        if name == "approved":
            sheet['A1'] = 'Full Name'
            sheet['B1'] = 'Username'
            sheet['F1'] = 'Email'

            taglist = ['full_name', 'username', 'public_email']
        else:
            sheet['A1'] = 'Full Name'
            sheet['B1'] = 'Username'
            sheet['F1'] = 'Email'
            sheet['C1'] = 'Media Count'
            sheet['D1'] = 'Contact Phone'
            sheet['E1'] = 'Category'

            taglist = ['full_name', 'username', 'media_count', 'contact_phone_number', 'category', 'public_email']
        if jsonx != None:
            if db.get('row') == '' or db.exists('row') == False:
                db.set('row', '2')
            else:
                db.set('row', int(db.get('row')) + 1) 
            for item in jsonx:
                if item in taglist:
                    position = taglist.index(item) + 1
                    value = jsonx[item]
                    sheet.cell(column=position, row=int(db.get('row')), value=value)
                    wb.save("{}-{}.xlsx".format(name, db.get('resetbot')))


    def getinfos(self, user_info):
        infoslist = {"full_name": user_info['full_name'], "username": user_info['username'], "media_count": user_info['media_count']}
        infos = json.dumps(infoslist)
        infosadd = json.loads(infos)
        if "contact_phone_number" in user_info:
            if user_info['contact_phone_number'] != '':
                infosadd.update({"contact_phone_number": user_info['contact_phone_number']})
        else:
            infosadd.update({"contact_phone_number": ''})
        if "category" in user_info:
            if user_info['category'] != None:
                infosadd.update({"category": user_info['category']})
        else:
            infosadd.update({"category": ''})
        if "public_email" in user_info:
            if user_info['public_email'] != '':
                infosadd.update({"public_email": user_info['public_email']})
                
                infosresult = json.dumps(infosadd)
                result =  json.loads(infosresult)
                db2.sset(user_info)
                
                with open('./includes/usernames.txt', 'a') as arq:
                    arq.write('{}\n'.format(user_info['username']))
                count = int(db.get('saved')) + 1
                db.set('saved', count)

                print(colored(f"Usuário verificado. (Usuário: {result['username']}, Email: {result['public_email']})", 'blue'))

                return result
        return False
    def verifyProcess(self, user_info):
        if db.get('checkcategories') == "on":
            try:
                categories = user_info['category'].lower()
            except:
                categories = ''
            if categories != None:
                if any(i in categories for i in self.strConvert(db.get('categories'))):
                    if self.checklang(user_info) != None:
                        self.finalProcess(user_info,self.getinfos(user_info))
        else:
            if db.get('checklang') == "on":
                if self.checklang(user_info) != None:
                    self.finalProcess(user_info,self.getinfos(user_info))
            else:
                    self.finalProcess(user_info,self.getinfos(user_info))
    
    def finalProcess(self, user_info, jsonx):
        if jsonx != False:
            if db.get('checkmedia') == 'on':
                if int(user_info['media_count']) >= int(db.get('mediakeywords')):
                    count = int(db.get('approved')) + 1
                    db.set('approved', count)
                    print(colored(f"Usuário aprovado. (Usuário: {user_info['username']}, Email: {user_info['public_email']})", 'green'))
                    db2.aset(user_info)
            else:
                count = int(db.get('approved')) + 1
                db.set('approved', count)
                print(colored(f"Usuário aprovado. (Usuário: {user_info['username']}, Email: {user_info['public_email']})", 'green'))
                db2.aset(user_info)
