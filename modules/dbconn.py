# Created by Tyler :)

# File specifics:
#   - Database class for all related database actions:
#       - Creating entire database structure (includes tables and columns) <-- This will also check to make sure db is created      correctly and that all tables were created correctly 
#       - Ability to view all entries in database, add, remove, or modify entries (last one is coming soon hopefully lol... fml)
#       - Initial database connection (persistent)
#       - Will also create credentials on setup (May move this to another class tbh since it's not super relevant to the database class)


import mysql.connector
from mysql.connector import errorcode
from modules.menu import Menu
from modules.hash import Hash
import time

class Database(object):
    connection = None
    database_menu = Menu()
    logo = Menu.MainLogo
    
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
                pass
            
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
            cursor.execute(create_database_sql)
        except Exception as error:
            print(error)
        else:
            database_created = True
            
        if database_created == True:
            if Database.checkDatabase(self, 'passwordmanagerlite') == True:
                print("The database has been created successfully and validated...")
                time.sleep(1)
                try:
                    cursor.execute(create_master_table_sql)
                    cursor.execute(create_passwords_table_sql)
                except Exception as error:
                    print(error)
                else:
                    tables_created = True

        if tables_created == True:
            if Database.checkTables(self, 'passwords', 'mastercredentials') == True:
                print("The tables have been successfully created and validated...")
            else:
                print("There was an error creating the tables, please try again...")
                
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
        password = input("Please type in your master password: ")
        hashobj = Hash()
        hashed_pw = hashobj.hashPassword(password)
        credentials_created = False
        
        params = [username, hashed_pw]
        sql = """
            INSERT INTO passwordmanagerlite.mastercredentials (masterUsername, masterPassword)
            VALUES(%s,%s)
            """
        try:
            cursor = Database.connection.cursor()
            cursor.execute(sql, (params[0],params[1]))
            Database.connection.commit()
            time.sleep(1)
        except mysql.connector.Error as error:
            print(error)
        else:
            credentials_created = True
            return credentials_created
        
           
    # Get all entries from database
    def viewEntries(self):
        
        execute_string = 'SELECT * FROM `passwordmanagerlite`.`passwords`;'
        cursor = Database.connection.cursor()
        cursor.execute(execute_string)
        database_entries = cursor.fetchall()
        Database.logo
        print(f"{'ID':<5}{'Username':<20}{'Password':<35}{'Email':<25}{'Url':<20}")
        print('='*110)
        for row in database_entries:
            print(f"{row[0]:<5}{row[1]:<20}{row[2]:<35}{row[3]:<25}{row[4]:<20}")
        print("\n")
         
    # Add entries to database
    def addEntries(self):
        
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
            print("Committed successfully")
    
    # Remove entries from database
    def removeEntries(self):
        Database.logo
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
        pass