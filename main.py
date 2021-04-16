from preprocessing import preprocessing
import pandas as pd


def main():
    dataset = pd.read_csv("dataset.csv", sep=";")

    index, X, Y = preprocessing(dataset)


if __name__ == "__main__":
    main()
