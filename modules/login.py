from modules.dbconn import Database
import os

class Login():
    
    database = Database()
    user = ''
    
    def __init__(self):
        pass
        
    def loginScreen(self):
        bar = '=' * 31
        middle_text = "PasswordManagerLite"
    
        print(bar)
        print("|     " + middle_text + "     |")
        print(bar)
        Login.loginAuth(self)
    
    def loginAuth(self):
        os.system('CLS')
        bar = '=' * 31
        middle_text = "PasswordManagerLite"
    
        print(bar)
        print("|     " + middle_text + "     |")
        print(bar)
        username = input("Please enter master username: ")
        
        if username != '':
            password = input("Please enter master password: ")
            if password != '':
                if Login.database.checkEntries(username, password) == True:
                    Login.user = username
                    return True
                else:
                    return False
    
    def loginSuccess(self):
        pass
