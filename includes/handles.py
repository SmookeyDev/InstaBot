from includes.db import Sql
from textblob import TextBlob
import json

db = Sql()

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
    
    def getinfos(self, user_info):
        infoslist = {"full_name": user_info['full_name'], "username": user_info['username'], "media_count": user_info['media_count']}
        infos = json.dumps(infoslist)
        infosadd = json.loads(infos)
        if "public_email" in user_info:
            if user_info['public_email'] != '':
                infosadd.update({"public_email": user_info['public_email']})
        if "contact_phone_number" in user_info:
            if user_info['contact_phone_number'] != '':
                infosadd.update({"contact_phone_number": user_info['contact_phone_number']})
        if "category" in user_info:
            if user_info['category'] != None:
                infosadd.update({"category": user_info['category']})

        infosresult = json.dumps(infosadd)

        return json.loads(infosresult)
        


    def verifyProcess(self, user_info):
        if db.get('checkcategories') == "on":
            try:
                categories = user_info['categories']
            except:
                categories = ''
            if any(i in categories for i in self.strConvert(db.get('checkcategories'))):
                if self.checklang(user_info) != None:
                    self.finalProcess(self.getinfos(user_info))
        else:
            if db.get('checklang') == "on":
                if self.checklang(user_info) != None:
                    self.finalProcess(self.getinfos(user_info))
            else:
                    self.finalProcess(self.getinfos(user_info))
    
    def finalProcess(self, user_info):
        if int(user_info['media_count']) >= int(db.get('mediakeywords')):
            print('achei')



