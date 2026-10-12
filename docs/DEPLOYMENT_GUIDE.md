# SOF Audit Cockpit — Cẩm Nang Triển Khai Web Online & Chia Sẻ (Deployment Guide)

*Last Updated: 2026-10-12 · Target Org: `ai-coreteam` · Architecture: Serverless Static Single-Page App (SPA)*

---

## 1. Thông Tin Truy Cập Chính Thức (Official URLs) [VERIFIED]

| Hạng Mục | Đường Dẫn Trực Tuyến | Mục Đích Sử Dụng |
|---|---|---|
| **🌐 Web Online (GitHub Pages)** | **[https://ai-coreteam.github.io/lg-sof-audit-cockpit/](https://ai-coreteam.github.io/lg-sof-audit-cockpit/)** | **Link chia sẻ chính thức** cho GTM Strategist, C-Level, Regional Leaders và PC Supervisors xem trên máy tính & điện thoại. |
| **📦 GitHub Repository** | **[https://github.com/ai-coreteam/lg-sof-audit-cockpit](https://github.com/ai-coreteam/lg-sof-audit-cockpit)** | Quản lý mã nguồn, lịch sử cam kết, hệ thống tài liệu và bộ công cụ đồng bộ dữ liệu. |
| **📊 Master Google Sheet** | **[SOF check W37-W41 (Middle)](https://docs.google.com/spreadsheets/d/1mpArbb5ShJqtWfgC8yB7pVv70tcTXK7XYKnxGWSGaws/edit?usp=sharing)** | Cơ sở dữ liệu nguồn nhập liệu giải trình của PC Supervisors. |

---

## 2. Kiến Trúc Hoạt Động Trên Môi Trường Trực Tuyến (Serverless Cloud Architecture)

Hệ thống được thiết kế theo kiến trúc **Zero-Backend (Serverless Client-Side Engine)**:

```mermaid
graph TD
    subgraph Data Layer (Google Cloud)
        GS[(Master Google Sheet\nCheck theo CAT, theo Brand)]
    end

    subgraph Hosting Layer (GitHub Cloud)
        GH_REPO[GitHub Repository\nai-coreteam/lg-sof-audit-cockpit]
        GH_PAGES[GitHub Pages CDN Engine\nhttps://ai-coreteam.github.io/lg-sof-audit-cockpit/]
    end

    subgraph Client Runtime (Any Browser / Any Device)
        BROWSER[Trình Duyệt Của Người Dùng\nLaptop, PC, iPhone, Android]
        CACHE[Pre-bundled Datasets\nW41 Middle & W40 National]
        LIVE_SYNC[Client Live Engine\nFetch CSV qua CORS mở]
        STATE[Client LocalStorage\nLưu quyết định Duyệt / Bác bỏ]
    end

    GH_REPO -->|Tự động triển khai branch main| GH_PAGES
    GH_PAGES -->|Phục vụ mã nguồn HTML/CSS/JS| BROWSER
    BROWSER --> CACHE
    BROWSER -->|Tự động đồng bộ mỗi 30s & khi focus tab| GS
    GS -->|Phản hồi luồng dữ liệu CSV mới nhất| LIVE_SYNC
    LIVE_SYNC --> BROWSER
    BROWSER <--> STATE
```

### Ưu Điểm Tuyệt Đối Của Kiến Trúc:
1. **Không Tốn Chi Phí Máy Chủ (Zero-Cost Hosting):** Vận hành 100% trên nền tảng GitHub Pages CDN toàn cầu của GitHub.
2. **Không Cần Đăng Nhập / Phân Quyền Phức Tạp:** Link công khai cho nội bộ, bất kỳ nhân sự nào có link đều mở được ngay trên điện thoại hoặc máy tính mà không gặp rào cản firewall nhà máy.
3. **Đồng Bộ Dữ Liệu Hai Tầng (Dual-Layer Sync):**
   - **Tầng 1 (Tức thì):** File `index.html` tích hợp sẵn dữ liệu đệm (cached datasets) giúp trang tải tức thì trong `< 0.5s` mà không bao giờ bị màn hình trắng kể cả khi mạng yếu.
   - **Tầng 2 (Real-time Live):** Trình duyệt tự động gọi API xuất CSV của Google Sheet để quét các phản hồi mới của PC SUP mỗi 30 giây và tính toán lại các cờ bất thường trong bộ nhớ RAM trình duyệt.

---

## 3. Quy Trình Cập Nhật & Đẩy Code Lên GitHub (Developer Handover)

Khi có bất kỳ thay đổi nào về giao diện, quy tắc kiểm tra (Sanity Check) hoặc bổ sung tài liệu:

```bash
# 1. Di chuyển vào thư mục dự án
cd "/Users/macbook/Documents/antigravity/AI study/LG other/SOF monitoring"

# 2. Cập nhật dữ liệu từ Google Sheet (tùy chọn)
python3 scripts/sync_sheets.py

# 3. Đồng bộ code từ app sang root (nếu có sửa đổi trong app/)
cp app/index.html ./index.html
cp -r app/assets/* ./assets/

# 4. Kiểm tra trạng thái git
git status

# 5. Commit và đẩy lên GitHub
git add .
git commit -m "feat: [Mô tả nội dung thay đổi]"
git push origin main
```

Sau khi `git push origin main`, GitHub Pages sẽ tự động kích hoạt tiến trình triển khai và cập nhật website online trong vòng **15 – 30 giây**.

---

## 4. Hướng Dẫn Chia Sẻ Link Cho Các Đối Tượng Người Dùng

### A. Gửi Cho C-Level / GTM Director:
> *"Kính gửi Anh/Chị, GTM đã triển khai Hệ Thống Giám Sát & Quản Trị Rủi Ro SOF (W37–W41) trực tuyến tại đường dẫn: https://ai-coreteam.github.io/lg-sof-audit-cockpit/ . Hệ thống tự động đồng bộ real-time với Google Sheet của PC SUP, phân loại rủi ro mất quầy LG và kiểm soát giải trình qua loa."*

### B. Gửi Cho Regional Leaders & PC Supervisors:
> *"Team có thể truy cập link https://ai-coreteam.github.io/lg-sof-audit-cockpit/ trên điện thoại di động để kiểm tra tiến độ giải trình của khu vực mình phụ trách. Bấm vào tab 'Dạng Thẻ' để xem các ca cần bổ sung thông tin thực địa (Extra Note)."*
