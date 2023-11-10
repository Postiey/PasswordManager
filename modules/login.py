from modules.dbconn import Database

class Login():
    
    database = Database()
    
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
        username = input("Please enter master username: ")
        
        if username != '':
            password = input("Please enter master password: ")
            if password != '':
                
                print(Login.database.checkEntries(username, password))
    
    def loginSuccess(self):
        pass


    

newLogin = Login()
newLogin.loginScreen()
