import requests
import pandas as pd
import datetime
import numpy as np
import matplotlib.pyplot as plt
from bs4 import BeautifulSoup
from collections import defaultdict, Counter
from itertools import combinations

df = pd.DataFrame(columns=["date", "num1", "num2", "num3", "num4", "num5"])
# 開始從第一頁爬到第48頁
for i in range(1, 58):
    r = requests.get(
        "https://www.pilio.idv.tw/lto539/list539BIG.asp?indexpage=" + str(i) + "&orderby=new")
    r.encoding = 'utf-8'
    soup = BeautifulSoup(r.text, "html.parser")
    sel = soup.select("tr span")
    for j, s in enumerate(sel[2:]):
        if s["style"] == "font-size: 22px; font-weight: bold; color: #000000":
            dateStr = s.text.strip()[5:15]
            dt = datetime.datetime.strptime(dateStr, "%Y/%m/%d").date()
        if s["style"] == "font-size: 36px; font-weight: bold; color: #000000":
            numsStr = s.text.replace(" ", "").replace("\n", "")
            nums = numsStr.split()
            nums = [int(num[:2]) for num in nums]
        # 因為它每隔兩個才是我們要的資料
        if j % 2:
            dftmp = pd.DataFrame(
                [[dt] + nums], columns=["date", "num1", "num2", "num3", "num4", "num5"])
            df = pd.concat([df, dftmp], ignore_index=True)
# 將日期設為我們的index
df.set_index('date', inplace=True)
df.to_csv('lotteryHistory.csv', index=True)
