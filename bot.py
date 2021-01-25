from instabot import Bot
from includes.db import Sql
from includes.handles import hands

bot = Bot()
db = Sql()
defs = hands()

bot.login(username=db.get('username'), password=db.get('password'))
get_followers = bot.get_user_followers_username(db.get('usersearch'))
get_following = bot.get_user_following_username(db.get('usersearch'))

get_all = get_followers + get_following

## Variables
userkeys = defs.strConvert(db.get('userkeywords'))
namekeys = defs.strConvert(db.get('namekeywords'))
biokeys = defs.strConvert(db.get('biokeywords'))

for followers in get_all:
    user_info = bot.get_user_info(followers)

    count = int(db.get('checked')) + 1
    db.set('checked', count)
    if db.get('checkuser') == "on":
        if any(i in followers for i in userkeys):
            defs.verifyProcess(user_info)
            print(f"Perfil Encontrado, Parâmetro: Usuário. (Nome: {user_info['full_name']}, Usuário: {user_info['username']})")
            continue

    if db.get('checkname') == "on":
        if any(i in user_info['full_name'] for i in namekeys):
            defs.verifyProcess(user_info)
            print(f"Perfil Encontrado, Parâmetro: Nome. (Nome: {user_info['full_name']}, Usuário:{user_info['username']})")
            continue

    if db.get('checkbio') == "on":
        if any(i in user_info['biography'] for i in biokeys):
            defs.verifyProcess(user_info)
            print(f"Perfil Encontrado, Parâmetro: Biografia. (Nome: {user_info['full_name']}, Usuário: {user_info['username']})")
            continue






##result = bot.get_user_info('doctorrahimd')
##print(f"""
##{result['username']}
##{result['full_name']}
##{result['is_private']}
##{result['media_count']}
##{result['category']}
##{result['contact_phone_number']}
##{result['public_email']}
##{result['public_phone_country_code']}{result['public_phone_number']}
##{result['is_business']}
##{result['account_type']}
##{result['whatsapp_number']}""")

#re.findall(r'[\w\.-]+@[\w\.-]+', line)