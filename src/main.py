import fasttext
import pandas as pd


def main():
    df = pd.read_parquet("training_data/training_data.parquet")
    with open("./output.train.txt", "w") as output_train_file:
        for i, j in zip(df["label"], df["readme_content"]):
            output_train_file.write(i + " " + j + "\n")

    print("Hello from threat-detection!")


if __name__ == "__main__":
    main()
