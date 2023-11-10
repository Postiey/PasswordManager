

class Menu(object):
    
    user_selection = ''
    
    def __init__(self):
        pass
    
    def MainLogo(self):
        bar = '=' * 31
        middle_text = "PasswordManagerLite"
    
        print(bar)
        print("|     " + middle_text + "     |")
        print(bar)
        
    def MainMenu(self):
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