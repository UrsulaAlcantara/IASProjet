import pandas as pd
import numpy as np
from sklearn.preprocessing import OneHotEncoder
from sklearn.decomposition import PCA


def get_onehot_data(dataset):
    onehot_data = OneHotEncoder(dtype=int).fit_transform(
        dataset[['state', 'country', 'industry', 'sector']])

    onehot_data = pd.DataFrame(onehot_data.A)

    return onehot_data


def get_var_data(dataset):
    var0 = dataset["Close0"] / dataset["Open0"] - \
        np.ones(dataset["Close0"].shape[0])

    var1 = dataset["Close1"] / dataset["Open1"] - \
        np.ones(dataset["Close1"].shape[0])

    var_height_low = dataset["High0"] / dataset["Low0"] - \
        np.ones(dataset["High0"].shape[0])

    return pd.DataFrame({"var0": var0, "var1": var1, "var_height_low": var_height_low})


def get_normalized_volume(dataset):
    normalized_volume = (
        dataset["Volume0"] - dataset["Volume0"].mean()) / np.sqrt(dataset["Volume0"].var())

    normalized_volume = pd.DataFrame({"normalized_volume": normalized_volume})

    return normalized_volume


def preprocessing(dataset):
    dataset = dataset.dropna(subset=['Open0', 'High0', 'Low0', 'Close0',
                                     'Volume0', 'Open1', 'Close1']).reset_index()

    onehot_data = get_onehot_data(dataset)
    var_data = get_var_data(dataset)
    normalized_volume = get_normalized_volume(dataset)

    dataset = onehot_data.join(var_data).join(normalized_volume)

    Y = dataset["var1"]
    X = dataset.drop(columns="var1")

    return X, Y


def main():
    dataset = pd.read_csv("dataset.csv", sep=";")
    X, Y = preprocessing(dataset)
    print(Y.head(5), X.head())


if __name__ == "__main__":
    main()
