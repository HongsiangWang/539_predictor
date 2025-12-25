import pandas as pd


def load_data():
    df = pd.read_csv("lotteryHistory.csv")
    data = df.to_numpy()[::-1]
    return data[:, 1:].astype(int)


def load_data_full():
    df = pd.read_csv("lotteryHistory.csv")
    data = df.to_numpy()[::-1]
    return data
