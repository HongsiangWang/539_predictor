from flask import Flask, request, render_template, url_for
import numpy as np
import pandas as pd
from parameters import PARAMS_LIST, COMBINATION
from utils import load_data, load_data_full
from drag import get_drag_results
from sumation import convert_version, main_scripts
import os

app = Flask(__name__)


# --- Load Data ---
DATA = load_data()[1:]
TOTAL_NUM = DATA.shape[0]
COMBINATION_ARR = np.array(COMBINATION)


@app.route("/")
def index():
    data = load_data_full()
    data = data[::-1]
    return render_template("index.html", data=data)


@app.route("/drag")
def stats():
    # compute drag lists and counts (same logic as drag.py results.append)
    try:
        period = int(request.args.get("period", 1))
        if period < 1:
            period = 1
    except Exception:
        period = 1

    try:
        total_data_num = int(request.args.get("total_data_num", 100))
        if total_data_num < 100:
            total_data_num = 100
    except Exception:
        total_data_num = 100

    try:
        locator_array, drag_results = get_drag_results(
            DATA, period=period, total_data_num=total_data_num)
    except Exception:
        locator_array, drag_results = [], []

    return render_template("drag.html", locator_array=locator_array, drag_results=drag_results, period=period, total_data_num=total_data_num)


@app.route("/sumation", methods=["GET", "POST"])
def summation():
    results = []
    continous_default = 4
    if request.method == "POST":
        continous_input = request.form.get("continous")
        try:
            continous = int(continous_input)
        except:
            continous = continous_default
    else:
        continous = continous_default

    for params in PARAMS_LIST:
        interval = params["interval"]
        position = params["position"]
        version = params["version"]

        predictions = []
        for add_number in range(78):
            res = main_scripts(interval, position, add_number,
                               continous, version, data=DATA, combination_arr=COMBINATION_ARR)
            if res:
                predictions.append(res)

        results.append({
            "interval": interval,
            "position": position,
            "continous": continous,
            "version": convert_version(version),
            "predictions": predictions
        })

    return render_template("sumation.html", results=results, zip=zip, latest=DATA[-1])


if __name__ == "__main__":
    app.run(debug=True)
