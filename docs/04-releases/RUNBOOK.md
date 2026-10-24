# Sổ tay triển khai & khôi phục — SOF monitoring

## 1. Điểm quay lại (mỗi lần phát hành 1 dòng, viết TRƯỚC khi phát hành)
| Phát hành | Điểm quay lại | Cách quay lại |
|---|---|---|
| `v2.1.1` (2026-10-19) | `7231346` (`v2.1.0` W42 Initial 9/16 Release) | `git checkout 7231346 -- app/ index.html assets/ data/ scripts/ && git commit -m "Rollback to v2.1.0 (7231346)" && git push origin main` |
| `v2.1.0` (2026-10-19) | `9df1f2c` (`W37–W41` 100% Extra Note Release) | `git checkout 9df1f2c -- app/ index.html assets/ data/ scripts/ && git commit -m "Rollback to v2.0.0 (9df1f2c)" && git push origin main` |
| `v2.0.0` (2026-10-12) | `321258e` | `git checkout 321258e -- app/ index.html assets/ data/ scripts/` |

## 2. Quy trình phát hành
1. Mọi bộ test đạt (`node tests/verify_cockpit.js` = 11/11 PASS).
2. Viết dòng CHANGELOG + dòng quay lại; `pm_check.py . --release v2.1.1` = 0 ERROR.
3. `secret_scan.py --staged` = 0.
4. Commit, tag, fetch + gộp remote (không ép), push lên `origin/main` (`https://github.com/ai-coreteam/lg-sof-audit-cockpit`).
5. Triển khai GitHub Pages (`https://ai-coreteam.github.io/lg-sof-audit-cockpit/`); kiểm bản chạy thật.
6. Cập nhật `docs/CURRENT_STATE.md` và `docs/HANDOFF.md`.

## 3. Sao lưu dữ liệu
| Ngày | Tên / vị trí bản sao | Đã đối chiếu (số dòng) | Trước thao tác nào |
|---|---|---|---|
| 2026-10-19 | `data/w41_audit_cockpit.json` & `assets/w41_audit_cockpit.js` | 11 bản ghi (giữ nguyên 100%) | Tích hợp chu kỳ mới `W38–W42` vào `data/w42_audit_cockpit.json` |
| 2026-10-19 | `data/w40_audit_cockpit.json` & `assets/w40_audit_cockpit.js` | 632 bản ghi (giữ nguyên 100%) | Tích hợp chu kỳ mới `W38–W42` |

## 4. Xử lý sự cố
1. Xác nhận hiện tượng (tái hiện, ảnh, thời điểm).
2. Có từ trước hay do lần phát hành gần nhất? (so với commit `9df1f2c`)
3. Nếu do lần phát hành gần nhất và nghiêm trọng: quay lại (§1), kiểm bản chạy thật, rồi mới điều tra.
4. Ghi sự cố vào `docs/07-risks/LESSONS.md`.
