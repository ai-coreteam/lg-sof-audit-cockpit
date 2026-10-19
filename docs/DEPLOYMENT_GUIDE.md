# Hướng Dẫn Vận Hành, Đồng Bộ & Triển Khai (Operations & Deployment Guide)

> Tài liệu này hướng dẫn cách sử dụng **LG SOF Audit & Risk Governance Cockpit**, cơ chế đồng bộ thời gian thực với Google Sheet (`W38–W42`), cách chạy kiểm thử tự động và quy trình xuất bản lên GitHub Pages.

---

## 1. Cách Mở & Sử Dụng Cockpit Hàng Ngày

### Cách 1: Truy cập Bản Trực Tuyến (GitHub Pages — Khuyến nghị cho GTM & Mobile)
- Mở trực tiếp đường dẫn: **`https://ai-coreteam.github.io/lg-sof-audit-cockpit/`** trên máy tính hoặc điện thoại.

### Cách 2: Mở Trực Tiếp File Nội Bộ (Local File)
- Mở trực tiếp file:
  ```text
  /Users/macbook/Documents/antigravity/AI study/LG other/SOF monitoring/app/index.html
  ```
- Hoặc chạy HTTP Server nội bộ:
  ```bash
  python3 -m http.server 8765
  ```
  Sau đó mở `http://localhost:8765/app/index.html`.

---

## 2. Cơ Chế Đồng Bộ Dữ Liệu 2 Lớp (Dual-Layer Sync Architecture)

### Lớp 1: Đồng bộ Tự động Thời gian thực trên Trình duyệt (Browser Real-Time Live Sync)
Khi bạn mở Cockpit ở chế độ **`W38–W42 (Google Sheet Live)`**, ứng dụng sẽ tự động kết nối tới endpoint CSV Export của Google Sheet tuần hiện tại:
```text
https://docs.google.com/spreadsheets/d/1lA6mxuh3yn6TMGWH8TIWOl6PWyKP5PeZ586sOnOGG40/export?format=csv&gid=1357809752
```
- **Khi vừa mở trang:** Tự động tải dữ liệu mới nhất từ Google Sheet, tự động nhận diện thứ tự cột (`Region` / `PC Active`), đọc đầy cả các ô `Extra note` nhiều dòng (RFC-4180 CSV parser) và gắn nhãn gợi ý lịch sử W41 (`w41_hint`).
- **Mỗi 30 giây:** Tự động quét ngầm trong nền và cập nhật giờ đồng bộ tại huy hiệu **`Live: HH:MM:SS`**.
- **Khi chuyển tab quay lại (`window.focus`):** Ngay khi bạn vừa sửa trên Google Sheet và bấm quay lại tab Cockpit, hệ thống lập tức làm mới bảng dữ liệu.
- **Ép đồng bộ thủ công:** Bấm trực tiếp vào nút **`Live Sync`** trên thanh Header bất kỳ lúc nào.

### Lớp 2: Đồng bộ & Lưu trữ Offline bằng Python (`scripts/sync_sheets.py`)
Khi muốn lưu bản chụp (snapshot) từ Google Sheet vào các file tĩnh của dự án (`data/w42_audit_cockpit.json`, `app/assets/w42_audit_cockpit.js`, `assets/w42_audit_cockpit.js`) để đẩy lên GitHub Pages hoặc gửi file offline:

```bash
python3 scripts/sync_sheets.py
```

---

## 3. Chuyển Đổi Giữa 3 Chu Kỳ (`W38–W42 Live`, `W37–W41 Đã Chốt`, `W36–W40 Baseline`)

Trên thanh điều hướng trên cùng (Header), bạn có thể chuyển đổi tức thời giữa 3 chu kỳ:
1. **`W38–W42 (Google Sheet Live)`** *(Mặc định)*: Hiển thị **16 ca** cảnh báo mới nhất của khu vực Miền Trung tuần hiện tại, tự động đồng bộ mỗi 30 giây và hiển thị gợi ý lịch sử W41 (`w41_hint`) cho các ca lặp lại.
2. **`W37–W41 (Middle Đã Chốt)`**: Hiển thị bản lưu trữ **11 / 11 ca (100%)** đã giải trình hoàn tất của khu vực Miền Trung tuần trước.
3. **`W36–W40 (Baseline Toàn Quốc)`**: Hiển thị toàn bộ **632 ca** biến động trên **1.690 cửa hàng** toàn quốc (Bắc: 321 ca, Trung: 123 ca, Nam: 188 ca).

> **Lưu ý về Quyết định Duyệt / Bác bỏ (`localStorage`):** Các quyết định bấm **Duyệt** hoặc **Bác bỏ / Đòi ảnh** của GTM được lưu tách biệt theo từng chu kỳ (`lg_gtm_decisions_W42`, `lg_gtm_decisions_W41`, `lg_gtm_decisions_W40`) nên không bao giờ bị ghi đè lẫn nhau.

---

## 4. Quy Trình Kiểm Thử & Triển Khai Lên GitHub Pages (`origin/main`)

Trước mỗi lần đẩy code lên GitHub Pages, chạy bộ kiểm thử tự động và công cụ kiểm tra quản trị dự án:

```bash
# 1. Đồng bộ app/index.html ra ./index.html ở thư mục gốc
cp app/index.html index.html

# 2. Chạy bộ 11 bài kiểm thử tự động (Syntax, Parity, Multi-line CSV, Dealer CP, 3 Cycles)
node tests/verify_cockpit.js

# 3. Kiểm tra chuẩn Project Management & Quét bí mật
python3 /Users/macbook/.gemini/config/skills/project-management/scripts/pm_check.py . --release v2.1.0
python3 /Users/macbook/.gemini/config/skills/project-management/scripts/secret_scan.py --staged
```

Sau khi tất cả kiểm thử đều đạt (`11/11 PASS`, `0 error(s)`), commit và đẩy lên `origin/main`:
```bash
git add .
git commit -m "Release v2.1.0: Integrate W38-W42 Live Google Sheet, 3-cycle switcher & W41 hints"
git push origin main
```
