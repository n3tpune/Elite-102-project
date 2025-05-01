import mysql.connector # type: ignore
import random
import os
import time


#connecting to MySQL table
connection = mysql.connector.connect(
    user = 'python_connection',
    database = 'bank_user_info',
    password = 'password9('
)
cursor = connection.cursor()

#introduction (welcome message, present options, ask user where they want to go)
def intro():
    os.system('cls')
    print("Welcome to the SWAMP Bank, please input 1 - 6 to go to these options below or print '-1' to leave:")
    options = ['create an account', 'delete an account', 'modify an account', 'check balance', 'withdraw', 'deposit']
    for option in options:
        print(f"{str(options.index(option) + 1)}. {option}")
    return input("")

def uniqueRandint():
    sql = "SELECT PIN FROM user_info"
    cursor.execute(sql)
    temp = random.randint(123456, 1000000)

    #if temp in PIN row in user_info, then it creates another unqiue temp
    for pin in cursor:
        if pin == temp:
           temp = random.randint(123456, 1000000)
    return temp

def getRow(user_PIN):
    #gets a row (account) from user_info and returns it
    try:
        sql = "SELECT * FROM user_info WHERE pin = %s"
        val = [user_PIN]
        cursor.execute(sql, val)
        return cursor.fetchone()
    except:
        print("Please enter a valid PIN.")

def confirm():
    #confirms user_choice before going ahead, otherwise user goes back to menu
    user_choice = input("Are you sure you want to do this? (input 'yes' or 'no')\n").lower()
    if user_choice == 'yes':
        return True
    else:
        print("You will be returned to the main menu.")
        time.sleep(2)
        return main()

def creating_acc():
    user_name = input("Your first and last name: ")
    user_birth_date = input("Your birth date (mm/dd/yyyy): ")
    user_SSN = input("Your Social Security number (########): ")
    user_phone_number = input("Your phone number (##########): ")
    randomNum = uniqueRandint()

    #check user info
    if len(user_name) > 45:
        print("Please enter a name less than 45 characters.")
    if len(user_birth_date) > 10:
        print("Please enter a appropriate date.")
    if int(user_phone_number) > 9999999999:
        print("Please print an appropriate phone number.")

    if confirm():
        #send user info to MySQL
        sql = "INSERT INTO user_info (name, date, SSN, number, PIN, balance) VALUES (%s, %s, %s, %s, %s, %s)"
        val = (user_name, user_birth_date, user_SSN, user_phone_number, randomNum, 0)
        cursor.execute(sql, val)
        connection.commit()

        #prints all of user's account details
        counter = 0
        attributes = ['\nAccount Number', 'Name', 'Date', 'Social Security Number', 'Phone Number', 'PIN', 'Current balance']
        user_acc = getRow(randomNum)
        for item in user_acc:
            print(attributes[counter] + ": " + str(item))
            counter += 1
        
        print("\nWARNING: All of your account details will ONLY show when a new account is created.")
        input("Input anything to go back to the main menu: ")


def deleting_acc():
    print("we have to ask your PIN for security")
    user_PIN = input("PIN: ")
    
    if confirm():
        #tries to delete account with user_PIN, else it quits
        try:
            sql = "DELETE FROM user_info WHERE PIN = %s"
            val = [user_PIN]
            cursor.execute(sql, val)
            connection.commit()
            print("Your account is successfully been deleted.")
            time.sleep(2)
        except:
            print("Please enter a valid PIN.")
            quit()

def modify_acc():
    print("we have to ask your PIN for security")
    user_PIN = input("PIN: ")

    #prints all attributes in user_info
    print("\nPlease input one of the follwing attributes to modify your account: ")
    data = ['name', 'date', 'SSN (social security number)', 'number (phone number)']
    for attribute in data:
        print(attribute)

    #asks which attribute; and it's new and current value
    user_choice = input("\n").lower()
    user_confirm = input(f"What is the current {user_choice}: ")
    user_new = input(f"What would be the new {user_choice} be: ")

    #updates attribute to new value
    if confirm():
        try:
            sql = f"UPDATE user_info SET {user_choice} = %s WHERE PIN = %s AND {user_choice} = %s"
            val = [user_new, user_PIN, user_confirm]
            cursor.execute(sql, val)
            connection.commit()

            #if PIN is correct, print correctly changed otherwise hasn't
            if cursor == None:
                print("Please enter the valid information from before.")
            else:
                print(f"Your {user_choice} has been successfully changed.")
            time.sleep(2)
        except:
            print("Please enter the valid information from before.")
            quit()

def check_balance():
    print("we have to ask your PIN for security")
    try:
        user_PIN = int(input("PIN: "))
    except:
        print("Please enter a valid PIN.")

    if confirm():
        #gets account from user_PIN
        sql = "SELECT * FROM user_info WHERE pin = %s"
        val = [user_PIN]
        cursor.execute(sql, val)
        user_acc = cursor.fetchone()

    #prints balance from user_acc if correct PIN
    if cursor != None:
        print("SWAMP balance: " + str(user_acc[(len(user_acc)) - 1]))
        time.sleep(2)
    else:
        print("Please enter a valid PIN.")
        quit()

def change_balance(user_input):
    print("we have to ask your PIN for security")
    user_PIN = input("PIN: ")

    #gets account from user_PIN
    user_acc = getRow(user_PIN)

    #chaage balance by subtracting if user_input = 5, adding otherwise
    print()
    try:
        if user_input == '5':
            user_choice = int(input("How much do you want to withdraw from the SWAMP: "))
            new_balance = user_acc[(len(user_acc)) - 1] - user_choice
        else:
            user_choice = int(input("How much do you want to deposit into the SWAMP: "))
            new_balance = user_acc[(len(user_acc)) - 1] + user_choice
    except:
        print("Please enter the correction information.")
        quit()

    if confirm():
        #update balance with new balance
        sql = "UPDATE user_info SET balance = %s WHERE pin = %s"
        val = [new_balance, user_PIN]
        cursor.execute(sql, val)
        connection.commit()
        print("balance: " + str(new_balance))
        time.sleep(2)

def main():
    # send user where they wanna go from intro()
    user_input = intro()
    os.system("cls")
    #create a function for user to confirm their actions or go back to menu screen

    if user_input == "1":
        creating_acc()
        main()
    elif user_input == '2':
        deleting_acc()
        main()
    elif user_input == '3':
        modify_acc()
        main()
    elif user_input == '4':
        check_balance()
        main()
    elif user_input == '5' or user_input == '6':
        change_balance(user_input)
        main()
    elif user_input == '-1':
        print("Thank you for using the Elite Bank, come back soon!")
        quit()
    else:
        print("Please enter a suitable number.")

main()

#close connection to MySQL
cursor.close()
connection.close()
