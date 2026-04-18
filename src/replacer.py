import pandas as pd

from tokenizer import replace_github_and_codeberg_url


def process_file(file_name):
    df = pd.read_parquet(file_name)
    df.loc[:, "readme_content"] = df["readme_content"].map(
        replace_github_and_codeberg_url
    )

    df.to_parquet(file_name, index=False)


process_file("training_data/testing_data.parquet")
process_file("training_data/training_data.parquet")
