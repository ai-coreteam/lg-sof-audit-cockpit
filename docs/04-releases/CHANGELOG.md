# Nhật ký thay đổi — SOF monitoring
Mới nhất ở trên. Mỗi thay đổi 1 dòng. Cột Kiểm thử phải có số (N/N). Quay lại = phiên bản / tag trước.

| Ngày | Phiên bản | Thay đổi | Duyệt | Người dùng thấy? | Kiểm thử | Quay lại |
|---|---|---|---|---|---|---|
| 2026-10-19 | `v2.1.1` | Đồng bộ bản cập nhật mới nhất trên Google Sheet `W38–W42` (**16/16 ca hoàn thành 100%** kèm **16/16 Extra Note** từ cả 5 PC SUP); tinh chỉnh bộ lọc từ khoá `DATA_MISMATCH` (bỏ từ đơn `sets` để ca `EASV4491` tăng `+6 sets LG` được phân loại đúng `PLAUSIBLE`). | Preview lại update mới | Có | 11/11 | `7231346` |
| 2026-10-19 | `v2.1.0` | Tích hợp Google Sheet tuần mới `W38–W42` (`1lA6mxuh3yn6TMGWH8TIWOl6PWyKP5PeZ586sOnOGG40`, 16 ca Miền Trung: 9 đã feedback / 7 tồn); nâng cấp bộ chuyển đổi 3 chu kỳ (`W42 Live`, `W41 Middle Đã Chốt`, `W40 Baseline Toàn Quốc`); tự động nhận diện cột `Region`/`PC Active` đảo chiều & parser CSV đa dòng; hiển thị gợi ý lịch sử W41 (`w41_hint`) và sửa phân loại đại lý `CAOPHONG` -> `CP`. | Phương án 1A, 2A, 3A | Có | 11/11 | `9df1f2c` |
| 2026-10-12 | `v2.0.0` | Hoàn thiện Cockpit chu kỳ `W37–W41` Miền Trung (11/11 ca giải trình), bổ sung cột `Extra note`, luật `Rule SAN-EXTRA` và giao diện Mobile Card/Table. | Đã duyệt | Có | 10/10 | `321258e` |
