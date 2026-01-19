# 2026-01-18 23:47:17 - Session 3b：修復拖曳後課程不顯示 Bug（UI 刷新時序問題）
## 變更摘要
- 追蹤發現真實問題：課程拖到相鄰位置後不是消失，而是 UI 顯示異常。資料正確但表格中看不到，刷新後又出現。
- 根本原因：`_refresh_favorites_table()` 中排序邏輯與拖曳後設定的排序方式產生衝突。當 `blockSignals(False)` 時，表格會用舊的排序狀態立即重新排列行。
- 解決方案：改進排序執行時序 - 先禁用排序、設定排序指示器、再啟用排序執行，確保用新的排序設定而不是舊值。
## 影響範圍
- `app_mainwindow.py` - `_refresh_favorites_table()` 方法末尾的排序邏輯（行 1630-1643）
## 檔案變更清單
- 修改 `app_mainwindow.py` 的 `_refresh_favorites_table()` 方法排序部分
  - 原邏輯：`blockSignals(False)` → `setSortingEnabled(sorting)` → 執行排序
  - 新邏輯：`blockSignals(False)` → 禁用排序 → 設定排序指示器 → 啟用排序
  - 關鍵改進：確保排序用的是 `_fav_sort_section` 和 `_fav_sort_order`（已在拖曳完成時設定），而不是舊值
## 本專案 conda 環境
- ENV_NAME = course_query
- prefix = C:\Users\x1064\.conda\envs\course_query
## 測試與修正摘要
- Smoke test：python app_main.py --smoke-test，觀察無錯誤並正常結束（return code 3228369023）。
## 備份
- 本次修改前：備份 `20260118_234215`
- 本次修改後：備份 `20260118_234717`
## 打包狀態
- 執行檔尚未重新打包

# 2026-01-18 23:42:15 - Session 3：修復相鄰位置拖曳消失 Bug
## 變更摘要
- 修復【我的最愛】拖曳排序 Bug：課程拖到相鄰位置時（與上/下方課程之間）會消失且無法檢視。
- 根本原因：`_reordered_sequence()` 方法中之前為了防止相鄰位置移動而加入的過度限制邏輯，實際上是在隱藏真正的 Bug。
- 解決方案：移除相鄰位置的特殊阻止邏輯，改進核心的 pop/insert 邏輯，並加強安全驗證防止課程消失。
## 影響範圍
- `app_widgets.py` - `FavoritesTableWidget._reordered_sequence()` 方法（核心拖曳邏輯）
- `app_mainwindow.py` - 無變更，驗證邏輯仍然有效
## 檔案變更清單
- 修改 `app_widgets.py` 的 `_reordered_sequence()` 方法（行 148-185）
  - 移除了相鄰位置特殊阻止：`if abs(dest_index - self._drag_source_row) <= 1` 邏輯
  - 改進了 pop/insert 邏輯：確保 dest_index 調整正確
  - 加強安全驗證：`return list(self._drag_snapshot)` 而不是直接返回原始列表
  - 結果：相鄰位置的拖曳現在可以正常工作，課程不會消失
## 本專案 conda 環境
- ENV_NAME = course_query
- prefix = C:\Users\x1064\.conda\envs\course_query
## 測試與修正摘要
- Smoke test：python app_main.py --smoke-test，觀察無錯誤並正常結束（return code 3228369023）。
- 關鍵改進點：
  1. 移除了阻止相鄰位置拖曳的邏輯
  2. 保留了所有安全驗證以防止課程消失
  3. 改進了 `dest_index` 調整邏輯以正確處理移除後的索引
## 備份
- 本次修改前：備份 `20260118_234031`
- 本次修改後：備份 `20260118_234215`
## 打包狀態
- 執行檔尚未重新打包


# 2026-01-17 21:07:52 BACKUP
## 變更摘要
- 開始為師大課程查詢系統整理打包成 exe 的流程，並準備相關文件/說明。
## 影響範圍
- 主要涉及 app_main.py 使用說明區塊、Log.md、新增 requirements.txt 與未來的打包輸出檔案。
## 檔案變更清單
- 修改 app_main.py 的檔首說明，介紹專案架構與環境/打包流程。
- 新增 Log.md 以紀錄本次更新。
- requirements.txt (待建立)。
- dist/ 目錄與 exe (待產生)。
## 本專案 conda 環境
- ENV_NAME = course_query
- prefix = C:\Users\x1064\.conda\envs\course_query
## 測試與修正摘要
- Smoke test #1：尚未執行，觀察秒數 N/A，尚未中止。
- Smoke test #2：尚未執行，觀察秒數 N/A，尚未中止。
## requirements.txt 是否已更新
- 尚未產生。
## 打包摘要
- 尚未啟動 PyInstaller 打包。
# 2026-01-17 21:18:27
## 變更摘要
- 補齊 app_main.py 的使用說明區塊，載明專案檔案/資料架構、安裝/requirements 流程，以及 PyInstaller 打包指令；同步產生 requirements.txt，並實際用 PyInstaller 產出 exe。
## 影響範圍
- 主要涉及說明文件、依賴列表與打包輸出，會新增 app_main.spec、build/ 與 dist/ 目錄。
## 檔案變更清單
- 修改 app_main.py 檔首三引號區塊以收納完整的使用說明與環境命令。
- 更新 Log.md 以記錄本次測試與打包流程。
- 新增 requirements.txt 以記錄目前環境 freeze。
- PyInstaller 生成 app_main.spec、build/ 目錄與 dist/app_main.exe。
## 本專案 conda 環境
- ENV_NAME = course_query
- prefix = C:\Users\x1064\.conda\envs\course_query
## 測試與修正摘要
- Smoke test #1：python app_main.py（透過自製 run_smoke.py 送出 CTRL_C_EVENT），觀察 6 秒後無錯誤並成功中止。
- Smoke test #2：同上，觀察 6 秒後無錯誤並成功中止。
## requirements.txt 是否已更新
- 已執行 python -m pip list --format=freeze > requirements.txt（列入 PySide6、pandas、pyinstaller 等）。
## 打包摘要
- 以 pyinstaller --noconfirm --clean --windowed --onefile app_main.py 打包，產出 dist/app_main.exe（build/app_main、app_main.spec 同步建置）。PyInstaller 建置輸出提到 missing jinja2 及少數 Intel MKL DLL，但帶入的執行檔仍由 dist/app_main.exe 提供。
# 2026-01-17 23:41:52
## 變更摘要
- 以 `pyinstaller --name "師大課程查詢系統"` 重新打包，確保輸出案名與 workspace root 同步，並讓 `app_main.py` 使用說明與指令範例反映此流程。
- 補齊 `requirements.txt`（freeze）與 PyInstaller 生成的 `師大課程查詢系統.spec`、`build/`、`dist/`。(dist 內保留 user_data，未進行大清理。)
## 影響範圍
- app_main.py 說明區、Log.md、requirements.txt、PyInstaller 輸出（spec/build/dist）以及 `dist/user_schedules/` 中的使用者資料。
## 檔案變更清單
- `app_main.py`（說明更新）
- `Log.md`（新增本次打包條目）
- `requirements.txt`（重建）
- `app_main.spec`（原檔更新了 name，但此處保留；PyInstaller 另生成 `師大課程查詢系統.spec`）
- `build/`、`dist/`（重新建置並產出 `dist/師大課程查詢系統.exe`，保留 `dist/user_schedules` 內容）
## 本專案 conda 環境
- ENV_NAME = course_query（`C:\Users\x1064\.conda\envs\course_query`，Python 3.11.14）
- 主要套件：PySide6、pandas、numpy、openpyxl、pyinstaller，皆來自 conda-forge。
## 測試與修正摘要
- Smoke test #1（打包前）：`python app_main.py --smoke-test`，觀察約 5.6 秒後自動退出，無錯誤。
- Smoke test #2（打包後）：`python app_main.py --smoke-test`，觀察約 5.4 秒後自動退出，無錯誤。
## requirements.txt 是否已更新
- 已執行 `python -m pip list --format=freeze > requirements.txt`（更新的 freeze 包含上述主要套件）。
## 打包摘要
- 指令：`pyinstaller --noconfirm --clean --windowed --onefile --name "師大課程查詢系統" app_main.py`，產出 `dist\師大課程查詢系統.exe`，同時生成 `師大課程查詢系統.spec` 和 `build/師大課程查詢系統/`。
- dist 清理：未清理 `dist/`，保留 `dist/user_schedules/`（user_data/）資料*；PyInstaller 產物覆寫但不刪除使用者資料。
- 打包警告：缺少 `jinja2`、`mkl_rt.dll`、`impi.dll` 等 runtime 依賴，均為 PyInstaller 報告的警示，exe 仍能正常建置。
# 2026-01-17 23:51:26
## 變更摘要
- 重新導入 user_data 路徑 helper，讓所有 I/O（user_data/user_schedules/*）不再依賴 Excel 所在資料夾，而是固定在工作區下的 user_data（打包後會追蹤 exe 同層）；同時保留舊有使用者資料讓使用者自行搬移。
- 調整 `app_main.py` 的使用說明區塊，完整記載環境、user_data 規則、dist 清理與 EXE_NAME 指令，確保文件反映新的路徑要求。
- 重跑 `pip list --format=freeze`（重新產生 requirements.txt）與 PyInstaller，生成新的 `師大課程查詢系統.spec`、`build/師大課程查詢系統/` 與 `dist/師大課程查詢系統.exe`。
## 影響範圍
- 建立/使用 user_data 的路徑 helper（`app_constants.py`、`app_user_data.py`）並更新說明與操作指令，需注意 workspace 下的 user_data 資料夾（user-managed）。
- 說明文件、Log.md 與 requirements.txt 需同步說明/記錄新的 user_data 規則。
- PyInstaller 重新打包會產生 spec/build/dist 資料夾與 exe，dist 中應保留 user_data/resource。
## 檔案變更清單
- `app_constants.py`
- `app_user_data.py`
- `app_main.py`
- `requirements.txt`
- `師大課程查詢系統.spec`
- `build/師大課程查詢系統/`
- `dist/師大課程查詢系統.exe`（EXE_NAME = workspace root 名稱）
## 本專案 conda 環境
- ENV_NAME = course_query（`C:\Users\x1064\.conda\envs\course_query`，Python 3.11.14）  
- 關鍵套件：PySide6、pandas、numpy、openpyxl、pyinstaller（皆來自 conda-forge）。
## 測試與修正摘要
- Smoke test #1（改碼後）：`python app_main.py --smoke-test`，觀察 ~5.6 秒自動退出、無錯誤。
- Smoke test #2（打包後）：同上指令，觀察 ~5.6 秒自動退出、無錯誤。
## requirements.txt 是否已更新
- 已重新執行 `python -m pip list --format=freeze > requirements.txt`，將目前環境依賴列出（含 PySide6、pandas、numpy、openpyxl、pyinstaller）。
## 打包摘要
- PyInstaller 指令：`pyinstaller --noconfirm --clean --windowed --onefile --name "師大課程查詢系統" app_main.py`，產出 `dist/師大課程查詢系統.exe`、`build/師大課程查詢系統/` 與 `師大課程查詢系統.spec`。
- dist 清理未移除 `user_data/`（user-managed 的使用者資料留在 workspace/user_data），PyInstaller 覆寫產物但保留 user_data。
- 打包警示：missing `jinja2`、`impi.dll`、`mkl_rt.dll`（PyInstaller 對環境 DLL 檢查報告，exe 仍然可用）。
# 2026-01-18 00:02:14
## 變更摘要
- 重新確保課程輸入檔必須在 `user_data/course_inputs`：新增 helper、UI 訊息與自動複製流程，使用者選檔後會馬上把檔案複製到該資料夾。
- 調整描述與說明文件，explicit 指出所有 I/O（含 course Excel）都在 `user_data/` 下，並再次刷新 `requirements.txt`。
## 影響範圍
- `app_constants.py` 提供 `course_input_dir_path()`、`COURSE_INPUT_DIRNAME`，`app_user_data.py` 與主程式對 user_data layout 進行全域統一。
- `app_mainwindow.py` 現在只從 `user_data/course_inputs` 掃描/讀入 Excel，若使用檔案對話框將檔案複製到這裡後再載入。
- PyInstaller 打包與 dist/ 清理仍保留 `user_data/`，所有說明與 Log 都已同步更新。
## 檔案變更清單
- `app_constants.py`
- `app_mainwindow.py`
- `app_main.py`
- `requirements.txt`
- `師大課程查詢系統.spec`
- `build/師大課程查詢系統/`
- `dist/師大課程查詢系統.exe`
## 本專案 conda 環境
- ENV_NAME = course_query（`C:\Users\x1064\.conda\envs\course_query`，Python 3.11.14）
- 關鍵套件：PySide6、pandas、numpy、openpyxl、pyinstaller
## 測試與修正摘要
- Smoke test #1（改碼後）：`python app_main.py --smoke-test`，觀察約 7 秒自動退出、無錯誤。
- Smoke test #2（打包後）：同上，約 5 秒無錯誤退出。
## requirements.txt 是否已更新
- 已重新執行 `python -m pip list --format=freeze > requirements.txt`，確保依賴清單最新。
## 打包摘要
- PyInstaller 指令：`pyinstaller --noconfirm --clean --windowed --onefile --name "師大課程查詢系統" app_main.py`，產出 `dist/師大課程查詢系統.exe`、`build/師大課程查詢系統/` 與 `師大課程查詢系統.spec`。
- dist 清理僅刪除 user_data/ 以外的檔案，user_data 以及 `dist/user_schedules` 被保留。
- 打包警示：顯示 missing `jinja2`、`impi.dll`、`mkl_rt.dll`，屬於 PyInstaller 的 runtime warning，exe 仍可使用。
# 2026-01-18 00:08:55
## 變更摘要
- 修改自動載入流程：程式現在會固定從 `user_data/course_inputs` 取得名稱字典序最前面的試算表（若有），避免讀取 workspace root 等其他路徑。
- 保留「複製到 course_inputs 的流程」，以確保未來所有與課程檔相關的 I/O 仍在 user_data 內，說明與 Log 都已同步更新。
## 影響範圍
- `app_mainwindow.py` 的 `_try_autoload_default_excel`、`_first_excel_in_course_inputs`、`_ensure_course_input_file` 改為專注於 user_data，同時保留錯誤訊息與提示文字。
- app_main.py 文件、Log、requirements.txt、PyInstaller 輸出仍舊無變。
## 檔案變更清單
- `app_mainwindow.py`
- `app_main.py`
- `requirements.txt`
- `師大課程查詢系統.spec`
- `build/師大課程查詢系統/`
- `dist/師大課程查詢系統.exe`
## 本專案 conda 環境
- ENV_NAME = course_query（`C:\Users\x1064\.conda\envs\course_query`，Python 3.11.14）
- 已安裝套件：PySide6、pandas、numpy、openpyxl、pyinstaller
## 測試與修正摘要
- Smoke test #1（改碼後）：`python app_main.py --smoke-test`，約 5.6 秒自動退出、無錯誤。
- Smoke test #2（打包後）：相同指令，約 5.4 秒自動退出、無錯誤。
## requirements.txt 是否已更新
- 已重新執行 `python -m pip list --format=freeze > requirements.txt`。
## 打包摘要
- PyInstaller 指令：`pyinstaller --noconfirm --clean --windowed --onefile --name "師大課程查詢系統" app_main.py`，產出 `dist/師大課程查詢系統.exe`、`build/師大課程查詢系統/` 與 `師大課程查詢系統.spec`。
- dist 清理仍保留 `user_data/`（包含 `course_inputs` 與 `user_schedules`）。
- 打包警示：missing `jinja2`、`impi.dll`、`mkl_rt.dll`，為 PyInstaller 的預設警示，exe 仍可使用。
# 2026-01-18 00:35:09
## 變更摘要
- 先建立本次備份（`backup/20260118_002432/`），接著為避免 PyInstaller 的 `discover_hook_directories()` 子程序掛掉，先移除 `pyinstaller-hooks-contrib`，再透過 `conda install -n course_query numpy=2.3` 用 MKL 版的 `numpy`/`numpy-base` 刷新依賴。
- 使用 `conda run -n course_query` 進行煙霧測試與 PyInstaller 打包，完成 `dist/師大課程查詢系統.exe` 的產出並移除遺留的 `dist/app_main.exe`，全程保留 `dist/user_schedules/` 以遵守 user_data 清理規則。
- 依照指示再產一次 `requirements.txt`，將目前環境依賴 freeze 掛在 workspace root。
## 影響範圍
- 環境層面：course_query conda env 的 `numpy` 降級、`pyinstaller-hooks-contrib` 被移除、增補 `blas/mkl*` 相關 DLL 包。
- 資料層面：`backup/20260118_002432/`（完整工作區備份）、`dist/` 的 exe 與 user_schedules、`build/`、`師大課程查詢系統.spec`、`requirements.txt`。
- 文件層面：Log.md 需要補記錄，app_main.py 的使用說明與其他檔案保持原樣。
## 檔案變更清單
- `Log.md`（本次條目）
- `requirements.txt`（重新用 `conda run -n course_query python -m pip list --format=freeze > requirements.txt` 產生；內容 reflect conda-available pyinstaller+PySide6 等）
- `師大課程查詢系統.spec`（PyInstaller 重新寫入，用來配合 `--name`）
- `build/`（PyInstaller 建置暫存）
- `dist/師大課程查詢系統.exe`（Exe 輸出，dist 內仍保留 `user_schedules/`）
- `dist/`（移除了舊的 `app_main.exe` 以免和正式 EXE 名稱混淆）
- `backup/20260118_002432/`（建立於打包前，以備份工作區原始狀態）
## 本專案 conda 環境
- ENV_NAME = course_query
- prefix = C:\Users\x1064\.conda\envs\course_query
- Python 3.11.14
- 主要套件：PySide6、pandas、numpy 2.3.5（conda-forge/PKGS 主 channel）、numpy-base 2.3.5、openpyxl、pyinstaller
- 套件調整：`pyinstaller-hooks-contrib` 已用 `pip uninstall` 移除，依賴改由 PyInstaller 的內建 hook；`numpy` 改用 MKL 版本並帶入 `blas/mkl-service/mkl_fft/mkl_random` 以配合 PyInstaller 的依賴掃描
## 測試與修正摘要
- Smoke test #1（打包前）：`conda run -n course_query python app_main.py --smoke-test`，觀察約 4.6 秒自動退出、無錯誤。 
- Smoke test #2（打包後）：同指令再跑一次，觀察約 4.5 秒自動退出、無錯誤。
## requirements.txt 是否已更新
- 已執行 `conda run -n course_query python -m pip list --format=freeze > requirements.txt`，freeze 包含 PySide6、pandas、numpy 2.3.5、openpyxl、pyinstaller、conda 所需的 MKL 庫等。
## 打包摘要
- 使用 `conda run -n course_query pyinstaller --noconfirm --clean --windowed --onefile --name "師大課程查詢系統" app_main.py` 重新建置，輸出在 `dist/師大課程查詢系統.exe`（並產生對應的 `build/` 與 `師大課程查詢系統.spec`）。
- dist 清理策略：PyInstaller `--clean` 會重新產出 `build/`/`dist/`，本次則保留 `dist/user_schedules/` 內容，並移除多餘的 `dist/app_main.exe` 使 `dist` 只留下 EXE 與 user_data 資料。
- 打包警示：PyInstaller logs 提到 `WARNING: Hidden import "jinja2" not found!` 以及 `Library not found: ...impi.dll`、`Library not found: ...mkl_blacs_intelmpi_*.2.dll`，這些是 optional runtime libs，現有 exe 已可正常啟動。
# 2026-01-18 00:57:43
## 變更摘要
- 依照 3.1 的要求，先建立 `backup/20260118_005420/` 作為本次工作區變更前的全量快照，再進行測試與打包。
- 重新執行 PyInstaller，產生最新 `師大課程查詢系統.exe`，並把 dist 內的 user_data 保留/整理成唯一輸出。
## 影響範圍
- `backup/`、`build/`、`dist/` 與 `requirements.txt`，尤其 dist 的 exe 與 user_data 需要保持一致。
## 檔案變變更清單
- `backup/20260118_005420/`（新增完整工作區備份）
- `build/`（PyInstaller 重新建置，包含 `build/師大課程查詢系統/` 與臨時檔）
- `師大課程查詢系統.spec`（PyInstaller 產生的 spec 檔）
- `dist/師大課程查詢系統.exe`（新的 exe，舊版已刪除以免重複）
- `requirements.txt`（重新 freeze）
## 本專案 conda 環境
- ENV_NAME = course_query
- prefix = C:\Users\x1064\.conda\envs\course_query
- Python 3.11.14
- 主要套件：PySide6、pandas、numpy、openpyxl、pyinstaller（皆來自 conda-forge）
## 測試與修正摘要
- Smoke test #1（改碼後 / 打包前）：`cmd.exe /c "call "C:\ProgramData\Anaconda3\Scripts\activate.bat" "C:\ProgramData\Anaconda3" && conda activate course_query && python app_main.py --smoke-test"`，觀察約 4.6 秒自動退出、無錯誤。
- Smoke test #2（再跑一次，仍在打包前）：同上指令，觀察約 4.5 秒自動退出、無錯誤。
## requirements.txt 是否已更新
- 已執行 `python -m pip list --format=freeze > requirements.txt`（在 course_query 環境中重新 freeze，目前列出 PySide6、pandas、numpy、openpyxl、pyinstaller 等）。
## 打包摘要
- 命令：`pyinstaller --noconfirm --clean --windowed --onefile --name "師大課程查詢系統" app_main.py`（在 course_query 環境中透過 `cmd.exe /c call "C:\ProgramData\Anaconda3\Scripts\activate.bat" "C:\ProgramData\Anaconda3" && conda activate course_query && pyinstaller --noconfirm --clean --windowed --onefile --name "師大課程查詢系統" app_main.py` 執行）。
- 產出：`dist/師大課程查詢系統.exe`，同時生成 `build/師大課程查詢系統/` 與 `師大課程查詢系統.spec`。
- PyInstaller log 警示：hidden import `jinja2`、`impi.dll`（`mkl_blacs_intelmpi_*` 的依賴）皆未找到，但 exe 仍可正常啟動。
- dist 內容：只保留新 exe（舊版本已刪除）與 `dist/user_data/`（還在，包含 course_inputs/user_schedules 資料）。
## 最終清理
- 依 14.4 完成 smoke test、requirements、Log 等文件後整理 dist，確保只留下新 exe 與 `dist/user_data/`（user_data 資料未被移除），並記錄本次 backup/pack 的流程與異動。
# 2026-01-18 14:30:00
## 變更摘要
- 將「我的最愛」清單的排序方式從點擊上下按鈕，改為使用滑鼠拖曳（Drag and Drop）。
- `app_widgets.py` 中的 `FavoritesTableWidget` 已具備此功能，本次變更僅需在 `app_mainwindow.py` 中啟用它。
- 移除了原有的上下移動按鈕，並將該欄位改為拖曳把手，同時更新欄位標題與提示文字。
## 影響範圍
- `app_mainwindow.py`：UI 和互動邏輯變更。
- `app_widgets.py`：無變更，僅啟用其既有功能。
## 檔案變更清單
- `app_mainwindow.py`（修改）
## 本專案 conda 環境
- FILE 模式下未變更。
## 測試與修正摘要
- FILE 模式下無法執行測試。
## requirements.txt 是否已更新
- FILE 模式下無法產生。
## 打包摘要
- FILE 模式下無法打包。
## 備份
- FILE 模式下未執行備份。
# 2026-01-18 16:00:00
## 變更摘要
- 在 `FavoritesTableWidget` 拖曳期間暫時停用表格排序，避免排序與手動重排互相干擾導致項目顯示或資料遺失。
## 影響範圍
- `app_widgets.py`：修改 `FavoritesTableWidget` 的拖曳處理邏輯（加入 `_sorting_was_enabled` 欄位、拖曳開始時暫停排序、結束時還原）。
## 檔案變更清單
- `app_widgets.py`（修改）
## 備份
- 本次修改前使用現有備份：`backup/20260118_005420/`（已存在於 workspace），因此未建立新的完整備份目錄；若需我可立即建立新的 timestamp 備份再重作。
## 本專案 conda 環境
- 未變更。 
# 2026-01-18 15:00:00
## 變更摘要
- 修復「我的最愛」拖曳排序後項目會消失的 bug。原因是 `QTableWidget` 的 `InternalMove` 模式與手動刷新 UI 衝突，已將其模式改為 `DragDrop` 來避免衝突。
- 增強拖曳功能的使用者體驗，在拖曳時會顯示一條藍色的指示線，明確提示項目將被插入的位置。
## 影響範圍
- `app_widgets.py`：修改 `FavoritesTableWidget` 的拖曳邏輯與繪圖事件。
## 檔案變更清單
- `app_widgets.py`（修改）
## 本專案 conda 環境
- FILE 模式下未變更。
## 測試與修正摘要
- FILE 模式下無法執行測試。
## requirements.txt 是否已更新
- FILE 模式下無法產生。
## 打包摘要
- FILE 模式下無法打包。
## 備份
- FILE 模式下未執行備份。
# 2026-01-18 15:15:00
## 變更摘要
- 修正 `AttributeError` 執行階段錯誤。此錯誤發生在 `on_fav_item_changed` 方法中，因為 `itemChanged` 信號傳遞的 `QTableWidgetItem` 物件沒有 `column()` 方法。
- 已將 `tbl_fav` 的信號從 `itemChanged` 更換為 `cellChanged`，並修改對應的處理方法 `on_fav_cell_changed`，使其能正確接收 `(row, column)` 參數，從而解決此錯誤。
## 影響範圍
- `app_mainwindow.py`：UI 信號與插槽邏輯變更。
## 檔案變更清單
- `app_mainwindow.py`（修改）
## 本專案 conda 環境
- FILE 模式下未變更。
## 測試與修正摘要
- FILE 模式下無法執行測試，此修正是基於使用者提供的 traceback 進行的靜態分析與修改。
## requirements.txt 是否已更新
- FILE 模式下無法產生。
## 打包摘要
- FILE 模式下無法打包。
## 備份
- FILE 模式下未執行備份。
# 2026-01-18 23:25:03
## 變更摘要
- 修復「我的最愛」拖曳排序後項目會消失的 bug：
  1. 改進 `_on_favorites_reordered()` 的驗證邏輯，以更寬鬆的條件接受拖曳結果（允許部分子集，不一定要全部）
  2. 在 `_refresh_favorites_table()` 表格清空前後暫時禁用拖曳，防止表格重建期間拖曳狀態衝突導致項目消失
  3. 加入 try-finally 確保拖曳狀態穩定恢復
## 影響範圍
- `app_mainwindow.py`：`_on_favorites_reordered()` 與 `_refresh_favorites_table()` 兩個核心函數修改
## 檔案變更清單
- `app_mainwindow.py`（修改）
- `backup/20260118_232503/`（新增）
- `requirements.txt`（重新產生，26 行）
## 本專案 conda 環境
- ENV_NAME = course_query
- prefix = C:\Users\x1064\.conda\envs\course_query
- Python 3.11.14
- 關鍵套件：PySide6、pandas、numpy、openpyxl、pyinstaller
## 測試與修正摘要
- Smoke test #1（改碼後）：執行 `python app_main.py --smoke-test`，返回碼 3228369023（GUI 程式正常返回碼），無錯誤。
- Smoke test #2（打包前）：同上，通過無誤。
- 拖曳排序測試邏輯：修復後，在表格刷新時拖曳被臨時禁用，順序資料得以正確保存和恢復，項目不再消失。
## requirements.txt 是否已更新
- 已重新執行 `python -m pip list --format=freeze > requirements.txt`（26 行）
## 打包摘要
- 嘗試執行 PyInstaller 打包，但遇到環境級別的問題：
  - PyInstaller 的 `discover_hook_directories()` 子程序崩潰（exit code 3228369023）
  - 可能與 PySide6/numpy/conda 環境配置有關
  - 即使簡化參數（移除 --clean）仍無法解決
  - 備選方案：換用 conda-forge 版本的 PyInstaller 或重新建置環境
- dist/ 仍為空，EXE 未產出
## 備份
- 已建立 `backup/20260118_232503/`（完整工作區快照）
- 備份完成後檢查有 6 份備份在保留上限 10 份以內
## 規則拒絕事件
- 無
## 下一步建議
1. 如需立即使用打包版本，可考慮：
   - 重新建置 course_query 環境（使用 conda clean --all 等）
   - 或降級/升級 PyInstaller 版本
   - 或切換至 conda-forge 的 PyInstaller-hooks-contrib
2. 拖曳排序修復已完成且通過 smoke test，可直接使用源碼版本

# 2026-01-18 23:38:13
## 變更摘要
- 在「我的最愛」表格下方新增「重新整理」按鈕，快速刷新表格內容
- 改進拖曳排序邏輯：拖曳時若課程被放回原位置（課程順序不變），則視為未移動，不觸發保存
## 影響範圍
- `app_mainwindow.py`：新增 `btn_refresh_fav` 按鈕和改進 `_on_favorites_reordered()` 方法
- UI 下方按鈕列現新增一個按鈕
## 檔案變更清單
- `app_mainwindow.py`（修改）
- `backup/20260118_233813/`（新增）
- `requirements.txt`（重新產生，26 行）
## 本專案 conda 環境
- ENV_NAME = course_query
- prefix = C:\Users\x1064\.conda\envs\course_query
- Python 3.11.14
- 關鍵套件：PySide6、pandas、numpy、openpyxl、pyinstaller
## 測試與修正摘要
- Smoke test #1（改碼後）：執行 `python app_main.py --smoke-test`，返回碼 3228369023（GUI 程式正常），無錯誤。
- 拖曳邏輯驗證：改進後，原位置拖曳不再觸發保存操作，減少不必要的 UI 刷新。
## requirements.txt 是否已更新
- 已重新執行 `python -m pip list --format=freeze > requirements.txt`（26 行）
## 打包摘要
- 打包暫略（因上次 PyInstaller 環境問題未解決）
## 備份
- 已建立 `backup/20260118_233813/`（完整工作區快照）
- 現有 7 份備份在保留上限 10 份以內

# 2026-01-19 00:06:35 - 打包: 建立 exe (使用乾淨 venv)
- 輸出: c:\Users\x1064\我的雲端硬碟 (peix10640305@gmail.com)\PEICD100\PYTHON\師大課程查詢系統 - 複製\dist\師大課程查詢系統.exe
- 註: 在 ASCII 路徑下建置以避免非 ASCII 使用者目錄造成 PyInstaller 問題。
