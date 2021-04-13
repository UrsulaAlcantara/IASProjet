import yfinance as yf
import pandas as pd
import datetime

SYMBOLS_FILE = "symbols.csv"
DATASET_FILE = "dataset.csv"


def get_financial_data(start):
    end = (datetime.date.fromisoformat(start) +
           datetime.timedelta(days=2)).isoformat()

    symbols_df = pd.read_csv(SYMBOLS_FILE, sep=";")
    symbols_array = symbols_df["upper_case"].values

    sentence = " ".join(symbols_array)
    data = yf.download(sentence, start=start, end=end, group_by="ticker")

    data = [data.iloc[i].unstack(level=1) for i in range(2)]
    data = data[0].join(data[1], lsuffix='0', rsuffix='1')

    data.index = data.index.set_names('symbol')

    return data


def main():
    info_data = pd.read_csv("info_data.csv", sep=";").set_index("symbol")
    financial_data = get_financial_data("2021-02-01")

    dataset = info_data.join(financial_data)

    dataset.to_csv("dataset.csv", sep=";")


if __name__ == "__main__":
    main()
