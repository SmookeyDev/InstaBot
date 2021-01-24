from includes.db import Sql
from textblob import TextBlob

db = Sql()

class hands:
    def __init__(self):
        pass

    def strConvert(self, string):
        result = list(string.split(', '))
        print(result)
        return result

    def checklang(self, user_info):
        if db.get('checklang') == "on":
            try:
                lang = TextBlob(user_info['biography']).detect_language()
            except:
                lang = ""
            if any(i in lang for i in self.strConvert(db.get('langkeywords'))):
                print('oi')