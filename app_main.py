# -*- coding: utf-8 -*-
r"""專案架構與環境:
  app_main.py               - PySide6 GUI 與 smoke test 入口，會載入 app_*.py、app_workers.py。
  app_constants.py          - Excel 欄位與 user_data 路徑 helper（包含 runtime root）。
  app_excel.py              - Excel 自動讀取/修正，支援 openpyxl。
  app_timetable_logic.py    - 建構時間表矩陣與遮罩、檢查衝堂、計算 slot。
  app_user_data.py          - 在 user_data/user_schedules/<username> 下管理 history、best_schedule、best_schedule_cache.json。
  app_utils.py              - 數字/字串/ID/路徑等共用工具。
  app_widgets.py            - 訂製 Qt 控制項（FavoritesTableWidget、結果視圖等）。
  app_workers.py            - 背景 Worker（計算排課表、儲存）。
  user_data/
    user_schedules/         - 所有使用者 I/O 資料（history、best_schedule、cache、快取、log）           
  dist/                     - PyInstaller 輸出資料夾（包含 exe，user_data 需在清理時保留）。
ENV_NAME = course_query
prefix = C:\Users\x1064\.conda\envs\course_query

輸入/輸出說明:
  輸入: 按「讀入 Excel 課表」跳出檔案對話，預設使用 2025_1_16_課程.xls，會以 app_constants.REQUIRED_COLUMNS 檢查欄位。
  輸出: 內部儲存於 user_data/user_schedules/<sanitize username> 下的 history、best_schedule、best_schedule_cache.json 及其他快取。
  一切 I/O（設定、log、資料、暫存）都應在 user_data/ 下：
    - 開發期：<workspace root>\user_data\
    - 打包後：<EXE 所在資料夾>\user_data\
    - 有舊有 user_schedules 資料請自行移至 user_data/user_schedules，不要在程式中修改既有檔案。

從零開始的安裝流程:
  # 先進入 Anaconda base
  call "C:\ProgramData\Anaconda3\Scripts\activate.bat" "C:\ProgramData\Anaconda3"
  call conda activate base
  # 建立並啟用 course_query 環境
  call conda create --prefix "C:\Users\x1064\.conda\envs\course_query" python=3.11 -y
  call conda activate "C:\Users\x1064\.conda\envs\course_query"
  # 安裝 PySide6 GUI、資料分析套件與 PyInstaller（conda-forge 來源）
  call conda install -y python=3.11 PySide6 pandas numpy openpyxl pyinstaller -c conda-forge
  # 產生 requirements.txt
  python -m pip list --format=freeze > requirements.txt
  # 若需要從 requirements 安裝
  pip install -r requirements.txt
  # 執行 GUI
  python app_main.py

requirements.txt 安裝流程:
  # 已在 course_query 環境
  pip install -r requirements.txt
  python app_main.py

測試方式:
  # smoke test（請至少在改動後、打包前各跑一次）
  python app_main.py

user_data 與 dist 清理:
  - dist 清理只能移除 user_data/ 以外的檔案；若需保留資料請放入 user_data/。
  - 打包後 exe 與 user_data/ 同層，清理時務必保留 user_data/。

打包與命名:
  - EXE_NAME = workspace root 的資料夾名稱（師大課程查詢系統），打包出品需以此命名。
  - 可直接複製以下指令：
    pyinstaller --noconfirm --clean --windowed --onefile --name "師大課程查詢系統" app_main.py
"""

from __future__ import annotations

import sys
import traceback

from PySide6.QtCore import QTimer
from PySide6.QtWidgets import QApplication, QMessageBox

from app_mainwindow import MainWindow


def main() -> int:

    smoke_test = "--smoke-test" in sys.argv[1:]

    qt_args = [sys.argv[0]] + [arg for arg in sys.argv[1:] if arg != "--smoke-test"]

    app = QApplication(qt_args)

    try:
        w = MainWindow()
        w.show()

        if smoke_test:
            QTimer.singleShot(400, app.quit)

        return app.exec()

    except Exception:
        error_message = f"發生未預期的嚴重錯誤，應用程式即將關閉。\n\n錯誤資訊：\n{traceback.format_exc()}"
        QMessageBox.critical(None, "應用程式錯誤", error_message)
        return 1

if __name__ == "__main__":

    raise SystemExit(main())
