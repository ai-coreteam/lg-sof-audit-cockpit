# Bàn giao phiên — SOF monitoring
Cập nhật: 2026-10-19 17:02 +07:00

## Đã xong trong phiên
- Đọc hiểu toàn bộ cấu trúc dự án **LG SOF Audit & Risk Governance Cockpit** và áp dụng chuẩn quản trị dự án (`AGENTS.md`, `BRIEF.md`, `CHANGELOG.md`, `RUNBOOK.md`, `tests/verify_cockpit.js`).
- Tích hợp link Google Sheet mới của khu vực Miền Trung tuần `W38–W42` (`1lA6mxuh3yn6TMGWH8TIWOl6PWyKP5PeZ586sOnOGG40`, `gid=1357809752`) theo đúng **Phương án 1A, 2A, 3A** đã được chủ dự án phê duyệt:
  - **Phương án 1A:** Nâng cấp thanh chuyển đổi lên **3 chu kỳ**: `W38–W42 (Google Sheet Live)` (mặc định), `W37–W41 (Middle Đã Chốt)` (lưu trữ 11/11 ca), `W36–W40 (Baseline Toàn Quốc)` (632 ca).
  - **Phương án 2A:** Đồng bộ trực tiếp 16 ca cảnh báo của `W38–W42` (hiện tại **9/16 ca đã phản hồi — 56.2%**, **7/16 ca chưa phản hồi — 43.8%**), tự động gắn nhãn gợi ý lịch sử W41 (`w41_hint`) cho các shop/ca lặp lại từ W41 (`EASV6502`), và sửa lỗi phân loại đại lý `"CAOPHONG"` viết liền thành `"CP"` (`EASV10177` ở W42 và `EASV10176` ở W41).
  - **Phương án 3A:** Đồng bộ `app/index.html` sang `./index.html`, vượt qua 11/11 bài kiểm thử tự động (`node tests/verify_cockpit.js`), cập nhật toàn bộ tài liệu trong `docs/` và đẩy lên GitHub Pages (`origin/main`).

## Đang làm dở (bước cụ thể, lệnh đang chạy, nhánh)
- Không còn việc dở dang. Nhánh `main` đã sạch và đồng bộ.

## Bước tiếp theo (đánh số)
1. Tiếp tục theo dõi 7 ca còn tồn đọng chưa phản hồi ở Miền Trung chu kỳ `W38–W42` (4 ca của SUP `Nguyễn Thị Mỵ`, 2 ca của SUP `La Thành Nhân`, 1 ca của SUP `Trần Thanh Tuấn`). Hệ thống trên web sẽ tự động quét và cập nhật mỗi 30 giây khi các SUP điền thêm lên Google Sheet.
2. Khi có Google Sheet cho chu kỳ `W39–W43` tuần tới, cập nhật `GOOGLE_SHEET_ID` hoặc bổ sung chu kỳ mới tương tự kiến trúc đa chu kỳ hiện tại.

## Đang chờ chủ dự án
- Không có mục nào đang bị chặn.

## Lưu ý phát hiện hôm nay
- **Đảo chiều cột giữa W41 và W42 trên Google Sheet:** Ở sheet W41 cũ, Cột D là `PC active` và Cột E là `Region`; sang sheet W42 mới, Cột D là `Region` và Cột E là `PC Active`. Cả `scripts/sync_sheets.py` và `fetchGoogleSheetLive()` trong `app/index.html` đã được nâng cấp lên cơ chế **Header-Aware Detection** để tự động bắt đúng cột bất kể thứ tự.
- **Ô `Extra note` nhiều dòng (Multi-line CSV cell):** Các SUP (`Dương Nguyên Trà My`, `Phan Tú Sinh`) xuống dòng liệt kê từng mã model trong ô `Extra note` (ví dụ `EASV4271`, `EASV0737`, `EASV10177`). Hàm `parseCsvToRows(text)` trên trình duyệt đã được nâng cấp lên máy trạng thái RFC-4180 chuẩn để không bị tách nhầm dòng khi gặp ký tự `\n` bên trong dấu ngoặc kép `"..."`.
