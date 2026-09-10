import psycopg2

# Connection bnao
conn = psycopg2.connect(
    database = "bank_practice",
    user = "postgres",
    password = "mehak",
    host = "localhost",
    port = "5432"
)
print("Connected successfully! ")

cur = conn.cursor()

# Function define karo (execute sy pehly)
def create_account():
    name = input("Enter name: ")
    balance = input("Enter initial balance: ")
    city = input("Enter city: ")

    cur.execute("insert into accounts (name, balance, city) values (%s, %s, %s) returning id", (name, balance, city))
    new_id = cur.fetchone()[0]
    conn.commit()
    print(f"Account created successfully! Your account ID is {new_id}")

def deposit():
    acc_id = input("Enter account ID: ")
    amount = float(input("Enter amount to deposit: "))

    if amount <= 0:
        print("Error: Amount must be greater than zero.")
    else:
        cur.execute("update accounts set balance = balance + %s where id = %s", (amount, acc_id,))

    # transaction record add karo
        cur.execute("insert into transactions (account_id, type, amount) values (%s, %s, %s)", (acc_id, 'deposit', amount))

        conn.commit()
        print("Deposit successfully! ")

def withdraw():
    acc_id = input("Enter account ID: ")
    amount = float(input("Enter amount to withdraw: "))

    if amount <= 0:
        print("Error: Amount must be greater than zero.")
    else:
    # step #1: pehly current balance nikalo
        cur.execute("select balance from accounts where id = %s", (acc_id,))
        current_balance = cur.fetchone()[0]  # fetchone() ek row leta hai, [0] pehla column

    # step #2: Check karo
        if current_balance >= amount:
            # step 3: withdraw karo
            cur.execute("update accounts set balance = balance - %s where id = %s", (amount, acc_id))

            # transaction record add karo
            cur.execute("insert into transactions (account_id, type, amount) values (%s, %s, %s)", (acc_id, 'withdraw', amount))

            conn.commit()
            print("Withdraw successfully! ")
        else:
            # step 4: Error do
            print("Insufficient balance! ")

def check_balance():
    acc_id = input("Enter account ID: ")
    cur.execute("select * from accounts where id = %s", (acc_id,))
    row = cur.fetchone()
    if row:
        print(row)
    else:
        print("Account not found! ")

def transaction_history():
    acc_id = input("Enter account ID to see history: ")
    cur.execute("""
    select accounts.name, transactions.type, transactions.amount
    from accounts
    join transactions on accounts.id = transactions.account_id
    where accounts.id = %s
""", (acc_id,))
    rows = cur.fetchall()
    for row in rows:
        print(row)

def menu():
    while True:
        print("\n=====Bank Management System=====")
        print("1. Create Account")
        print("2. Deposite")
        print("3. Withdraw")
        print("4. Check Balance")
        print("5. Transaction History")
        print("6. Exit")

        choice = input("Enter your choice: ")

        if choice == '1':
            create_account()
        elif choice == '2':
            deposit()
        elif choice == '3':
            withdraw()
        elif choice == '4':
            check_balance()
        elif choice == '5':
            transaction_history()
        elif choice == '6':
            print("Thank you for using Bank Management System! ")
            break
        else:
            print("Invalid choice, try again.")

menu()

conn.close()





