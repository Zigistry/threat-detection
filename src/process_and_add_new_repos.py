# Basically this file will do this:
# I need to read the index_new_repo table
# then need to do a get request on their readme
# then check using my spam detector algo, wether
# the repo is safe to index or not.
# if repo is safe:
#     put it in safe_to_index_new_repo table
# if not:
#     put it in quarantined_repos table
import os
import sys

import fasttext
import libsql
import requests
from dotenv import load_dotenv

from tokenizer import replace_github_and_codeberg_url


def check_if_text_good(text, model):
    text = text.replace("\n", " ").replace("\r", " ")
    text = replace_github_and_codeberg_url(text)
    return model.predict(text)[0] == ("__label__good",)


def process_github_repo(owner_name, repo_name):
    url_to_process = f"https://api.github.com/repos/{owner_name}/{repo_name}/readme"
    headers = {
        "Accept": "application/vnd.github.v3.raw",
        "Authorization": f"Bearer {os.getenv('GH_API_KEY')}",
    }
    res = requests.get(url_to_process, headers=headers, timeout=10)

    if res.status_code == 404:
        return ""

    if res.status_code != 200:
        sys.exit(1)

    return res.text


def process_codeberg_repo(owner_name, repo_name):
    url_to_process = (
        f"https://codeberg.org/{owner_name}/{repo_name}/raw/branch/main/README.md"
    )
    res = requests.get(url_to_process, timeout=10)

    if res.status_code == 404:
        return ""

    if res.status_code != 200:
        sys.exit(1)

    if not res.text:
        return ""

    return res.text


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
        readme_text = ""
        if provider == "gh":
            readme_text = process_github_repo(owner_name, repo_name)
        else:
            readme_text = process_codeberg_repo(owner_name, repo_name)

        if readme_text == "" or check_if_text_good(readme_text, model):
            cursor.execute(
                "INSERT OR IGNORE INTO safe_to_index_new_repo VALUES (?, ?, ?)",
                (provider, owner_name, repo_name),
            )
        else:
            cursor.execute(
                "INSERT OR IGNORE INTO quarantined_repos VALUES (?, ?, ?)",
                (provider, owner_name, repo_name),
            )

    cursor.execute("DELETE FROM index_new_repo")

    connection.commit()


if __name__ == "__main__":
    main()
