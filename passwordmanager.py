# PasswordManagerLite - Created by Tyler :)
from modules.setup import Setup
from modules.dbconn import Database
from modules.menu import Menu
from modules.login import Login
import sys

class MainApp():
    
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
            if self.menu.backToMainMenu() == False:
                MainApp.exit_choice = True
        elif new_menu == 'a':
            self.database.addEntries()
            if self.menu.backToMainMenu() == False:
                MainApp.exit_choice = True
        elif new_menu == 'r':
            self.database.removeEntries()
            if self.menu.backToMainMenu() == False:
                MainApp.exit_choice = True
        elif new_menu == 'm':
            self.database.modifyEntries()
            if self.menu.backToMainMenu() == False:
                MainApp.exit_choice = True
        else:
            self.menu.MainMenu()
            
        # If the user chooses to go back to the main menu, show the main menu in a loop until they exit
        
new_app = MainApp()
validate = new_app.validateSetup()
new_login = Login

if __name__ == "__main__":
    if validate == True:
        try:
            new_login.loginScreen
        except Exception as error:
            print(error)
        # while True: 
        #     new_app.Main()
        #     if new_app.exit_choice == True:
        #         break
    else:
        new_app.setup.fullSetup()