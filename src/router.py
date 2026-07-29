# router.py
import psycopg2
from pgvector.psycopg2 import register_vector
# 1. Import psycopg2 and your DB connection details

# 2. Define a list of deterministic keywords:
#    ["how many", "count", "list all", "total"]
KEYWORDS = [
    "count",
    "how many",
    "number of rows",
    "list all",
]
# 3. Write a function called route(question):
#    - check if any keyword is in the question (lowercase)
#    - if yes → connect to DB, run the right query, return result
#    - if no → return {"path": "llm", "question": question}
def route(question):
    if any(keyword in question.lower() for keyword in KEYWORDS):
        conn = psycopg2.connect(
            host="localhost",
            port=5432,
            dbname="nexusrag",
            user="postgres",
            password="nexuspass"
        )
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM documents")
        result = cursor.fetchone()
        conn.close()
        return{"path": "deterministic", "result": result[0]}
    else:
        return {"path": "llm", "question": question}

# 4. Test it at the bottom:
#    print(route("how many chunks are stored?"))
#    print(route("what were Apple's total revenues?"))
print(route("how many chunks are stored?"))
print(route("what were apple's total revenue?"))