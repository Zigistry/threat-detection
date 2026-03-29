# Basically this file will do this:
# I need to read the index_new_repo table
# then need to do a get request on their readme
# then check using my spam detector algo, wether
# the repo is safe to index or not.
# if repo is safe:
#     put it in repos table
# if not:
#     put it in quarantined_repos
import os

import fasttext
import libsql
import requests
from dotenv import load_dotenv


def process_github_repo(owner_name, repo_name, model):
    url_to_process = f"https://api.github.com/repos/{owner_name}/{repo_name}/readme"
    headers = {"Accept": "application/vnd.github.v3.raw"}
    res = requests.get(url_to_process, headers=headers)

    text_to_process = res.text.replace("\n", " ").replace("\r", " ")
    print(
        model.predict(text_to_process), f"https://github.com/{owner_name}/{repo_name}"
    )


def process_codeberg_repo(owner_name, repo_name):
    pass


def main():
    load_dotenv()
    model = fasttext.load_model("model.bin")
    connection = libsql.connect(
        database="zigistry.db",
        sync_url=os.getenv("DATABASE_URL"),
        auth_token=os.getenv("API_KEY"),
    )

    cursor = connection.cursor()
    cursor.execute("SELECT * FROM index_new_repo")
    rows = cursor.fetchall()

    for row in rows:
        provider, owner_name, repo_name = row[0].split("/")
        if provider == "gh":
            process_github_repo(owner_name, repo_name, model)
        else:
            process_codeberg_repo(owner_name, repo_name)


if __name__ == "__main__":
    main()
