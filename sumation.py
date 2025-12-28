import numpy as np
from typing import Optional, Dict, Any

from parameters import COMBINATION
from utils import load_539_data


def convert_version(version: str) -> str:
    """Convert version code to a symbol for display.

    Supported versions: 'add', 'add+', 'diff', 'diff+'
    """
    mapping = {"add": ["-", "+"], "diff": ["+", "-"],
               "add+": ["+", "+"], "diff+": ["-", "-"]}
    if version not in mapping:
        raise ValueError(
            "version must be one of: 'add', 'add+', 'diff', 'diff+'")
    return mapping[version]


def scale(value: np.ndarray) -> np.ndarray:
    """Normalize numbers into 1..39 range, keep zeros.

    Works element-wise on numpy arrays or scalars.
    """
    value = np.array(value)
    return np.where(value > 0, (value - 1) % 39 + 1, 0)


def calculate(value: np.ndarray, add_number: int, version: str, combination_arr: np.ndarray) -> np.ndarray:
    """Compute candidate numbers based on the chosen 'version' and given combinations."""
    if version == "add":
        return np.array([scale(add_number - (value[i] + value[j]))
                         for i, j in combination_arr])
    elif version == "add+":
        return np.array([scale(add_number + (value[i] + value[j]))
                         for i, j in combination_arr])
    elif version == "diff":
        return np.array([scale(add_number + (value[i] - value[j]))
                         for i, j in combination_arr])
    elif version == "diff+":
        return np.array([scale(add_number - (value[i] - value[j]))
                         for i, j in combination_arr])
    else:
        raise ValueError(
            "version must be one of: 'add', 'add+', 'diff', 'diff+'")


def match_number(win_values: np.ndarray, candidate_values: np.ndarray) -> np.ndarray:
    """Compare winning numbers with candidates; return array of 0/1 matches."""
    return np.isin(candidate_values, win_values).astype(int)


def main_scripts(interval: int = 3,
                 position_period: int = 1,
                 add_number: int = 0,
                 continous: int = 3,
                 version: str = "diff",
                 data: Optional[np.ndarray] = None,
                 combination_arr: Optional[np.ndarray] = None) -> Optional[Dict[str, Any]]:
    """
    Core algorithm: scan history and return prediction when combination matches `continous` times.

    Accepts `data` and `combination_arr` so callers (like app.py) can share the same dataset.
    """
    # lazy-load data / combinations if caller didn't provide them
    if data is None:
        data = load_539_data()
    total_num = data.shape[0]
    if combination_arr is None:
        combination_arr = np.array(COMBINATION)

    if interval <= position_period or interval < 2:
        raise ValueError(
            "Invalid settings: interval must be > position_period and >= 2")

    match_lists = np.zeros(len(combination_arr), dtype=int)
    for i in range(1, continous + 1):
        period_count = total_num - (i * interval)
        win_set = data[period_count]
        position_set = data[period_count - position_period]
        candidate = calculate(position_set, add_number,
                              version, combination_arr)
        match_lists += match_number(win_set, candidate)

    # find combinations that matched `continous` times
    if np.any(match_lists == continous):
        right_index = np.where(match_lists == continous)[0]
        current_position_set = data[total_num - position_period]
        candidate = calculate(current_position_set, add_number, version, combination_arr)[
            right_index]
        candidate = scale(candidate)
        # ignore zero candidates
        if candidate.size > 0 and candidate[0] > 0:
            return {
                "interval": interval,
                "position": position_period,
                "continous": continous,
                "version": convert_version(version),
                "add": add_number,
                "predict": candidate.tolist(),
                "candidate": candidate,
                "combination": (combination_arr[right_index] + 1).tolist()
            }
    return None


if __name__ == "__main__":
    # quick sanity: print dataset size
    DATA = load_539_data()
    print("Loaded data shape:", DATA.shape)
