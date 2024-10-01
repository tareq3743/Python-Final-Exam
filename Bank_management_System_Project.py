from datetime import date
import random

class Bank:
    def __init__(self, name, email, address) -> None:
        self.name = name
        self.email = email
        self.address = address
        self.Accounts = {}
        self.__Bank_Balance = 0
        self.__loan_balance = 0
        self.switch = True
        

    def add_Account(self, account):
        self.Accounts[account.id] = account
        print("Account Created Successfully!!")

    def delete_Account(self, id):
        if id in self.Accounts:
            self.Accounts.pop(id)
            print("Successfully Deleted!")
        else:
            print("Wrong Information!")

    def show_all_Account(self):
        print("AC_ID\t\tAC_NAME")
        for key, value in self.Accounts.items():
            print(f'{key}\t\t{value.name}')

    def check_bank_balance(self):
        return self.__Bank_Balance
    
    def set_bank_balance(self, balance):
        self.__Bank_Balance += balance

    def get_bank_balance(self, balance):
        self.__Bank_Balance -= balance

    def set_loan_balance(self, loan):
        self.__loan_balance -= loan

    def check_Bank_loan(self):
        return self.__loan_balance
    
    def loan_switch(self):
        print("1.Loan_System_off")
        print("2.Loan_System_ON")
        choice = int(input("Switch : "))
        if choice == 1:
            self.switch = False
            print("Load System OFf")
        elif choice == 2:
            self.switch = True
            print("Load System ON")
        else:
            print("Entered Wrong Number!!")

    

class Account(Bank):
    def __init__(self, name, email, address, account_type, id, bank) -> None:
        super().__init__(name, email, address)
        self.account_type = account_type
        self.__balance = 0
        self.__loan_balance = 0
        self.bank = bank
        self.id = id
        self.loan_count = 0
        self.transaction = []

    def show_transaction(self):
        print("Reason\t\t\tReceiver_id\t\t\tamount\t\t\tdate")
        for tns in self.transaction:
            print(f'{tns.reason}\t\t\t{tns.id}\t\t\t{tns.amount}\t\t\t{tns.date}')

    def check_Balance(self):
        return self.__balance
    
    def deposit(self, amount):
        self.__balance += amount
        self.bank.set_bank_balance(amount)
        self.reason = "Deposit"
        tns = self.Create_transaction(self.reason, self.id, amount, date.today())
        self.transaction.append(tns)


    def receive(self, amount):
        self.__balance += amount
        reason = "Received"
        tns = self.Create_transaction(reason, id, amount, date.today())
        self.transaction.append(tns)

    def withdraw(self, amount):
        if amount>self.__balance:
            print("Withdrawal amount exceeded!!")
        else:
            temp = self.bank.check_bank_balance()
            if temp>amount:
                self.__balance -= amount
                self.bank.get_bank_balance(amount)
                reason = "Withdraw"
                tns = self.Create_transaction(reason, self.id, amount, date.today())
                self.transaction.append(tns)
                print("Withdraw successfully!")
            else:
                print("Bank is bankrupt!!")

    def send_money(self, amount, id):
        if id in self.bank.Accounts:
            self.bank.Accounts[id].receive(amount)
            self.__balance -= amount
            reason = "SendMoney"
            tns = self.Create_transaction(reason, id, amount, date.today())
            self.transaction.append(tns)
            print("Money send Successfully!")
        else:
            print("Account does not exist")

    def set_loan_balance(self, loan):
        if self.loan_count <= 2:
            temp = self.bank.check_bank_balance() - self.__balance
            if temp > loan:
                self.__loan_balance -= loan
                self.__balance += loan
                self.bank.set_loan_balance(loan)
                self.loan_count += 1
                reason = "Loan"
                tns = self.Create_transaction(reason, self.id, loan, date.today())
                self.transaction.append(tns)
            else:
                print("Balance Limited!")
        else:
            print("You can take loan only two times!!\n\tThank You!!")

    def Create_transaction(self,reason, id, amount, date):
        tns = Transaction(reason, id, amount, date)
        return tns

class Transaction:
    def __init__(self, reason=0, receiver_id=0, amount=0, date=0) -> None:
        self.reason = reason
        self.id = receiver_id
        self.amount = amount
        self.date = date




bank = Bank("BD_Bank", "bd@gmail.com", "uttara, dhaka")
ac = Account("A", "towhidul@gmail.com", "U,D", "Savings", "1", bank)
ac1 = Account("B", "towhidul@gmail.com", "U,D", "Savings", "2", bank)
bank.add_Account(ac)
bank.add_Account(ac1)

def Create_Account():
    print("\n\t**Fillup The Form**")
    name = input("Name : ")
    email = input("Email : ")
    address = input("Address : ")
    account_type = input("Account_Type : ")
    id = f'{name[::1]}{random.randint(0,100)}'
    account = Account(name, email, address, account_type, id, bank)
    bank.add_Account(account)

def find_Account():
    name = input("Enter User Name : ")
    id = input("Enter ID : ")
    if id in bank.Accounts:
        if name == bank.Accounts[id].name:
            return bank.Accounts[id]
        else:
            return None
    else:
        return None

def User_Account_interface():
    print()
    currentUser = find_Account()
    if currentUser == None:
        print("Account doesn't exist")
    else:
        while True:
            print()
            print("1. Check Balance")
            print("2. Deposit Balance")
            print("3. Withdraw Balance")
            print("4. Send Balance")
            print("5. Get Loan")
            print("6. Check Transaction")
            print("7. Exit")
            choice = int(input("Enter choice : "))

            if choice == 1: 
                print("Account Balance : ", currentUser.check_Balance())
            elif choice == 2:
                balance = int(input("Enter Balance : "))
                currentUser.deposit(balance)
                print("Deposit successfully!")
            elif choice == 3:
                balance = int(input("Enter Balance : "))
                currentUser.withdraw(balance)
            elif choice == 4:
                id = input("Enter Receiver ID : ")
                balance = int(input("Enter Amount : "))
                currentUser.send_money(balance, id)
            elif choice == 5:
                if bank.switch == True:
                    balance = int(input("Enter Loan quentity : "))
                    currentUser.set_loan_balance(balance)
                else:
                    print("Loan System Not Available now!!")
            elif choice == 6:
                currentUser.show_transaction()
                pass
            else:
                print("Exit From User Account")
                break

def Admin_Account_interface():
    while True:
        print()
        print("1. Create New Account")
        print("2. Delete User Account")
        print("3. All Account List")
        print("4. Total_Bank_Balance")
        print("5. Check_Bank_loan")
        print("6. Loan ON_OFF")
        print("7. Exit")
        choice = int(input("Enter choice : "))

        if choice == 1:
            Create_Account()
        elif choice == 2:
            id = input("Enter User Account_id : ")
            bank.delete_Account(id)
        elif choice == 3:
            bank.show_all_Account()
        elif choice == 4:
            print("Total Bank Balance : ", bank.check_bank_balance())
        elif choice == 5:
            print("Total Bank Loan : ", bank.check_Bank_loan())
        elif choice == 6:
            bank.loan_switch()
        else:
            print("Admin Panel Exit Successfully")
            break


#Automation Start--->
while True:
    print()
    print("1. Admin")
    print("2. User")
    print("3. Exit")
    choice = int(input("Enter choice : "))
    
    if choice == 1 :
        Admin_Account_interface()
    elif choice == 2:
        User_Account_interface()
    else:
        print("Program is Closed!!")
        break

