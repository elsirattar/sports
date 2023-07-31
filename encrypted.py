from mysql.connector.locales.eng import client_error

import json
from cryptography.fernet import Fernet
# import MySQLdb as mdb
from PyQt5.QtWidgets import QMessageBox

from getpass import getpass
from mysql.connector import connect,Error


class Connection:
    def __init__(self):
        self.db = None
        self.cr = None
        # self.connector()

    def connector(self):
        # key = b'_FNDmD6gfe0AQOB-P-pVMiX8f51M00Q8Rpg-5et3t3M='
        # fernet = Fernet(key)
        # with open('database.json', 'rb') as file:
        #     original = file.read()
        # decrypted = fernet.decrypt(original)

        conf = {"user": "root", "host": "localhost", "location": "", "dbname": "sports"}
        dbase = conf['dbname']
        user = conf['user']
        host = conf['host']
        password = conf['location']
        try:    
            self.db = connect(host=host,user=user,password=password,database=dbase)
            self.cr = self.db.cursor(buffered = True)
        except Exception as e:
            print(e)
            QMessageBox.about(self, 'connection', str(e))