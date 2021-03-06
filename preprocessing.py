import pandas as pd
import numpy as np
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.decomposition import PCA


class Preprocessing:
    """
    Preprocessing utility fonction
    """

    def get_onehot_data(self, dataset):
        onehot_data = OneHotEncoder(dtype=int).fit_transform(
            dataset[['state', 'country', 'industry', 'sector']])

        onehot_data = pd.DataFrame(onehot_data.A)

        return onehot_data

    def get_var_data(self, dataset):
        var0 = dataset["Close0"] / dataset["Open0"] - \
            np.ones(dataset["Close0"].shape[0])

        var1 = dataset["Close1"] / dataset["Open1"] - \
            np.ones(dataset["Close1"].shape[0])

        var_height_low = dataset["High0"] / dataset["Low0"] - \
            np.ones(dataset["High0"].shape[0])

        return pd.DataFrame({"var0": var0, "var1": var1, "var_height_low": var_height_low})

    def get_normalized_volume(self, dataset):
        normalized_volume = (
            dataset["Volume0"] - dataset["Volume0"].mean()) / np.sqrt(dataset["Volume0"].var())

        normalized_volume = pd.DataFrame(
            {"normalized_volume": normalized_volume})

        return normalized_volume

    def get_normalized_date(self, dataset):
        normalized_day = dataset["day"] / 31
        normalized_month = dataset["month"] / 12

        return pd.DataFrame({"normalized_day": normalized_day, "normalized_month": normalized_month})


class Preprocessing1(Preprocessing):
    def get(self, dataset):
        """
        Preprocessing pipeline
        """

        print("Cleaning...")
        dataset = dataset.dropna(subset=['Open0', 'High0', 'Low0', 'Close0',
                                         'Volume0', 'Open1', 'Close1']).reset_index().drop_duplicates()

        index = dataset[["symbol", "longName"]]

        print("Refactoring...")
        onehot_data = self.get_onehot_data(dataset)
        var_data = self.get_var_data(dataset)
        normalized_volume = self.get_normalized_volume(dataset)
        normalized_date = self.get_normalized_date(dataset)

        dataset = onehot_data.join(var_data).join(
            normalized_volume).join(normalized_date)

        Y = dataset["var1"]

        print("PCA...")
        pca = PCA(n_components=80)
        X = pca.fit_transform(dataset.drop(columns="var1"))

        print("standardize...")
        standardizer = StandardScaler()
        X = standardizer.fit_transform(X)

        X = pd.DataFrame(X)

        return index, X, Y


def main():
    dataset = pd.read_csv("dataset.csv", sep=";")
    index, X, Y = Preprocessing1().get(dataset)

    print(index.head())
    print(Y.head(5))
    print(X.head(5))


if __name__ == "__main__":
    main()
