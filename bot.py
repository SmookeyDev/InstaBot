from instabot import Bot
from textblob import TextBlob
import json

bot = Bot()

bot.login(username='icaroparanhos_', password='passkey8153')

get_followers = bot.get_user_followers_username('icaroparanhos_')

usercheck = True
biocheck = True
full_name = True


userkeys = ['adsd']
biokeys = ['Lauro de Freitas']
namekeys = ['Yuri Matos']
langkeys = ['pt']

for followers in get_followers:
    user_info = bot.get_user_info(followers)

    if usercheck == True:
        if any(i in followers for i in userkeys):
            print(user_info['username'])
            continue

    if full_name == True:
        if any(i in user_info['full_name'] for i in namekeys):
            print(user_info['username'])
            continue

    if biocheck == True:
        if any(i in user_info['biography'] for i in biokeys):
            print(user_info['username'])
            continue


def checklang(user_info):
    bio = user_info['biography']


##print()

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


 #   if langcheck == True:
  #      try:
   #         lang = TextBlob(user_info['biography']).detect_language()
    #    except:
     #       lang = ""
       #     if any(i in lang for i in langkeys):