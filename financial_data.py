import yfinance as yf
import pandas as pd
import datetime
import random
random.seed()

SYMBOLS_FILE = "symbols.csv"
DATASET_FILE = "dataset.csv"


def get_financial_data(start_date, days=2):
    start = start_date.isoformat()
    end = (start_date + datetime.timedelta(days=days)).isoformat()

    symbols_df = pd.read_csv(SYMBOLS_FILE, sep=";")
    symbols_array = symbols_df["upper_case"].values

    sentence = " ".join(symbols_array)
    data = yf.download(sentence, start=start, end=end, group_by="ticker")

    data = [data.iloc[i].unstack(level=1).add_suffix(str(i))
            for i in range(days)]

    result = data[0]
    result["day"] = start_date.day
    result["month"] = start_date.month
    result["year"] = start_date.year

    for i in range(1, days):
        result = result.join(data[i])

    result.index = result.index.set_names('symbol')

    return result


def get_n_days_random_financial_data(n):
    print("-----------------{} restants--------------{}".format(n, datetime.datetime.now().time()))

    start_date = datetime.date(2020, 1, 1)

    result = None
    try:
        result = get_financial_data(
            start_date + datetime.timedelta(random.randint(0, 365)))
    except IndexError:
        print("Error")
        return get_n_days_random_financial_data(n)

    if (n > 0):
        return result.append(get_n_days_random_financial_data(n - 1))

    return result


def main():
    info_data = pd.read_csv("info_data.csv", sep=";").set_index("symbol")
    financial_data = get_n_days_random_financial_data(20)

    dataset = info_data.join(financial_data)

    print(dataset.info())

    dataset.to_csv("dataset.csv", sep=";")


if __name__ == "__main__":
    main()
