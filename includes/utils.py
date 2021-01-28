import logging, os
from termcolor import colored


class utils:
    def __init__(self):
        self.botprocess = "off"
    def start(self):
        log = logging.getLogger('werkzeug')
        log.setLevel(logging.ERROR)
        os.system('cls' if os.name == 'nt' else 'clear')
        print("""  ________             _____       ________      _____ 
    ____  _/_______________  /______ ___  __ )_______  /_
    __  / __  __ \_  ___/  __/  __ `/_  __  |  __ \  __/
    __/ /  _  / / /(__  )/ /_ / /_/ /_  /_/ // /_/ / /_  
    /___/  /_/ /_//____/ \__/ \__,_/ /_____/ \____/\__/
                                                    
        """)
        print(' - Developer:', colored('@xSmookeyBR', 'blue'))
        print(' -', colored('InstaBot iniciado, os resultados serão mostrados nessa tela.', 'green'))
        print(" =================================================================\n")
