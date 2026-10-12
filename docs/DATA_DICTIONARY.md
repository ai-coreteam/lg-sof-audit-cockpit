# SOF Monitoring Data Dictionary

This document provides a verified, comprehensive mapping of data schemas across both the **Live Google Sheet Database (W37–W41)** and the **W40 Baseline Dataset (`SOF check W40.xlsx`)**.

---

## 1. Live Google Sheet Database (`W37–W41`)

- **Spreadsheet Title:** `SOF check W37-W41 (Middle)`
- **Google Sheet URL:** [Google Sheets Live Link](https://docs.google.com/spreadsheets/d/1mpArbb5ShJqtWfgC8yB7pVv70tcTXK7XYKnxGWSGaws/edit?usp=sharing)
- **Export Endpoint:** `https://docs.google.com/spreadsheets/d/1mpArbb5ShJqtWfgC8yB7pVv70tcTXK7XYKnxGWSGaws/export?format=xlsx`
- **Automated Sync Script:** `python3 scripts/sync_sheets.py`
- **Output Artifacts:** `data/w41_audit_cockpit.json` & `app/assets/w41_audit_cockpit.js`

### 1.1. Sheet: `Check theo CAT, theo Brand` (Primary Audit Sheet)
- **Active Data Rows:** 3,143 display lines (Middle Region)
- **Grain:** 1 row per `Code Shop` + `CAT` + `Brand`
- **Rolling Cycle:** W37, W38, W39, W40, W41 (Current audit week: **W41**)

| Col # | Excel Col | Header Name | Data Type | Sample Value | Business Description |
|---|---|---|---|---|---|
| 0 | A | `Code Shop` | String | `EASV1004` | Store unique identifier (references Store Master) |
| 1 | B | `Tên Shop` | String | `CONG TY TNHH TM DV XUAN HOA` | Retail shop commercial name |
| 2 | C | `PC Sup` | String | `Trần Thanh Tuấn` | Assigned Field Supervisor (6 SUPs in Middle region) |
| 3 | **D** | **`PC active`** | **Integer** | **`1`**, **`2`**, **`0`** | **[NEW COLUMN] Số lượng nhân viên PC đang trực tiếp làm việc tại shop** |
| 4 | E | `Region` | String | `Middle` | Geographic territory (North / Middle / South) |
| 5 | F | `CAT` | String | `REF`, `TV`, `WM`, `DW` | Product Category (10 active product groups) |
| 6 | G | `Brand` | String | `LG`, `SS`, `Pana`, `Other` | Target Brand being audited |
| 7 | H | `W37` | Integer | `11` | Display sets 4 weeks prior |
| 8 | I | `W38` | Integer | `11` | Display sets 3 weeks prior |
| 9 | J | `W39` | Integer | `12` | Display sets 2 weeks prior |
| 10 | K | `W40` | Integer | `12` | Previous week display count ($W_{prev}$) |
| 11 | L | `W41` | Integer | `15` | Current week display count ($W_{cur}$) |
| 12 | M | `Chênh lệch hơn 2 so với tuần cũ` | Flag | `x` / Null | Triggered when $\|W41 - W40\| \ge 2$ (7 rows flagged in W41) |
| 13 | N | `Chênh lệch hơn 8 so với 4 tuần trước` | Flag | `x` / Null | Triggered when $\|W41 - \min(W37..W40)\| \ge 8$ (4 rows flagged in W41) |
| 14 | O | `Data về 0` | Flag | `x` / Null | Triggered when $W41 = 0$ and $W40 > 0$ (0 rows flagged in W41) |
| 15 | P | `Feedback` | String | (Text) | Free-text explanation filled by PC Supervisor on Google Sheet |
| 16 | Q | `Count số lỗi` | Integer | `1`, `2` | Formula `=countifs(M{row}:O{row},"x")` |
| 17 | **R** | **`Extra note`** | **String** | **`"dọn kho & mang..."`** | **[NEW COLUMN] Ghi chú thực tế bổ sung từ PC Sup / Regional Manager để làm rõ nguyên nhân biến động sâu hoặc đính chính số lượng thực tế.** |

> [!NOTE]
> **Key Schema Evolutions (Column D & Column R Insertions):**
> 1. **Column D (`PC active`):** Bổ sung số lượng nhân viên promoter túc trực tại sàn.
> 2. **Column R (`Extra note`):** Bổ sung trường ghi chú thực địa giúp làm rõ ngữ cảnh biến động, phân biệt giữa đối phó qua loa và giải trình nghiệp vụ thực chất (dọn kho, cắt đảo kệ, chuyển model EOL chạy event, hoặc phát hiện số liệu khai khống 18 vs 27 sets). Khi cột này có nội dung, ca kiểm soát lập tức được chuyển hoàn toàn ra khỏi mục Nghi vấn đối phó theo nguyên tắc MECE để đảm bảo thông tin tinh gọn, không trùng lặp.

---

### 1.2. Sheet: `Mapping PC SUP` (Store Master in Live Google Sheet)
- **Total Entities:** 1,690 Stores (Nationwide: North 948, Middle 391, South 351)
- **Supervisor Coverage:** 28 Field Supervisors

| Col # | Field Name | Type | Notes |
|---|---|---|---|
| 0 | `Code store` | String (PK) | Unique store identifier |
| 1 | `Store` | String | Full commercial outlet name |
| 2 | `Khu vực` | String | `North`, `Middle`, `South` |
| 3 | `Tỉnh/TP` | String | Province / Municipality |
| 4 | `Quận/Huyện` | String | District |
| 5 | `Sup` | String | Assigned PC Supervisor |
| 6..10 | `HA`, `HE`, `AC`, `HAC`, `CE` | Number | Category-specific promoter headcounts |
| 11 | `Số lượng PC đang hoạt động` | Number | Total active promoters stationed at store (`active_pc`) |

---

## 2. W40 Baseline Dataset (`SOF check W40.xlsx`)

- **File Size:** 11.66 MB
- **Cycle:** W36–W40 (Nationwide baseline with 632 flagged priority anomalies)
- **Output Artifacts:** `data/w40_audit_cockpit.json` & `app/assets/w40_audit_cockpit.js`

### 2.1. Sheet: `Check theo CAT, theo Brand` (W40)
- **Volume:** 28,521 active data rows across North, Middle, South.
- **Top 3 Priority Flags Evaluated:**
  - `Data về 0` (Col N): 97 rows
  - `Chênh lệch > 8 so với 4W cũ` (Col L): 121 rows
  - `Chênh lệch > 2 so với tuần cũ` (Col M): 536 rows
  - Total deduplicated flagged cases: **632 priority cases**.

---

## 3. Standard Reason Dictionary (`Lý do`)

Standardized explanation codes for supervisors on Google Sheet:
1. `Shop báo tăng giảm đúng thực tế so với tuần trước đó`
2. `Tuần cũ PC báo sai, tuần này điều chỉnh lại`
3. `Shop tăng giảm trưng bày do relayout - bán bớt mẫu cũ`
4. `Tăng do shop trưng thêm ở khu vực quầy kệ khác`
5. `Giảm do cắt shop bỏ quầy trưng bày`
6. `Shop tăng trưng bày do được đâu tư thêm bục kệ`
7. `PC nhập sai cần điều chỉnh lại`
8. `Khác`

---

## 4. Client-side State Persistence Schema (Lưu Trữ Cục Bộ Trình Duyệt)

Hệ thống duy trì trạng thái thẩm định của GTM Strategist trực tiếp trên trình duyệt máy khách (Client-side LocalStorage) để không làm ảnh hưởng hay ghi đè vào dữ liệu gốc của Google Sheet:

| Khóa Lưu Trữ (Key) | Kiểu Dữ Liệu | Chu Kỳ Áp Dụng | Mô Tả Ý Nghĩa |
|---|---|---|---|
| `lg_gtm_decisions_W41` | JSON String | Chu kỳ W41 Live | Lưu bản đồ quyết định của GTM: `{ [recordId: string]: "APPROVED" \| "REJECTED" }`. |
| `lg_gtm_decisions_W40` | JSON String | Chu kỳ W40 Baseline | Lưu bản đồ quyết định của GTM cho 632 ca lịch sử W40. |
| `currentMobileViewMode` | In-memory State | Toàn cục di động | Lưu trạng thái hiển thị trên di động (`"CARD"`: Dạng Thẻ dọc, `"TABLE"`: Bảng cuộn ngang). |

> [!TIP]
> Khi người dùng bấm **"Duyệt"** hoặc **"Bác bỏ / Đòi ảnh"** (trên cả giao diện Desktop hay Thẻ Mobile), hệ thống tự động cập nhật vào `localStorage`, đồng bộ lại bộ lọc và phát tín hiệu Toast xác nhận. Trạng thái này được bảo lưu nguyên vẹn kể cả khi trang tự động đồng bộ lại số liệu mới từ Google Sheet sau mỗi 30 giây.
