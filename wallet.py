import random
import sqlite3
from utilities import generate_account_no

connection = None

def connect():
    global connection
    if connection:
        raise RuntimeError("Connect() cannot be called twice!")
    connection = sqlite3.connect('file:cachedb?mode=memory&cache=shared') 
    cursor = connection.cursor()
    cursor.execute(""" CREATE TABLE IF NOT EXISTS users (
            CID INTEGER PRIMARY KEY,
            first_name TEXT,
            last_name TEXT,
            account_no INT,
            balance REAL DEFAULT 0.00,
            transaction_pin INT NOT NULL)""")
    connection.commit()

connect()

def menu_control(menu_option):
    if menu_option == 1:
        print("\nYour account has been created")
        add_user()
    elif menu_option == 2:
        account_no = input("\nEnter your account number:\n")
        transaction_pin = input("Enter your transaction pin:\n")

        cursor = connection.cursor()
        cursor.execute(f'SELECT account_no, transaction_pin, balance FROM users WHERE account_no = {account_no}')
        query = cursor.fetchone()
        if query is not None:
            if account_no == str(query[0]) and transaction_pin == str(query[1]):
                print("\nYou have successfully logged in!\n")
                log_in(query[0], query[1])
            else:
                print("\nInvalid account number or transaction pin!\n")
        else:
            print("\nInvalid account number or transaction pin!\n")
    elif menu_option == 0:
        print("\nBye!")
        exit()

def add_user():
    first_name = input("\nEnter your first name:\n")
    last_name = input("\nEnter your last name:\n")
    account_no = generate_account_no()
    transaction_pin = random.randint(1000, 9999)
    balance = 0.00

    cursor = connection.cursor()
    cursor.execute("""INSERT INTO users VALUES (NULL, ?, ?, ?, ?, ?)""", (first_name, last_name, account_no, balance, transaction_pin))
    connection.commit()
    print(f"Your account number:\n{account_no}\nYour transaaction_pin:\n{transaction_pin}\n")


def log_in(account_no, transaction_pin):
    log_menu = int(input("1. Balance\n"
                         "2. Deposit Funds\n"
                         "3. Transfer Funds\n"
                         "4. Close account\n"
                         "5. Log out\n"
                         "0. Exit\n"))

    if log_menu == 1:
        cursor = connection.cursor()
        cursor.execute(f'SELECT account_no, transaction_pin, balance FROM users WHERE account_no = {account_no}')
        query = cursor.fetchone()
        print(f"\nBalance: $ {query[2]}\n")
        log_in(account_no, transaction_pin)

    elif log_menu == 2:
        cursor = connection.cursor()
        funds_deposit = float(input("Enter deposit amount:\n"))
        cursor.execute(f'UPDATE users SET balance = balance + {funds_deposit} WHERE account_no = {account_no}')
        connection.commit()
        print("Deposit transaction was successfull!")
        log_in(account_no, transaction_pin)

    elif log_menu == 3:
        try:
            cursor = connection.cursor()
            reciever_acct_no = int(input("Enter reciever's 10 digit account number:\n"))
            amount = int(input("Enter transfer amount:\n"))
            
            # get sender account
            cursor.execute(f'SELECT account_no, balance FROM users WHERE account_no = {account_no}')
            sender_query = cursor.fetchone()

            # get reciever account
            cursor.execute(f'SELECT account_no, balance FROM users WHERE account_no = {reciever_acct_no}')
            reciever_query = cursor.fetchone()

            if reciever_query is None:
                print('Reciever account details is invalid.')

            if reciever_query !=  None:
                sender_balance = sender_query[1]
                receiver_balance = reciever_query[1]

                sql_sender_query = """UPDATE users SET balance = ? where account_no = ?"""
                sql_receiver_query = """UPDATE users SET balance = ? where account_no = ?"""

                # update user balances
                updated_balance_sender = sender_balance
                
                if sender_balance >= amount:
                    updated_balance_sender = sender_balance - amount
                    updated_balance_receiver = receiver_balance + amount

                    sender_data = (round(updated_balance_sender, 2), sender_query[0])
                    reciever_data = (round(updated_balance_receiver, 2), reciever_query[0])

                    cursor.execute(sql_sender_query, sender_data)
                    cursor.execute(sql_receiver_query, reciever_data)
                    connection.commit()
                    print('Transaction completed successfully.')

                else:
                    print('You have insufficient balance for this transaction')

        except sqlite3.Error as e:
            print("Transfer failed", e)

    elif log_menu == 4:
        cursor = connection.cursor()
        cursor.execute(f'DELETE FROM users WHERE account_no = {account_no}')
        connection.commit()
        print("Your account has been closed!")
        init()

    elif log_menu == 5:
        print("\nLog out successfull!\n")
        init()

    elif log_menu == 0:
        print("\nBye!")
        exit()

def init():
    print('\t')
    print('Welcome to Wafi Wallet!')
    menu = int(input("1. Create an account\n2. Log into account\n0. Exit\n"))
    menu_control(menu)

while True:
    init()
