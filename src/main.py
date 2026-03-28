import os

import fasttext
import pandas as pd


def main():
    df = pd.read_parquet("training_data/training_data.parquet")
    with open("./output.train.txt", "w") as output_train_file:
        for i, j in zip(df["label"], df["readme_content"]):
            j = j.replace("\n", " ").replace("\r", " ")
            output_train_file.write(i + " " + j + "\n")

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


if __name__ == "__main__":
    main()
