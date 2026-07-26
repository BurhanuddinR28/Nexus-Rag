import os
import sys
import psycopg2
from dotenv import load_dotenv
from fastembed import TextEmbedding
from pgvector.psycopg2 import register_vector

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from src.parser import parse_pdf

load_dotenv()

conn = psycopg2.connect(
    host="localhost",
    port=5432,
    dbname="nexusrag",
    user="postgres",
    password="nexuspass"
)
cursor = conn.cursor()

cursor.execute("CREATE EXTENSION IF NOT EXISTS vector")
conn.commit()
register_vector(conn)

cursor.execute("""
    CREATE TABLE IF NOT EXISTS documents (
        id SERIAL PRIMARY KEY,
        content TEXT,
        embedding vector(384),
        source TEXT
    )
""")
conn.commit()

model = TextEmbedding("BAAI/bge-small-en-v1.5")

chunks = parse_pdf("data_ingest/Sample Data 1.pdf")

for chunk in chunks:
    embedding = list(model.embed([chunk]))[0]
    cursor.execute(
        "INSERT INTO documents (content, embedding, source) VALUES (%s, %s, %s)",
        (chunk, embedding.tolist(), "Sample Data 1.pdf")
    )

conn.commit()
cursor.close()
conn.close()

print(f"Done. {len(chunks)} chunks stored in the database.")