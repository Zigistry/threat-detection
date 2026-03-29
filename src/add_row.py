import sys

import pandas as pd

print("enter readme content: ")
readme_content = sys.stdin.read()
if_is_valid_repo = input("enter if it is a valid repo: ")


df = pd.read_parquet("./training_data/training_data.parquet")


readme_content = readme_content.replace("\n", " ").replace("\r", " ")

row_to_add = pd.DataFrame(
    {"readme_content": [readme_content], "if_is_valid_repo": [if_is_valid_repo]}
)

df = pd.concat([df, row_to_add], ignore_index=True)

df.to_parquet("./training_data/training_data.parquet", index=False)
