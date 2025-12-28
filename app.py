from flask import Flask, request, render_template, url_for, session, redirect
import numpy as np
import pandas as pd
from parameters import PARAMS_LIST, COMBINATION
from utils import load_539_data, load_539_data_full, load_fantasy5_data, load_fantasy5_data_full
from drag import get_drag_results
from sumation import convert_version, main_scripts
import os

app = Flask(__name__)
# Change this to a secure key in production
app.secret_key = 'your_secret_key_here'


def get_data():
    game = session.get('game', '539')
    if game == '539':
        return load_539_data()
    else:
        return load_fantasy5_data()


def get_data_full():
    game = session.get('game', '539')
    if game == '539':
        return load_539_data_full()
    else:
        return load_fantasy5_data_full()


@app.route('/set_game/<game>')
def set_game(game):
    if game in ['539', 'fantasy5']:
        session['game'] = game
    return redirect(url_for('index'))


# --- Load Data ---
DATA = load_539_data()
TOTAL_NUM = DATA.shape[0]
COMBINATION_ARR = np.array(COMBINATION)


@app.route("/")
def index():
    data = get_data_full()
    data = data[::-1]
    game = session.get('game', '539')
    return render_template("index.html", data=data, game=game)


@app.route("/drag", methods=["GET", "POST"])
def stats():
    # compute drag lists and counts (same logic as drag.py results.append)
    if request.method == "POST":
        period_src = request.form
    else:
        period_src = request.args

    try:
        period = int(period_src.get("period", 1))
        if period < 1:
            period = 1
    except Exception:
        period = 1

    try:
        total_data_num = int(period_src.get("total_data_num", 100))
        if total_data_num < 100:
            total_data_num = 100
    except Exception:
        total_data_num = 100

    try:
        exclude_last = int(period_src.get("exclude_last", 0))
        if exclude_last < 0:
            exclude_last = 0
    except Exception:
        exclude_last = 0

    data = get_data()
    if exclude_last > 0:
        sliced_data = data[:-exclude_last]
    else:
        sliced_data = data

    try:
        locator_array, drag_results = get_drag_results(
            sliced_data, period=period, total_data_num=total_data_num)
    except Exception:
        locator_array, drag_results = [], []

    game = session.get('game', '539')
    return render_template("drag.html", locator_array=locator_array, drag_results=drag_results, period=period, total_data_num=total_data_num, exclude_last=exclude_last, game=game)


@app.route("/sumation", methods=["GET", "POST"])
def summation():
    results = []
    continous_default = 3
    exclude_last_default = 0
    if request.method == "POST":
        continous_input = request.form.get("continous")
        try:
            continous = int(continous_input)
        except:
            continous = continous_default
        exclude_last_input = request.form.get("exclude_last")
        try:
            exclude_last = int(exclude_last_input)
        except:
            exclude_last = exclude_last_default
    else:
        continous = continous_default
        exclude_last = exclude_last_default

    data = get_data()
    if exclude_last > 0:
        sliced_data = data[:-exclude_last]
    else:
        sliced_data = data

    for params in PARAMS_LIST:
        interval = params["interval"]
        position = params["position"]
        version = params["version"]

        predictions = []
        for add_number in range(78):
            res = main_scripts(interval, position, add_number,
                               continous, version, data=sliced_data, combination_arr=COMBINATION_ARR)
            if res:
                predictions.append(res)

        results.append({
            "interval": interval,
            "position": position,
            "continous": continous,
            "version": convert_version(version),
            "predictions": predictions
        })

    game = session.get('game', '539')
    return render_template("sumation.html", results=results, zip=zip, latest=sliced_data[-1], exclude_last=exclude_last, game=game)


if __name__ == "__main__":
    app.run(debug=True)
