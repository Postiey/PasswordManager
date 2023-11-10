from modules.dbconn import Database
from modules.dbconn import Menu
import os
import sys
from sys import platform
import getpass
import time



class Setup(object):
    
    newDB = Database()
    user_os = sys.platform
    current_username = getpass.getuser()
    logo = Menu()
    filepath = ''
    log_filepath = ''
    program_name = 'PasswordManagerLite'
    
    def __init__(self):
        pass
    
    def getOS(self, os):
        self.os = os
        
        if self.os == 'win32':
            return 'win32'
        elif self.os == 'darwin':
            return 'macos'
        elif self.os == 'linux':
            return 'linux'
        
    def checkSetup(self):
        setup_done = False
        
        if Database.checkDatabase(self, 'passwordmanagerlite') == True and Database.checkTables(self, 'passwords', 'mastercredentials') == True:
            setup_done = True
            return setup_done
        else:
            setup_done = False
            return setup_done

    def fullSetup(self):
        Setup.logo.MainLogo
        Setup.filepath = os.path.join(f'C:\\Users\\{Setup.current_username}\\', Setup.program_name)
        Setup.log_filepath = os.path.join(Setup.filepath, "\\log")
        
        setup_completed = False
        
        print("Welcome to `PasswordManagerLite`, a light-weight password manager for your terminal")
        install_confirmation = input("Would you like to install `PasswordManagerLite` on your system? [y] - Yes | [n] - No: ").lower()
        if install_confirmation == 'y':
            # Create folder structure
            if Setup.getOS(self, platform) == 'win32':
                try:
                    print("Creating file paths")
                    os.mkdir(Setup.filepath)
                except Exception as error:
                    print(error)
                else:
                    time.sleep(1)
                    print("File paths have been created successfully.")
            
            print("Creating database...")
            newDatabaseSetup = Database()
            new_setup_confirmation = newDatabaseSetup.createDatabaseStructure()
            if new_setup_confirmation == True:
                credential_confirmation = newDatabaseSetup.createCredentials()
                print("Attempting to create master credentials...")
                if credential_confirmation == True:
                    print("Credentials created and saved to database.")
                    setup_completed = True
                    return setup_completed
                else:
                    print("Error creating credentials. Please try again.")
            else:
                return
        elif install_confirmation == 'n':
            print("You have selected no, installation will exit...")
            return
        else:
            Setup.fullSetup(self)