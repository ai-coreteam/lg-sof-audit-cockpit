# Từ Điển Dữ Liệu & Quy Tắc Thẩm Định (Data Dictionary & Audit Rules)

> Tài liệu này định nghĩa chi tiết cấu trúc các bảng trong Google Sheet, ý nghĩa từng trường dữ liệu trong JSON/JS và hệ thống quy tắc thẩm định tự động (**Sanity Check & Risk Governance Matrix**) của **LG SOF Audit & Risk Governance Cockpit**.

---

## 1. Cấu trúc Nguồn Dữ liệu Google Sheet (`Check theo CAT, theo Brand`)

### 1.1. Bảng Mapping Cột — Chu kỳ `W38 – W42` (Google Sheet Live `1lA6mxuh3yn6TMGWH8TIWOl6PWyKP5PeZ586sOnOGG40`, `gid=1357809752`)

> **Lưu ý kỹ thuật quan trọng (`[VERIFIED]`):** So với chu kỳ `W37–W41`, ở chu kỳ `W38–W42` vị trí cột **D** (`Region`) và cột **E** (`PC Active`) đã đảo chiều. Hệ thống đồng bộ (`scripts/sync_sheets.py` và `fetchGoogleSheetLive()` trong `app/index.html`) sử dụng cơ chế **Header-Aware Column Detection** để tự động nhận diện đúng vị trí cột dựa trên dòng tiêu đề.

| Cột Excel | Chỉ số (0-based) | Tên Cột Gốc (`W38–W42`) | Tên Cột Gốc (`W37–W41`) | Kiểu Dữ Liệu | Mô Tả Chi Tiết |
|---|---:|---|---|---|---|
| **A** | `0` | `Code Shop` | `shop_code` | `String` | Mã định danh duy nhất của cửa hàng trên hệ thống LG (VD: `EASV4271`, `EASV10177`). |
| **B** | `1` | `Tên Shop` | `New Format Name (update)` | `String` | Tên cửa hàng theo định dạng chuẩn (VD: `CP-NINH THUAN-PHAN RANG`, `CN Cty TNHH CaoPhong tai Quang Tri`). |
| **C** | `2` | `PC SUP` | `PC SUP` | `String` | Họ và tên Quản lý khu vực (PC Supervisor) phụ trách điểm bán. |
| **D** | `3` | `Region` | `PC active` *(ở W41)* | `String` | Khu vực địa lý (`North`, `Middle`, `South`). Hệ thống tự động bắt theo tên cột header. |
| **E** | `4` | `PC Active` | `Region` *(ở W41)* | `Integer` | Số lượng nhân viên PG/PC đang hoạt động tại cửa hàng (`0` = White Spot không có PC; `>= 1` = Có PC cắm chốt). |
| **F** | `5` | `CAT` | `Category` | `String` | Mã ngành hàng (`TV`, `WM`, `REF`, `RAC`, `AP`, `MWO`, `DW`, `VC`, `DEHUM`, `AV`). |
| **G** | `6` | `Brand` | `Brand` | `String` | Thương hiệu (`LG`, `SS`, `Pana`, `Sony`, `TCL`, `Toshiba`, `Aqua`, `Sharp`, `Casper`, `Elux`, `Haier`, `Other`...). |
| **H – L** | `7 – 11` | `W38`, `W39`, `W40`, `W41`, `W42` | `W37`..`W41` *(hoặc `W36`..`W40`)* | `Integer` | Số lượng máy trưng bày thực tế (sets) ghi nhận tại cửa hàng qua 5 tuần liên tiếp. |
| **M** | `12` | `Chênh lệch hơn 2 so với tuần cũ` | `Chênh lệch hơn 2 so với tuần cũ` | `Flag (x)` | Đánh dấu `x` nếu `\|W_cur - W_prev\| > 2` sets. |
| **N** | `13` | `Chênh lệch hơn 8 so với 4 tuần trước` | `Chênh lệch hơn 8 so với 4 tuần trước` | `Flag (x)` | Đánh dấu `x` nếu `\|W_cur - W_cur-4\| > 8` sets. |
| **O** | `14` | `Data về 0` | `Data về 0` | `Flag (x)` | Đánh dấu `x` nếu tuần trước có trưng bày (`> 0`) nhưng tuần hiện tại rơi về `0`. |
| **P** | `15` | `Feedback` | `Feedback` | `String` | Nội dung giải trình chuẩn hóa (dropdown) của PC Supervisor điền trên Google Sheet. |
| **Q** | `16` | `Count số lỗi` | `Count số lỗi` | `Integer` | Tổng số cờ cảnh báo xuất hiện trên dòng đó (`0`, `1`, `2`, hoặc `3`). |
| **R** | `17` | `Extra note` | *(Không tiêu đề - Ghi chú bổ sung)* | `String` | Ghi chú thực địa chi tiết do PC SUP bổ sung (hỗ trợ cả ô nhiều dòng liệt kê mã model lên/xuống kệ, số thực đếm...). |

---

### 1.2. Bảng `Mapping PC SUP` (Sheet 2 trong `data/google_sheet_latest.xlsx`)
- **Tổng số dòng:** `1.690` cửa hàng chuẩn hóa trên toàn quốc.
- **Mục đích:** Cung cấp thông tin Master Data (`province`, `district`, `dealer`, `channel`, `active_pc`) để làm giàu (enrich) cho các dòng dữ liệu tải trực tiếp từ CSV Google Sheet (được nhúng sẵn vào `datasetW42.store_master`).
- **Quy tắc phân loại Đại lý (`classify_dealer` / `inferDealerClient`):**
  - Bắt đầu bằng `DMX` hoặc `ĐMX` -> **`DMX`** (`channel: "MC"`)
  - Bắt đầu bằng `CP`, `CAO PHONG`, hoặc có chứa `CAOPHONG` viết liền (VD: `CN Cty TNHH CaoPhong tai Quang Tri`) -> **`CP`** (`channel: "MC"`)
  - Bắt đầu bằng `MM` -> **`MM`** (`channel: "MC"`)
  - Bắt đầu bằng `VHC` -> **`VHC`** (`channel: "MC"`)
  - Các trường hợp còn lại -> **`Tradi`** (`channel: "Traditional"`)

---

## 2. Cấu trúc Bản ghi Đã Thẩm định (`w42_audit_cockpit.json`, `w41_audit_cockpit.json`, `w40_audit_cockpit.json`)

Mỗi bản ghi (`record`) trong mảng `records` của file JSON/JS có cấu trúc chuẩn như sau:

```json
{
  "id": "EASV4271_WM_Aqua",
  "store_code": "EASV4271",
  "store_name": "CP-NINH THUAN-PHAN RANG",
  "dealer": "CP",
  "channel": "MC",
  "region": "Middle",
  "province": "Ninh Thuan",
  "district": "Thành phố Phan Rang-Tháp Chàm",
  "sup": "Dương Nguyên Trà My",
  "active_pc": 2,
  "category": "WM",
  "brand": "Aqua",
  "w38": 23,
  "w39": 23,
  "w40": 23,
  "w41": 23,
  "w42": 19,
  "delta_wow": -4,
  "flags": {
    "diff_8_4w": false,
    "diff_2_prev": true,
    "zero_drop": false,
    "lg_drop_50": false
  },
  "feedback_raw": "Shop báo tăng giảm đúng thực tế so với tuần trước đó",
  "extra_note": "Chuyển model cũ về kho An hạ\nAW10-B4959U1K(B)\nAW10-BP4959U1K(B)\nAW12-B4377U1L(GN)",
  "w41_hint": "",
  "eval": {
    "status": "ĐÃ_FEEDBACK",
    "validity": "PLAUSIBLE",
    "validity_label": "Đã làm rõ (Extra Note)",
    "validity_desc": "SUP bổ sung: \"Chuyển model cũ về kho An hạ · AW10-B4959U1K(B) · AW10-BP4959U1K(B) · AW12-B4377U1L(GN)\". Đã làm rõ nguyên nhân biến động thực tế.",
    "risk_level": "P3_NORMAL",
    "risk_label": "Biến động đã làm rõ",
    "risk_desc": "Cửa hàng đã giải trình cụ thể biến động thực tế.",
    "action_code": "ACCEPT",
    "action_title": "Phê duyệt giải trình (Có Extra Note)",
    "action_detail": "Chấp thuận do SUP đã bổ sung nguyên nhân thực địa: 'Chuyển model cũ về kho An hạ · AW10-B4959U1K(B) · AW10-BP4959U1K(B) · AW12-B4377U1L(GN)'."
  }
}
```

---

## 3. Ma trận Quy tắc Thẩm định & Quản trị Rủi ro (Sanity Check & Risk Governance Matrix)

Hệ thống áp dụng bộ quy tắc đánh giá tự động theo thứ tự ưu tiên nghiêm ngặt (Strict Priority Order) và **Phân tách Độc lập (MECE Separation)**:

| Thứ tự | Mã Quy Tắc | Điều Kiện Kích Hoạt (Trigger Condition) | Kết Quả Thẩm Định (`validity`) | Cấp Độ Rủi Ro (`risk_level`) | Mã Hành Động (`action_code`) | Khuyến Nghị Hành Động Cho GTM |
|---:|---|---|---|---|---|---|
| **1** | `RULE-PENDING` | `feedback_raw` trống **VÀ** `extra_note` trống | `PENDING` *(Chưa có phản hồi)* | `HIGH` *(Rủi ro tồn đọng)* | `PUSH_SUP` | **Đôn đốc phản hồi gấp:** Gửi tin nhắn cảnh báo yêu cầu SUP xác minh trước 17:00 Thứ 4. |
| **2** | `RULE-SAN-03` | `feedback_raw` chứa *"báo sai"*, *"nhập sai"*, *"điều chỉnh lại"* (kể cả khi có kèm `extra_note` giải thích thêm) | `PC_ERROR` *(Thừa nhận PC báo sai)* | `P2_OPERATIONAL` *(Lỗi vận hành PC)* | `COACH_PC` | **Kiểm điểm & Đào tạo PC:** Yêu cầu SUP chấn chỉnh quy trình kiểm đếm của PC tại điểm bán (hiển thị kèm `extra_note` nếu có). |
| **3** | `RULE-EXTRA-01` | Có `extra_note` chứa từ khóa đính chính số liệu (*"số đúng là"*, *"không phải"*, *"sets"*, *"sai số"*, *"lệch số"*, *"week trước chỉ"*) | `DATA_MISMATCH` *(Sai lệch số thực tế)* | `P2_OPERATIONAL` *(Dữ liệu Sheet bị lệch số)* | `CORRECT_DATA` | **Bác bỏ & Hiệu chỉnh số liệu:** Yêu cầu sửa lại số đúng trên bảng chính thức theo ghi chú thực tế và kiểm điểm PC. |
| **4** | `RULE-EXTRA-02` | Có `extra_note` chứa từ khóa thu hẹp kệ đối thủ (*"cắt"*, *"bỏ mẫu"*, *"đảo"*, không phải đảo mẫu *"lên ... cắt ..."*) và `brand != "LG"` | `PLAUSIBLE` *(Đã làm rõ - Extra Note)* | `P3_NORMAL` *(Đối thủ bị cắt giảm)* | `EXPAND_LG` | **Tận dụng chiếm đảo kệ:** Đề xuất làm việc với cửa hàng để đưa thêm sản phẩm LG vào vị trí trống của đối thủ. |
| **5** | `RULE-EXTRA-03` | Có bất kỳ nội dung `extra_note` giải trình thực địa nào khác (liệt kê mã model mới lên/xuống kệ, chuyển kho EOL, dọn kho...) | `PLAUSIBLE` *(Đã làm rõ - Extra Note)* | `P3_NORMAL` *(Biến động đã làm rõ)* | `ACCEPT` | **Phê duyệt giải trình (Có Extra Note):** Chấp thuận giải trình thực địa và loại khỏi nhóm nghi vấn đối phó. |
| **6** | `RULE-SAN-01` | Không có `extra_note`, `zero_drop == true` VÀ `feedback_raw` ghi *"tăng giảm đúng thực tế"* | `SUSPICIOUS` *(Nghi vấn đối phó)* | `P0_CRITICAL` (nếu `LG`) / `P1_SUSPICIOUS` (nếu đối thủ) | `REJECT_AND_AUDIT` | **Bác bỏ & Đòi ảnh thực tế:** Từ chối duyệt. Yêu cầu SUP gửi ảnh chụp kệ thực tế trong 24h hoặc bổ sung `Extra note`. |
| **7** | `RULE-SAN-02` | Không có `extra_note`, `diff_8_4w == true` VÀ `feedback_raw` ghi *"tăng giảm đúng thực tế"* | `SUSPICIOUS` *(Nghi vấn đối phó)* | `P1_SUSPICIOUS` *(Nghi vấn đối phó)* | `REJECT_AND_AUDIT` | **Yêu cầu ảnh & Biên bản:** Yêu cầu SUP giải trình chi tiết lý do biến động đột biến hoặc điền `Extra note`. |
| **8** | `RULE-COMM-01` | `feedback_raw` chứa *"cắt shop"*, *"bỏ quầy"*, *"dồn quầy"*, *"hạ bục"*, *"thu hồi"* | `PLAUSIBLE` *(Hợp lý - Có căn cứ)* | `P0_CRITICAL` (nếu `LG`) / `P1_COMMERCIAL` (nếu đối thủ) | `ESCALATE_KAM` | **Can thiệp KAM khẩn cấp:** Báo cáo Head of GTM & làm việc với KAM để bảo vệ hợp đồng quầy kệ. |
| **9** | `RULE-LG-DROP` | `brand == "LG"` VÀ `delta_wow <= -2` | `PLAUSIBLE` *(Hợp lý đạt chuẩn)* | `P0_CRITICAL` *(Rủi ro giảm trưng bày LG)* | `ESCALATE_KAM` | **Theo dõi SOF & Kiểm tra shop:** Kiểm tra lý do giảm model LG và đôn đốc đưa thêm hàng trưng bày. |
| **10** | `RULE-DEFAULT` | Các trường hợp giải trình hợp lệ còn lại | `PLAUSIBLE` *(Hợp lý đạt chuẩn)* | `P3_NORMAL` *(Biến động bình thường)* | `ACCEPT` | **Phê duyệt giải trình:** Chấp thuận dữ liệu đưa vào báo cáo SOF chính thức. |
