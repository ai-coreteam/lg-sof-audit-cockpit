# AGENTS.md — SOF monitoring
> Điểm bắt đầu cho mọi AI agent và thành viên mới. Đọc file này trước, rồi `docs/CURRENT_STATE.md` và `docs/HANDOFF.md`.

## Quy tắc thường trực của chủ dự án (bắt buộc, giữ nguyên văn — áp dụng kể cả khi tin nhắn không nhắc lại)
> **S1.** "Always apply my Karpathy epistemics skill when working, no hallucination, no lazy, keep the current skills design system."
> **S2.** "Only fix the item having issue. Do not change any app functions that I already approved."
> **S3.** "Always crosscheck if the change affect the functions indirectly to ensure the system can operate smoothly."
Mọi báo cáo cuối kết thúc bằng bảng "Kiểm quy tắc thường trực" (S1–S3, kèm bằng chứng).

## Quy tắc (bắt buộc)
1. Chức năng đã duyệt giữ nguyên. Chỉ sửa đúng chỗ có lỗi; đổi hành vi phải được chủ dự án duyệt (đề xuất trước).
2. Có bằng chứng mới khẳng định. Ghi rõ mức chắc chắn. Báo cáo tách: đã làm / đã kiểm / chưa kiểm.
3. Tìm nguyên nhân gốc và kiểm "có từ trước hay do mình" trước khi sửa.
4. Mỗi thay đổi đều rà ảnh hưởng gián tiếp (phạm vi ảnh hưởng).
5. Mỗi lỗi sửa có test; mọi bộ test phải đạt; ghi số vào CHANGELOG.
6. Mỗi lần phát hành có điểm quay lại ghi trước khi phát hành; sao lưu dữ liệu trước thao tác xoá / ghi đè.
7. Cập nhật tài liệu cùng lần thay đổi. Không bao giờ đưa mật khẩu / khoá lên git (quét trước khi push).
8. Dữ liệu thật chỉ đọc, trừ khi chủ dự án duyệt. Việc chỉ chủ dự án làm được thì liệt kê, không tự làm.
9. Giữ hệ thống thiết kế đã duyệt và quy chuẩn thương hiệu trên mọi sản phẩm hình ảnh.

## Bản đồ
| Cần | Ở đâu |
|---|---|
| Thông tin hiện hành | `docs/CURRENT_STATE.md` |
| Phiên trước dừng ở đâu | `docs/HANDOFF.md` |
| Mục tiêu, tiêu chí thành công | `docs/00-brief/BRIEF.md` |
| Lịch sử thay đổi / quay lại | `docs/04-releases/CHANGELOG.md` · `docs/04-releases/RUNBOOK.md` |
| Từ điển dữ liệu & Quy tắc | `docs/DATA_DICTIONARY.md` |
| Hướng dẫn triển khai | `docs/DEPLOYMENT_GUIDE.md` |
| Bộ kiểm thử tự động | `tests/verify_cockpit.js` |

## Lệnh
| Việc | Lệnh |
|---|---|
| Chạy toàn bộ test | `node tests/verify_cockpit.js` |
| Đồng bộ dữ liệu Google Sheet | `python3 scripts/sync_sheets.py` |
| Build | `cp app/index.html index.html` |
| Cổng kiểm PM | `python3 /Users/macbook/.gemini/config/skills/project-management/scripts/pm_check.py .` |
| Quét bí mật | `python3 /Users/macbook/.gemini/config/skills/project-management/scripts/secret_scan.py --staged` |

## Không bao giờ commit
- `.env`
- `feedback/*`
- `scratch/`
- `archive/`
