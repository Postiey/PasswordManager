# Created by Tyler :)

# On another episode of wtf is broken with my code, here are the contenstants...
#   - When a user modifies an entry, it seems like it's getting the tuple correctly from the modifyEntryMenu function but there's an SQL error
#   - When an entry get's removed, the dbID for the rest of the entries should move so it always starts at 1
#       - Probably just need to use an SQL command to update the dbID entries...
#   - Move database to AWS?
#   - Could add different profiles for different users? (not right now tbh...)
#   - Change the backtomainmenu() function to inlude more options 
#        - Options include: 

# Need to add error handling for issues where setup didn't fully complete (ie. if setup failed before master creds could be created, we need to check for master creds on startup to make sure that there's something inside of the database)

import mysql.connector
from mysql.connector import errorcode
from modules.hash import Hash
import time
import os
import logging
import datetime

logging.basicConfig(filename='C:\\Users\\tpostuma\\basic.log', encoding='utf-8', level=logging.INFO, filemode='a', format=f'%(levelname)s - {datetime.datetime.now()} - %(process)d - %(message)s')

class Database(object):
    connection = None
    
    def __init__(self):
        
        if Database.connection is None:
            try:
                Database.connection = mysql.connector.connect(
                    host='localhost',
                    user='root',
                    password='password',
                    port='3308'
                )
            except Exception as error:
                print("Could not connect to the database {}".format(error))
            else:
                logging.info("Successfully connected to the database.")
            
    def createDatabaseStructure(self):
        cursor = Database.connection.cursor()
        database_created = False
        tables_created = False
        
        create_database_sql = """
            CREATE DATABASE `passwordmanagerlite`;
        """
        
        create_master_table_sql = """
            CREATE TABLE `passwordmanagerlite`.`mastercredentials` (
              `masterUsername` VARCHAR(255) NOT NULL,
              `masterPassword` VARCHAR(255) NOT NULL,
              PRIMARY KEY (`masterUsername`));
        """
        
        create_passwords_table_sql = """
            CREATE TABLE `passwordmanagerlite`.`passwords` (
              `dbID` INT NOT NULL AUTO_INCREMENT,
              `username` VARCHAR(255) NOT NULL,
              `password` VARCHAR(255) NOT NULL,
              `email` VARCHAR(255) NULL,
              `url` VARCHAR(255) NULL,
              PRIMARY KEY (`dbID`));
        """
        
        try:
            logging.info(f"Attempting to create database 'PasswordManagerLite'")
            cursor.execute(create_database_sql)
        except Exception as error:
            logging.info(error)
        else:
            database_created = True
            logging.info("PasswordManagerLite database has successfully been created!")
            
        if database_created == True:
            if Database.checkDatabase(self, 'passwordmanagerlite') == True:
                print("The database has been created successfully and validated...")
                logging.info("Validated database is created")
                time.sleep(1)
                try:
                    logging.info("Attempting to create tables 'mastercredentials' and 'passwords'")
                    cursor.execute(create_master_table_sql)
                    cursor.execute(create_passwords_table_sql)
                except Exception as error:
                    print(error)
                else:
                    tables_created = True
                    logging.info("Tables created successfully!")

        if tables_created == True:
            if Database.checkTables(self, 'passwords', 'mastercredentials') == True:
                print("The tables have been successfully created and validated...")
                logging.info("Tables have been verified!")
            else:
                print("There was an error creating the tables, please try again...")
                logging.log("There was an issue with creating the tables...")
                
        if tables_created == True and database_created == True:
            return True
        else:
            return False
                
    def checkEntries(self, username, password):
        self.username = username
        self.password = password
        
        hashobj = Hash()
        hashed_pw = hashobj.hashPassword(self.password)
        
        sql = """
            SELECT * FROM `passwordmanagerlite`.`mastercredentials` LIMIT 1
        """
        
        try:
            cursor = Database.connection.cursor()
            cursor.execute(sql)
            user_data = cursor.fetchall()
            user_data_list = []
            for entry in user_data:
                for i in entry:
                    user_data_list.append(i)
            if user_data_list[0] == self.username and user_data_list[1] == hashed_pw:
                return True
            else:
                return False
        except mysql.connector.Error as error:
            print(error)
        
        
                
    def checkDatabase(self, database):
        self.database = database
        cursor = Database.connection.cursor()
        cursor.execute("SHOW DATABASES")
        databases = cursor.fetchall()
        totalDatabases = []
        
        for d in databases:
            for i in d:
                totalDatabases.append(i)
                
        if self.database in totalDatabases:
            return True
        else:
            return False
         
    def checkTables(self, main_table, master_table):
        self.main_table = main_table
        self.master_table = master_table
        cursor = Database.connection.cursor()
        cursor.execute("SHOW TABLES FROM passwordmanagerlite")
        tables = cursor.fetchall()
        totalTables = []
        
        for t in tables:
            for i in t:
                totalTables.append(i)
        
        
        if self.main_table in totalTables and self.master_table in totalTables:
            return True
        else:
            return False
    
    # Create credentials and save them to DB
    def createCredentials(self):
        username = input("Please type in your master username: ")
        logging.info(f"Master Username set as: {username}")
        password = input("Please type in your master password: ")
        hashobj = Hash()
        hashed_pw = hashobj.hashPassword(password)
        logging.info(f"Master Password saved with hash of: {hashed_pw}")
        credentials_created = False
        
        params = [username, hashed_pw]
        sql = """
            INSERT INTO passwordmanagerlite.mastercredentials (masterUsername, masterPassword)
            VALUES(%s,%s)
            """
        try:
            logging.info("Attempting to save master credentials to the database.")
            cursor = Database.connection.cursor()
            cursor.execute(sql, (params[0],params[1]))
            Database.connection.commit()
            time.sleep(1)
        except mysql.connector.Error as error:
            logging.info(error)
        else:
            logging.info("Successfully saved the credentials to the 'mastercredentials' table.")
            credentials_created = True
            return credentials_created
        
           
    # Get all entries from database
    def viewEntries(self):
        execute_string = 'SELECT * FROM `passwordmanagerlite`.`passwords`;'
        try:
            logging.info("Trying to connect to database to view entries...")
            cursor = Database.connection.cursor()
            logging.info("Connected to database for viewing entries.")
            cursor.execute(execute_string)
            logging.info("Executed SQL for view entries.")
            database_entries = cursor.fetchall()
            logging.info("Gathered all entries and clearing screen to display entries to user.")
        except Exception as error:
            logging.info(error)
        os.system('CLS')
        Menu.MainLogo(self)
        print(f"{'ID':<5}{'Username':<20}{'Password':<35}{'Email':<25}{'Url':<20}")
        print('='*110)
        for row in database_entries:
            print(f"{row[0]:<5}{row[1]:<20}{row[2]:<35}{row[3]:<25}{row[4]:<20}")
        print("\n")
        logging.info("Displaying entries completed.")
         
    # Add entries to database
    def addEntries(self):
        os.system('CLS')
        Menu.MainLogo(self)
        print("Add a new entry")
        username = input("Username: ")
        password = input("Password: ")
        email = input("Email: ")
        url = input("Website / App Url: ")
        
        params = [username, password, email, url]
        sql = """
            INSERT INTO `passwordmanagerlite`.`passwords` (username, password, email, url)
            VALUES(%s,%s,%s,%s)
            """

        try:
            cursor = Database.connection.cursor()
            cursor.execute(sql, (params[0],params[1],params[2],params[3]))
            Database.connection.commit()
            
        except Exception as error:
            print(error)
        else:
            print("Successfully added entry to the database:")
            print("**Username: " + params[0])
            print("**Password: " + params[1])
            print("**Email: " + params[2])
            print("**Url: " + params[3])
    
    # Remove entries from database
    def removeEntries(self):
        os.system('CLS')
        Menu.MainLogo(self)
        Database.viewEntries(self)
        prompt = int(input("Please type the id of the entry you would like to remove: "))
        confirmation_message = input("Please confirm that you would like to remove this password | [y] - yes [n] - no: ").lower()
        
        if confirmation_message == 'y':
            try:
                cursor = Database.connection.cursor()
                cursor.execute("DELETE FROM `passwordmanagerlite`.`passwords` WHERE dbID=%s", (prompt,))
                Database.connection.commit()
            except Exception as error:
                print(error)
            else:
                print("Removed password successfully")
    
    # Modify entries from database
    def modifyEntries(self):
        os.system('CLS')
        Menu.MainLogo(self)
        Database.viewEntries(self)
        
        user_input = int(input("Please select the ID of the entry you want to change: "))
        col_change = Menu.modifyEntryMenu(self)
        
        column_change_input = ''
        new_value_input = col_change[1]
        
        print(col_change)
        if col_change[0] == 'u':
            column_change_input = 'username'
            print(col_change)
        elif col_change[0] == 'p':
            column_change_input = 'password'
        elif col_change[0] == 'e':
            column_change_input = 'email'
        elif col_change[0] == 'h':
            column_change_input = 'url'
        else:
            print("Please select a valid column name.")
        
        
        sql_username = "UPDATE `passwordmanagerlite`.`passwords` SET username='%s' WHERE dbID=%s"
        sql_password = "UPDATE `passwordmanagerlite`.`passwords` SET password='%s' WHERE dbID=%s"
        sql_email = "UPDATE `passwordmanagerlite`.`passwords` SET email='%s' WHERE dbID=%s"
        sql_url = "UPDATE `passwordmanagerlite`.`passwords` SET url='%s' WHERE dbID=%s"
        
        try:
            cursor = Database.connection.cursor()
            if column_change_input == 'username': 
                cursor.execute(sql_username, (new_value_input, user_input))
                Database.connection.commit()
            elif column_change_input == 'password':
                cursor.execute(sql_password, (new_value_input, user_input))
                Database.connection.commit()
            elif column_change_input == 'email':
                cursor.execute(sql_email, (new_value_input, user_input))
                Database.connection.commit()
            elif column_change_input == 'url':
                cursor.execute(sql_url, (new_value_input, user_input))
                Database.connection.commit()
        except Exception as error:
            print(error)
        else:
            print("Everything is working tbh")

 
class Menu(object):
    
    user_selection = ''
    
    def __init__(self):
        pass
    
    def modifyEntryMenu(self):
        print("What field would you like to edit?")
        print("[u] - Username")
        print("[p] - Password")
        print("[e] - Email")
        print("[h] - Url (Hyperlink)")
        modify_entry_input = input("--> ").lower()
        new_value = input("Please enter the new value: ")
        return modify_entry_input, new_value
    
    def MainLogo(self):
        bar = '=' * 31
        middle_text = "PasswordManagerLite"
    
        print(bar)
        print("|     " + middle_text + "     |")
        print(bar)
        
    def MainMenu(self):
        os.system('CLS')
        Menu.MainLogo(self)
        print("Please choose an option from the below list: ")
        print("[v] - View all credentials")
        print("[a] - Add credentials")
        print("[r] - Remove credentials")
        print("[m] - Modify credentials")
        print("[s] - Settings")
        print("[e] - Exit")
        
        Menu.user_selection = input("--> ").lower()
        return Menu.user_selection
    
    def backToMainMenu(self):
        back_choice = input("Would you like to go back to the main menu? [y] - Yes | [n] - No: ")
        print("")
        if back_choice == 'y':
            return True
        elif back_choice == 'n':
            return False
        else:
            Menu.backToMainMenu()