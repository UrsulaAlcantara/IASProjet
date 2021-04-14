import yfinance as yf
import pandas as pd
import datetime

SYMBOLS_FILE = "symbols.csv"
DATASET_FILE = "dataset.csv"


def get_financial_data(start, days=2):
    end = (datetime.date.fromisoformat(start) +
           datetime.timedelta(days=days)).isoformat()

    symbols_df = pd.read_csv(SYMBOLS_FILE, sep=";")
    symbols_array = symbols_df["upper_case"].values

    sentence = " ".join(symbols_array)
    data = yf.download(sentence, start=start, end=end, group_by="ticker")

    data = [data.iloc[i].unstack(level=1).add_suffix(str(i))
            for i in range(days)]

    result = data[0]
    for i in range(1, days):
        result = result.join(data[i])

    result.index = result.index.set_names('symbol')

    return result


def main():
    info_data = pd.read_csv("info_data.csv", sep=";").set_index("symbol")
    financial_data = get_financial_data("2021-02-01")

    dataset = info_data.join(financial_data)

    dataset.to_csv("dataset.csv", sep=";")


if __name__ == "__main__":
    main()
