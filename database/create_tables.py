from pathlib import Path
import sys

PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from database.connection import Database

db = Database()
db.connect()

cursor = db.connection.cursor()

schema = Path(__file__).resolve().parent / "schema.sql"
schema = schema.read_text(encoding="utf-8")

for statement in schema.split(";"):
    statement = statement.strip()

    if statement:
        cursor.execute(statement)

db.connection.commit()

cursor.close()
db.disconnect()

print("Tables Created Successfully")
