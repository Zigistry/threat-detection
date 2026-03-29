# Basically this file will do this:
# I need to read the index_new_repo table
# then need to do a get request on their readme
# then check using my spam detector algo, wether
# the repo is safe to index or not.
# if repo is safe:
#     put it in repos table
# if not:
#     put it in quarantined_repos
import libsql
import os
from dotenv import load_dotenv

load_dotenv()


def main():
    connection = libsql.connect(
        database="zigistry.db",
        sync_url=os.getenv("DATABASE_URL"),
        auth_token=os.getenv("API_KEY"),
    )

    cursor = connection.cursor()
    cursor.execute("SELECT * FROM index_new_repo")
    rows = cursor.fetchall()

    for row in rows:
        print(row)

if __name__ == "__main__":
    main()
