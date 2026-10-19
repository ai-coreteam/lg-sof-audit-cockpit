# Bản Tóm Tắt Dự Án (Project Brief) — LG SOF Audit & Risk Governance Cockpit

## 1. Mục tiêu Cốt lõi (Objective)
Xây dựng và vận hành hệ thống **LG SOF Audit & Risk Governance Cockpit** tuân thủ tuyệt đối chuẩn nhận diện **LG Electronics Brand Identity V5.2 (Aug 2024)** nhằm giúp GTM Executive:
1. **Giám sát tiến độ phản hồi (Feedback Progress Tracking):** Theo dõi thời gian thực (Real-time 30s) tỷ lệ giải trình của đội ngũ PC Supervisor trên Google Sheet đối với các điểm bán có biến động trưng bày bất thường (Lệch >2 tuần kế trước, Lệch >8 so với 4 tuần trước, hoặc Data về 0).
2. **Thẩm định tính chân thực của phản hồi (Sanity & Authenticity Audit):** Tự động đối chiếu giữa mức độ biến động số liệu và nội dung giải trình (`Feedback` + `Extra note`), tách biệt minh bạch các ca giải trình hợp lệ (`PLAUSIBLE`), lỗi nhập liệu tuần cũ (`PC_ERROR`), lệch số kiểm đếm (`DATA_MISMATCH`), và nghi vấn đối phó (`SUSPICIOUS`).
3. **Quản trị rủi ro thương mại & thị phần kệ LG (Commercial & SOF Risk Governance):** Phát hiện sớm nguy cơ mất quầy kệ LG (`P0_CRITICAL`) và cơ hội chiếm đảo trưng bày khi đối thủ bị cắt giảm (`EXPAND_LG`).

## 2. Tiêu chí Thành công Đo lường được (Verifiable Success Criteria — KPIs)
| Mã KPI | Chỉ số đo lường | Mục tiêu (Target) | Phương thức kiểm chứng |
|---|---|---|---|
| **KPI-01** | Độ chính xác đồng bộ dữ liệu Google Sheet (`W38–W42`, `W37–W41`, `W36–W40`) | **100%** khớp từng dòng, từng cột (kể cả ô `Extra note` nhiều dòng và thứ tự cột `Region` / `PC Active` đảo chiều) | `node tests/verify_cockpit.js` (11/11 PASS) |
| **KPI-02** | Bảo toàn dữ liệu lịch sử đa chu kỳ (`3-Cycle Switcher`) | Chuyển đổi tức thời giữa **W42 Live** (16 ca), **W41 Middle Đã Chốt** (11 ca), **W40 Toàn Quốc** (632 ca) không mất trạng thái duyệt `localStorage` | Kiểm thử tự động trong `tests/verify_cockpit.js` |
| **KPI-03** | Tỷ lệ phân loại đúng kênh Đại lý (`DMX`, `CP`, `MM`, `VHC`, `Tradi`) | **100%** (bao gồm các biến thể viết liền `CAOPHONG` -> `CP`) | Kiểm chứng trên `EASV10177` (W42) và `EASV10176` (W41) |
| **KPI-04** | Tuân thủ chuẩn thương hiệu **LG BI V5.2** & Responsive Đa thiết bị | **100%** token màu (`#A50034`, `#FD312E`, `#F0ECE4`), font `LG EI`, không dùng emoji, hỗ trợ cả Desktop Table và Mobile Card | Kiểm tra giao diện trên Desktop & Mobile (`<= 768px`) |
