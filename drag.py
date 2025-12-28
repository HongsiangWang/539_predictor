from collections import Counter
import numpy as np
import pandas as pd
import argparse
from utils import load_539_data
import matplotlib.pyplot as plt
import os
# --- Load Data ---


def build_drag_lists(data, period=1, total_data_num=100):
    data = data[data.shape[0]-total_data_num:]  # last 500 rows only
    drag_list = [[] for _ in range(5)]
    locator_array = data[-period]
    for i in range(data.shape[0] - period):
        row = data[i]
        for j in range(5):
            if int(row[j]) == int(locator_array[j]):
                drag_list[j].append(data[i + period])
    return locator_array, [np.array(lst) if len(lst) > 0 else np.array([]) for lst in drag_list]


def compute_counts(arr):
    if arr.size == 0:
        return [(n, 0) for n in range(1, 40)], []
    values = arr.flatten()
    values = values[(values >= 1) & (values <= 39)].astype(int)
    counts = Counter(values.tolist())
    all_counts = [(n, counts.get(n, 0))
                  for n in range(1, 40)]                # ordered by number
    # sorted by count desc, number asc
    sorted_counts = sorted(all_counts, key=lambda x: (-x[1], x[0]))
    return all_counts, sorted_counts


def get_drag_results(data: np.ndarray, period: int = 1, total_data_num=100):
    """
    Return list of dicts for positions 0..4:
      {"idx": int, "all_counts": [(num,count)...], "sorted_counts": [(num,count)...], "list": np.array}
    """
    locator_array, drag_arrays = build_drag_lists(
        data, period=period, total_data_num=total_data_num)
    results = []
    for idx, arr in enumerate(drag_arrays):
        all_counts, sorted_counts = compute_counts(arr)
        results.append({
            "idx": idx,
            "list": arr,
            "all_counts": all_counts,
            "sorted_counts": sorted_counts
        })
    return locator_array, results


def main(argv=None):
    parser = argparse.ArgumentParser(
        description="Compute drag lists counts for positions 0..4")
    parser.add_argument("--period", type=int, default=1,
                        help="period (lookback) to use for locator")
    args = parser.parse_args(argv)

    DATA = load_539_data()
    locator, results = get_drag_results(DATA, period=args.period)
    print("Locator (period={}): {}".format(args.period, locator))
    for r in results:
        print(f"\n--- position {r['idx']} ---")
        print("Top sorted (num:count):")
        for num, cnt in r["sorted_counts"]:
            print(f"{num}: {cnt}")
    return results


if __name__ == "__main__":
    main()
