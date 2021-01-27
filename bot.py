from instabot import Bot
from includes.db import Sql
from includes.handles import hands
from includes.utils import utils
from termcolor import colored

bot = Bot()
db = Sql()
utils = utils()
defs = hands()

def processbot():
    bot.login(username=db.get('username'), password=db.get('password'), is_threaded=True, use_cookie=False)

    while db.get('botprocess') == 'on':

        with open('./includes/usernames.txt') as f:  
            first_line = f.readline()
        get_followers = bot.get_user_followers_username(first_line.replace('\n', ''))
        get_following = bot.get_user_following_username(first_line.replace('\n', ''))

        get_all = get_followers + get_following

        with open('./includes/usernames.txt', 'r') as fin:
            data = fin.read().splitlines(True)
        with open('./includes/usernames.txt', 'w') as fout:
            fout.writelines(data[1:])

        ## Variables
        userkeys = defs.strConvert(db.get('userkeywords'))
        namekeys = defs.strConvert(db.get('namekeywords'))
        biokeys = defs.strConvert(db.get('biokeywords'))

        for followers in get_all:
            user_info = bot.get_user_info(followers)

            count = int(db.get('checked')) + 1
            db.set('checked', count)
            if type(user_info) != bool:
                if db.get('checkuser') == "on":
                    if any(i in user_info['username'] for i in userkeys):
                        print(colored(f"Perfil Encontrado, Parâmetro: Usuário. (Nome: {user_info['full_name']}, Usuário: {user_info['username']})", 'yellow'))
                        defs.verifyProcess(user_info)
                        continue
                if db.get('checkname') == "on":
                    if any(i in user_info['full_name'] for i in namekeys):
                        print(colored(f"Perfil Encontrado, Parâmetro: Nome. (Nome: {user_info['full_name']}, Usuário:{user_info['username']})", 'yellow'))
                        defs.verifyProcess(user_info)
                        continue

                if db.get('checkbio') == "on":
                    if any(i in user_info['biography'] for i in biokeys):
                        print(colored(f"Perfil Encontrado, Parâmetro: Biografia. (Nome: {user_info['full_name']}, Usuário: {user_info['username']})", 'yellow'))
                        defs.verifyProcess(user_info)
                        continue

            if db.get('botprocess') != 'on':
                break
    utils.start()