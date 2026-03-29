import os

import fasttext
import pandas as pd


def paraquet_to_fasttext_kind_of_format(input_file, output_file):
    df = pd.read_parquet(input_file)
    with open(output_file, "w") as output_train_file:
        for i, j in zip(df["label"], df["readme_content"]):
            j = j.replace("\n", " ").replace("\r", " ")
            output_train_file.write(i + " " + j + "\n")


def main():
    paraquet_to_fasttext_kind_of_format(
        "training_data/training_data.parquet", "output.train.txt"
    )
    model = fasttext.train_supervised(
        input="./output.train.txt",
        epoch=50,
        lr=0.3,
        wordNgrams=2,
        dim=50,
        minCount=1,
        thread=os.cpu_count(),
        verbose=2,
    )
    model.save_model("model.bin")

    paraquet_to_fasttext_kind_of_format(
        "training_data/testing_data.parquet", "output.test.txt"
    )

    results = model.test("output.test.txt")

    print(results)


if __name__ == "__main__":
    main()
