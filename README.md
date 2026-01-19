# 師大課程查詢系統（course_query）

## (1) 專案概述
本專案提供課程查詢與課表處理功能，採用 Python 與 PyQt 進行開發。

## (2) workspace root 定義
workspace root 為本專案根目錄（含 app_main.py 同層）。  
所有檔案操作與腳本執行皆須在此層進行。

## (3) 檔案與資料夾結構
```text
course_query/
├── app_main.py
├── app_constants.py
├── app_excel.py
├── app_mainwindow.py
├── app_timetable_logic.py
├── app_user_data.py
├── app_utils.py
├── app_widgets.py
├── app_workers.py
├── requirements.txt
├── user_data/
├── dist/
└── build/
```

## (4) Python 檔名規則
- 主入口：app_main.py  
- 其他模組：app_*.py 皆與主程式同層。

## (5) user_data/ 規範
- 所有輸入、設定、快取與中間產物一律放於 user_data/ 下。  
- 預設輸出亦放置於 user_data/。

## (6) Conda 環境（ENV_NAME）規範
- 本專案唯一 conda 環境名稱：`course_query`
- 允許 `conda activate base` 作為入口，但嚴禁對 base 進行 install/remove。
- 嚴禁修改非 course_query 的任何 conda 環境。

## (7) 從零開始安裝流程
```bash
# 建立環境
conda create -n course_query python=3.10 -y
conda activate course_query

# 安裝依賴
pip install -r requirements.txt
```

## (8) requirements.txt
- 產生方式：
  ```bash
  python -m pip list --format=freeze > requirements.txt
  ```
- 安裝方式：
  ```bash
  pip install -r requirements.txt
  ```

## (9) 測試方式
```bash
python app_main.py
```
- 本專案啟動後應顯示 GUI 主畫面。
- 測試時應於 course_query 環境中執行。

## (10) 清理與白名單
保留項目：
- README.md  
- app_main.py, app_*.py  
- requirements.txt  
- user_data/, dist/  
- .git/, .gitignore  

可刪除項目（需確認後再刪）：
- build/, __pycache__/, *.pyc, .pytest_cache/

## (11) 打包成 .exe
- EXE 名稱：course_query.exe  
- 指令範例：
  ```bash
  pyinstaller --onefile --name course_query app_main.py
  ```
- 打包前請確保測試通過並清理暫存。

## (12) GitHub 操作指令
```bash
# 初始化
git init
git branch -M main
git remote add origin https://github.com/peicd100/course_query.git
git add .
git commit -m "Initial commit"
git push -u origin main

# 例行上傳
git status
git add .
git commit -m "Describe your changes"
git push

# 還原成 GitHub 最新資料
git fetch origin && git switch main && git reset --hard origin/main && git clean -fd && git status

# 查看儲存庫
git remote -v
```
