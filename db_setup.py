import sqlite3
import json
from pathlib import Path


def setup(dbFile):
    connection = sqlite3.connect(dbFile)

    cursor = connection.cursor()

    cursor.execute("PRAGMA foreign_keys = ON;")

    cursor.executescript('''
        CREATE TABLE IF NOT EXISTS budget (
                budgetID INTEGER PRIMARY KEY AUTOINCREMENT,
                date TEXT UNIQUE NOT NULL 
                );
                        
        CREATE TABLE IF NOT EXISTS categories (
                categoryID INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT UNIQUE
                );

        CREATE TABLE IF NOT EXISTS monthly_budget (
                budgetID INTEGER,
                categoryID INT,
                budget INT,
                FOREIGN KEY (categoryID) REFERENCES categories (categoryID)
                    ON DELETE CASCADE
                    ON UPDATE CASCADE,
                FOREIGN KEY (budgetID) REFERENCES budget (budgetID)
                    ON DELETE CASCADE
                    ON UPDATE CASCADE
                );
        
        CREATE TABLE IF NOT EXISTS transactions (
                transactionID INTEGER PRIMARY KEY AUTOINCREMENT,
                categoryID INT,
                name TEXT,
                amount REAL,
                date TEXT,
                FOREIGN KEY (categoryID) REFERENCES categories (categoryID) 
                    ON DELETE SET NULL
                    ON UPDATE CASCADE
                );                 
                ''')

    connection.commit()
    connection.close()


def pull_data(transactions,category,unique=False):
    with open(transactions, 'r') as data_file:
        data = json.load(data_file)
    if unique:
        list_categories = set()
    else:
        list_categories = []
    if category == 'all':
        for row in data:
            if row['Transaction Category'] == "" or row['Transaction Category'] == None:
                row['Transaction Category'] = 'Other'
            list_categories.append(row)
        return list_categories
    else:
        for row in data:
            if row[category]:
                list_categories.add((row[category],))
                if row[category] == None:
                    list_categories.add('')
        return list(list_categories)
    

def pull_categories(transactions):
    cat = pull_data(transactions,'Transaction Category',unique=True)
    return cat 

def pull_months(transactions):
    dates = pull_data(transactions, 'Posting Date', unique=True)
    print(dates)
    monthSet = set((date[0][:7],) for date in dates)
    months = list(monthSet)
    print(months)
    return months

def initialize_budget_categories(db, transactions):
    conn = sqlite3.connect(db)
    cursor = conn.cursor()
    cursor.execute("PRAGMA foreign_keys = ON;")

    categories = pull_categories(transactions)
    months = pull_months(transactions)
    print(categories)
    print(months)

    categories_query = """
    INSERT OR IGNORE INTO categories (name)
    VALUES (?)
    """

    budget_query = """ 
    INSERT OR IGNORE INTO budget (date)
    VALUES (?)
    """

    try:
        cursor.executemany(categories_query,categories)
        cursor.executemany(budget_query,months)
        conn.commit()
        print("Success importing")
    except sqlite3.Error as e:
        print(f"Error occurred: {e}")
        conn.rollback()
    finally:
        conn.close()

def add_transactions(db,categories_name,data):
    conn = sqlite3.connect(db)
    cursor = conn.cursor()
    results = {}
    category_name_list = [row for row in categories_name]
    category_name_list.append(('Other',))
    print(category_name_list)
    for cat in category_name_list:
        print(cat)
        cursor.execute("SELECT categoryID FROM categories WHERE name = ?", cat)
        result = cursor.fetchone()
        if result:
            results[cat[0]] = result[0]

    transaction_query = """
    INSERT INTO transactions (categoryID, name, amount, date)
    VALUES (?, ?, ?, ?)
    """
    print(len(data))
    i = 1
    for row in data:
        print(i)
        print(row)
        print(row.get('Description') + " " + row.get('Transaction Category') + " " + row.get('Posting Date'))
        i += 1
        
    transactions_to_insert = [
        (    
            results.get(row.get('Transaction Category'), row.get("Uncategorized")),
            row.get('Description'),
            row.get('Amount'),
            row.get('Posting Date')
        )
    for row in data
    ]

    try:
        cursor.executemany(transaction_query,transactions_to_insert)
        conn.commit()
        print("Successfully added")
    except sqlite3.Error as e:
        print(f"An error occurred: {e}")
        conn.rollback()
    finally:
        conn.close()
    return results

def add_monthly_budget(db,cat_id_dict):
    conn = sqlite3.connect(db)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM budget;")
    budgets = cursor.fetchall()

    month_budget_query = """
    INSERT OR IGNORE INTO monthly_budget (budgetID, categoryID, budget)
    VALUES (?, ?, ?)
    """
    budget_month_totals = {'Groceries': 400, 'Entertainment': 150, 'Other Expenses' : 300, 'Restaurants & Dining': 100, 'Shopping': 100, 'Gasoline/Fuel': 200, 'Travel & Commute': 50, 'Loan Payments': 100, 'Healthcare & Pharmacy': 25, 'Clothing': 50, 'Hobbies': 75, 'Education': 200, 'Other': 100, 'Other Income': 25}
    insert_rows = []
    for month in budgets:
        for cat in cat_id_dict:
            insert_rows.append((month[0],cat_id_dict[cat],budget_month_totals[cat]))

    try:
        cursor.executemany(month_budget_query,insert_rows)
        conn.commit()
        print("Success")
    except sqlite3.Error as e:
        print(f"Error adding: {e}")
    finally:
        conn.close()

if __name__ == "__main__":
    db_file = Path("budget_fake_data.db")
    json_file = Path(input("Please provide a file to be added: "))
    data = pull_data(json_file,'all',False)
    categories = pull_categories(json_file)
    setup(db_file)
    initialize_budget_categories(db_file, json_file)
    cat_dict = add_transactions(db_file,categories,data)
    add_monthly_budget(db_file,cat_dict)