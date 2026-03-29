import pandas as pd
import re

def replace_github_and_codeberg_url(input_string):
    # I am doing github.com because platform really 
    # doesn't matter to the classification algorithm.
    input_string = str(input_string)
    input_string = re.sub(
        r"https?://(?:www\.)?github\.com/[^/\s]+/[^/\s]+(?:[^\s]*)?",
        "https://example.com/example/example",
        input_string
    )
    input_string = re.sub(
        r"https?://(?:www\.)?codeberg\.org/[^/\s]+/[^/\s]+(?:[^\s]*)?",
        "https://example.com/example/example",
        input_string
    )
    input_string = re.sub(
        r"github/[^/\s]+/[^/\s]+(?:[^\s]*)?",
        "https://example.com/example/example",
        input_string
    )

    return input_string

def process_file(file_name):
    df = pd.read_parquet(file_name)
    df = df.map(replace_github_and_codeberg_url)
    df.to_parquet(file_name, index=False)

process_file("training_data/testing_data.parquet")
process_file("training_data/training_data.parquet")
