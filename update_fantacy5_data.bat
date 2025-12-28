@echo off
REM ----------------------------
REM 啟動 conda 環境並執行 Flask
REM ----------------------------

REM 1. 初始化 conda（請改成你的 Anaconda 安裝路徑）
call C:\Users\user\anaconda3\Scripts\activate.bat

call conda activate 539
cd /d D:\workspace\539

REM update data and wait for completion
python update_fantacy5_data.py

exit