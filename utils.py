import pandas as pd


def load_539_data():
    df = pd.read_csv("data/539_history.csv")
    data = df.to_numpy()[::-1]
    return data[:, 1:].astype(int)


def load_539_data_full():
    df = pd.read_csv("data/539_history.csv")
    data = df.to_numpy()[::-1]
    return data


def load_fantasy5_data():
    df = pd.read_csv("data/fantasy5_history.csv")
    data = df.to_numpy()[::-1]
    return data[:, 1:].astype(int)


def load_fantasy5_data_full():
    df = pd.read_csv("data/fantasy5_history.csv")
    data = df.to_numpy()[::-1]
    return data
