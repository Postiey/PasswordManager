# PasswordManagerLite - Created by Tyler :)
from modules.setup import Setup
from modules.dbconn import Database
from modules.dbconn import Menu
from modules.login import Login
import logging
import datetime

class MainApp():
    
    logging.basicConfig(filename='C:\\Users\\tpostuma\\basic.log', encoding='utf-8', level=logging.INFO, filemode='a', format=f'%(levelname)s - {datetime.datetime.now()} - %(process)d - %(message)s')
    
    database = Database()
    menu = Menu()
    setup = Setup()
    exit_choice = False
    
    def __init__(self):
        pass

    def validateSetup(self):
        validate = Setup()
        return validate.checkSetup()

    def Main(self):
        self.database = MainApp.database
        self.menu = MainApp.menu
        self.setup = MainApp.setup
        
        # Display main menu
        new_menu = self.menu.MainMenu()
        # Get the input of what the user chose and do the action that the user chose
        if new_menu == 'v':
            self.database.viewEntries()
            logging.info(f"User: '{Login.user}' has requested to view all entries in database.")
            if self.menu.backToMainMenu() == False:
                print("PasswordManagerLite has closed!")
                logging.info(f"User: '{Login.user}' has exited the app and signed out.")
                MainApp.exit_choice = True
        elif new_menu == 'a':
            self.database.addEntries()
            logging.info(f"User: '{Login.user}' has requested to add entries to database.")
            if self.menu.backToMainMenu() == False:
                print("PasswordManagerLite has closed!")
                logging.info(f"User: '{Login.user}' has exited the app and signed out.")
                MainApp.exit_choice = True
        elif new_menu == 'r':
            self.database.removeEntries()
            logging.info(f"User: '{Login.user}' has requested to remove entries in database.")
            if self.menu.backToMainMenu() == False:
                print("PasswordManagerLite has closed!")
                logging.info(f"User: '{Login.user}' has exited the app and signed out.")
                MainApp.exit_choice = True
        elif new_menu == 'm':
            self.database.modifyEntries()
            logging.info(f"User: '{Login.user}' has requested to modify entries in database.")
            if self.menu.backToMainMenu() == False:
                print("PasswordManagerLite has closed!")
                logging.info(f"User: '{Login.user}' has exited the app and signed out.")
                MainApp.exit_choice = True
        elif new_menu == 's':
            pass
        elif new_menu == 'e':
            print("PasswordManagerLite has successfully closed!")
            MainApp.exit_choice = True
        else:
            self.menu.MainMenu()
            
        # If the user chooses to go back to the main menu, show the main menu in a loop until they exit
        
new_app = MainApp()
validate = new_app.validateSetup()
new_login = Login()
login_attempts = 0
time = datetime.datetime.now()

if __name__ == "__main__":
    logging.info(f'PasswordManagerLite has started.')
    if validate == True:
        logging.info(f'Was able to find database and all required tables on the system')
        try:
            if new_login.loginAuth() == True:
                logging.info(f"User '{Login.user}' has logged into PasswordManagerLite.")
                while True: 
                    new_app.Main()
                    if new_app.exit_choice == True:
                        break
            else:
                login_attempts += 1
                logging.info("There was an error authenticating the user...")
                print("You have failed to login! Please try again...")     
        except Exception as error:
            print(error)
    else:
        new_app.setup.fullSetup()