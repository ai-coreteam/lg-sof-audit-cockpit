# LG SOF Audit & Risk Governance Cockpit — Tổng Quan Dự Án (Project README)

> **Phiên bản:** 2.1 (Multi-Cycle W42 Live + W41 Closed + W40 National Baseline · Header-Aware Sync · Mobile Ready)  
> **Đơn vị sở hữu:** GTM Channel Development Strategist — LG Electronics Vietnam  
> **Nhận diện thương hiệu:** LG Brand Identity V5.2 (Heritage Red `#A50034`, Active Red `#FD312E`, Warm Gray `#F0ECE4`, Font `LG EI`)

---

## 1. Mục đích của Hệ thống (Why This Cockpit Exists)

Mỗi tuần, đội ngũ **PC (Promoter / Field Staff)** thu thập số lượng máy trưng bày (**Share of Floor — SOF**) của LG và các đối thủ cạnh tranh tại **1.690 cửa hàng điện máy** trên toàn quốc. Khi dữ liệu tuần mới có biến động bất thường so với tuần trước hoặc 4 tuần trước, hệ thống Google Sheet sẽ đánh dấu `x` để yêu cầu các **PC Supervisor (SUP)** vào giải trình nguyên nhân.

Hệ thống **SOF Audit & Risk Governance Cockpit** giúp GTM Executive quản trị tự động **4 trụ cột cốt lõi**:

1. **Giám sát Tiến độ Phản hồi (Feedback Progress Tracking):** Tự động đồng bộ thời gian thực (mỗi 30 giây) từ Google Sheet điều hành tuần hiện tại (`W38–W42`), thống kê tỷ lệ hoàn thành theo từng Khu vực và từng PC Supervisor.
2. **Thẩm định Tính Hợp lý & Ghi chú Thực địa (Sanity Check & Extra Note):** Tự động phát hiện các trường hợp trả lời qua loa (*"Shop báo tăng giảm đúng thực tế"* cho các ca dữ liệu rơi về 0 hoặc lệch $\ge 8$ sets), đồng thời tích hợp cột **`Extra note`** (hỗ trợ cả ghi chú nhiều dòng liệt kê mã model) và nhãn **Lịch sử W41 (`w41_hint`)** để phân biệt rõ ca đã xác minh thực địa với ca nghi vấn đối phó.
3. **Quản trị Rủi ro Thương mại & Thị phần Kệ LG (Commercial & SOF Risk):** Phân loại tự động mức độ rủi ro từ `P0_CRITICAL` (Mất quầy / sụt giảm trưng bày LG), `P1_COMMERCIAL` (Cắt giảm kệ đại lý), `P1_SUSPICIOUS` (Nghi vấn số liệu ảo), `P2_OPERATIONAL` (Lỗi PC báo sai tuần cũ hoặc lệch số kiểm đếm) đến `P3_NORMAL` (Luân chuyển bình thường / cơ hội chiếm đảo kệ).
4. **Cơ chế Hành động Tức thì (Actionable GTM Execution):** Cung cấp nút bấm 1-click để sao chép văn bản đôn đốc gửi trực tiếp cho Regional Leader hoặc từng PC Supervisor qua Zalo/Teams/Email, kèm bộ nút **Duyệt / Bác bỏ (Đòi ảnh)** lưu trữ tại trình duyệt theo từng chu kỳ (`W42`, `W41`, `W40`) và xuất báo cáo CSV.

---

## 2. Cấu trúc Thư mục Dự án (Project Directory Structure)

```text
SOF monitoring/
├── AGENTS.md                        # Quy tắc thường trực (S1-S3) & bản đồ điều hướng cho AI Agent
├── pm.config.json                   # Cấu hình kiểm chuẩn quản trị dự án (pm_check)
├── index.html                       # Bản chạy chính thức phục vụ GitHub Pages (Root)
├── assets/                          # Tài nguyên tĩnh ở Root phục vụ GitHub Pages
│   ├── w42_audit_cockpit.js         # Dataset chu kỳ W38–W42 (Google Sheet Live - 16 ca)
│   ├── w41_audit_cockpit.js         # Dataset chu kỳ W37–W41 (Miền Trung Đã Chốt - 11 ca)
│   ├── w40_audit_cockpit.js         # Dataset chu kỳ W36–W40 (Baseline Toàn Quốc - 632 ca)
│   ├── fonts/                       # Bộ font chính thức LG EI (Regular, SemiBold, Bold, ExtraBold)
│   ├── logo/                        # Logo LG Electronics chuẩn BI V5.2
│   └── slogan/                      # Slogan "Life's Good" chuẩn BI V5.2
├── app/
│   ├── index.html                   # Ứng dụng Web Cockpit mã nguồn chính (đồng bộ 1:1 với ./index.html)
│   └── assets/                      # Tài nguyên tĩnh trong thư mục app/
├── data/
│   ├── google_sheet_latest.xlsx     # File Excel gốc từ Google Sheet (64.487 dòng · 1.690 shop)
│   ├── w42_audit_cockpit.json       # Dữ liệu JSON đã thẩm định của chu kỳ W38–W42 (16 ca)
│   ├── w41_audit_cockpit.json       # Dữ liệu JSON đã thẩm định của chu kỳ W37–W41 (11 ca)
│   └── w40_audit_cockpit.json       # Dữ liệu JSON đã thẩm định của chu kỳ W36–W40 (632 ca)
├── scripts/
│   └── sync_sheets.py               # Script Python đồng bộ trực tiếp từ Google Sheet W42 & tái tính toán
├── tests/
│   └── verify_cockpit.js            # Bộ 11 bài kiểm thử tự động (Syntax, Parity, Multi-line CSV, Cycles)
└── docs/                            # Bộ tài liệu quản trị dự án (Documentation Suite)
    ├── README.md                    # Tổng quan kiến trúc và hướng dẫn nhanh (File này)
    ├── CURRENT_STATE.md             # Báo cáo phân tích số liệu điều hành mới nhất (W42, W41, W40)
    ├── HANDOFF.md                   # Biên bản bàn giao phiên làm việc
    ├── DATA_DICTIONARY.md           # Từ điển dữ liệu, cấu trúc cột Google Sheet & Ma trận Luật Thẩm định
    ├── DEPLOYMENT_GUIDE.md          # Hướng dẫn vận hành, đồng bộ dữ liệu & triển khai GitHub Pages
    ├── 00-brief/BRIEF.md            # Mục tiêu & KPIs đo lường dự án
    └── 04-releases/                 # Nhật ký phát hành (CHANGELOG.md) & Sổ tay khôi phục (RUNBOOK.md)
```

---

## 3. Liên kết Nguồn Dữ liệu (Data Sources)

- **Google Sheet Live Tuần Hiện Tại (`W38 – W42` · Miền Trung):**  
  `https://docs.google.com/spreadsheets/d/1lA6mxuh3yn6TMGWH8TIWOl6PWyKP5PeZ586sOnOGG40/edit?gid=1357809752#gid=1357809752`
- **Google Sheet Chu Kỳ Trước (`W37 – W41` · Miền Trung Đã Chốt):**  
  `https://docs.google.com/spreadsheets/d/1mpArbb5ShJqtWfgC8yB7pVv70tcTXK7XYKnxGWSGaws/edit?usp=sharing`
- **Bản chạy trực tuyến (GitHub Pages Live):**  
  `https://ai-coreteam.github.io/lg-sof-audit-cockpit/`
