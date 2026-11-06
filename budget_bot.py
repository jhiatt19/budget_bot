import mysql.connector

# load_dotenv()

# client = OpenAI()

# system_prompt_sql = """
# You are a SQLite expert. Your goal is to return sql syntax for the questions provided about a budget app.

# Database Schema:
# - Categories (categoryID, name)
# - Budget (date, budgetID) -- date always is in YYYY-MM-01 format
# - Monthly_Budget (budgetID, categoryID, budget)
# - Transactions (transactionID, categoryID, name, amount, date)

# Rules:
# 1) Transactions are linked to Categories through categoryID.
# 2) Monthly_Budget is linked to Categories through categoryID and is linked to Budget through budgetID.
# 3) Return ONLY SQL syntax, no explanation needed.
# 4) To get the transaction totals for a category for a specific month JOIN budget, categories, and transactions together and sum the amount columns. 
# 5) If the user says categories they want to know if any of the categoryID's, not if their is an actual category named categories.
# 6) Always return categories as category names not category ID's.
# 7) If one of the categories doesn't have any transactions one month make sure to calculate that value as a 0 in the average? So if I have a category that only has a transaction in December, still calculate it based on the total months.
# 8) Transacion.Amount column values and monthly_budget.budget column are in US dollars.
# 9) Total amount of spending in a month is determined by all the transaction amounts from a specific month. 
# 10) If a user asks for a month specific it usually means to use the monthly_budget table. There is no month table.
# """

# system_prompt_friendly = """
# You are a SQLite expert. Your goal is to return a friendly response that interprets the database response to a sql query.

# Database Schema:
# - Categories (categoryID, name)
# - Budget (date, budgetID) -- date always is in YYYY-MM-01 format
# - Monthly_Budget (budgetID, categoryID, budget)
# - Transactions (transactionID, categoryID, name, amount, date)

# Rules:
# 1) Transactions are linked to Categories through categoryID.
# 2) Monthly_Budget is linked to Categories through categoryID and is linked to Budget through budgetID.
# 3) Return a friendly simple response, do not ask if they would like a follow up question. Just answer the question that was asked.
# 4) To get the transaction totals for a category for a specific month JOIN budget, categories, and transactions together and sum the amount columns.
# 5) If the user says categories they want to know if any of the categoryID's, not if their is an actual category named categories.
# 6) Always return categories as category names not category ID's.
# """
# question = input("Please enter a question: ")
# secret = os.getenv("OPEN_AI_API")

db = mysql.connector.connect(
    host="127.0.0.1",
    user="j19",
    password="",
    database="budget"
)

cursor = db.cursor()
cursor.execute("SELECT DATABASE();")
record = cursor.fetchone()
print(f"Connected to database: {record[0]}")

cursor.close()
db.close()
# messages_sql= [
#         {"role": "system", "content": system_prompt_sql},
#         {"role": "user", "content": "Which month did I spend the least amount of money in?"},
#         {"role": "assistant", "content": "SELECT strftime('%Y-%m-01', T.date) AS budget_month, SUM(T.amount) AS total_expenses FROM Transactions T GROUP BY budget_month ORDER BY total_expenses ASC LIMIT 1;"},
#         {"role": "user", "content": question},
#         ]
# response = client.chat.completions.create(
#     model="gpt-5-nano",
#     messages= messages_sql
#     )
# sqlResponse = response.choices[0].message.content.strip()

# print(sqlResponse)

# databaseResponse = cursor.fetchall()
# print(databaseResponse)
# messages_friendly = [{"role": "system", "content": system_prompt_friendly},
#         ]
# messages_friendly.append({"role": "user", "content": question})
# messages_friendly.append({"role": "assistant", "content": "SQL query: {sqlResponse}"})
# messages_friendly.append({"role": "user", "content":f"Database response: {databaseResponse}"})




# response = client.chat.completions.create(
#     model="gpt-5-nano",
#     messages=messages_friendly
# )

# print(response.choices[0].message.content)