#!/usr/bin/env python3
"""
LG Electronics - SOF Monitoring & Governance Cockpit
Automated Ingestion & Real-Time Sync Pipeline for Google Sheet
Target URL: https://docs.google.com/spreadsheets/d/1mpArbb5ShJqtWfgC8yB7pVv70tcTXK7XYKnxGWSGaws/edit?usp=sharing
"""

import os
import sys
import json
import urllib.request
import openpyxl

GOOGLE_SHEET_ID = "1mpArbb5ShJqtWfgC8yB7pVv70tcTXK7XYKnxGWSGaws"
SHEET_GID = "1357809752"
CSV_URL = f"https://docs.google.com/spreadsheets/d/{GOOGLE_SHEET_ID}/export?format=csv&gid={SHEET_GID}"
GVIZ_URL = f"https://docs.google.com/spreadsheets/d/{GOOGLE_SHEET_ID}/gviz/tq?tqx=out:json&sheet=Check%20theo%20CAT,%20theo%20Brand"
EXPORT_URL = f"https://docs.google.com/spreadsheets/d/{GOOGLE_SHEET_ID}/export?format=xlsx"

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
XLSX_PATH = os.path.join(PROJECT_ROOT, "data", "google_sheet_latest.xlsx")
OUTPUT_JSON_W41 = os.path.join(PROJECT_ROOT, "data", "w41_audit_cockpit.json")
OUTPUT_JS_W41 = os.path.join(PROJECT_ROOT, "app", "assets", "w41_audit_cockpit.js")
ROOT_ASSETS_JS_W41 = os.path.join(PROJECT_ROOT, "assets", "w41_audit_cockpit.js")

def load_store_master():
    store_map = {}
    if os.path.exists(XLSX_PATH):
        try:
            wb = openpyxl.load_workbook(XLSX_PATH, read_only=True)
            sheet_name = "Mapping PC SUP" if "Mapping PC SUP" in wb.sheetnames else "Sheet6"
            if sheet_name in wb.sheetnames:
                ws = wb[sheet_name]
                for idx, row in enumerate(ws.iter_rows(values_only=True)):
                    if idx > 1 and row[0]:
                        code = str(row[0]).strip()
                        dealer = "Tradi"
                        c_upper = str(row[1]).upper() if row[1] else ""
                        if "DML" in c_upper or "DMM" in c_upper or "DIEN MAY XANH" in c_upper:
                            dealer = "DMX"
                        elif "CP" in c_upper or "CAO PHONG" in c_upper or "CHO LON" in c_upper:
                            dealer = "CP"
                        elif "MM" in c_upper or "MEGA" in c_upper:
                            dealer = "MM"
                        elif "VHC" in c_upper or "HC" in c_upper:
                            dealer = "VHC"
                        
                        store_map[code] = {
                            "store_name": row[1] or "",
                            "region": row[2] or "",
                            "province": row[3] or "",
                            "district": row[4] or "",
                            "sup": row[5] or "",
                            "dealer": dealer,
                            "active_pc": int(float(row[11])) if len(row) > 11 and row[11] is not None else 0
                        }
        except Exception as e:
            print("Notice: cannot read XLSX store master:", e)
    return store_map

def evaluate_feedback(record):
    fb_raw = (record.get("feedback_raw") or "").strip()
    brand = record.get("brand", "")
    w_cur = record.get("w41", 0)
    w_prev = record.get("w40", 0)
    delta = w_cur - w_prev
    flags = record.get("flags", {})

    if not fb_raw:
        return {
            "status": "CHƯA_FEEDBACK",
            "validity": "PENDING",
            "validity_label": "Chưa có phản hồi",
            "validity_desc": "PC SUP chưa điền giải trình trên Google Sheet",
            "risk_level": "HIGH",
            "risk_label": "Rủi ro tồn đọng",
            "risk_desc": "Cần đôn đốc SUP phản hồi gấp trước hạn chốt tuần",
            "action_code": "PUSH_SUP",
            "action_title": "Đôn đốc phản hồi gấp",
            "action_detail": "Gửi tin nhắn cảnh báo yêu cầu SUP xác minh trong ngày."
        }

    fb_lower = fb_raw.lower()
    extra_note = (record.get("extra_note") or "").strip()
    extra_lower = extra_note.lower()

    # Rule SAN-EXTRA: If SUP provided an Extra note, this case is EXCLUSIVELY clarified via Extra Note
    if extra_note:
        # Check if it's count correction / data mismatch
        if any(k in extra_lower for k in ["số đúng là", "không phải", "khổng phải", "sets", "sai số", "nhập nhầm"]):
            return {
                "status": "ĐÃ_FEEDBACK",
                "validity": "DATA_MISMATCH",
                "validity_label": "Sai lệch số thực tế",
                "validity_desc": f"SUP bổ sung: \"{extra_note}\". Số trên hệ thống không khớp với thực tế kiểm đếm.",
                "risk_level": "MEDIUM",
                "risk_label": "Dữ liệu Sheet bị lệch số",
                "risk_desc": "Số liệu trên Sheet khai khống so với thực tế. Cần hiệu chỉnh lại số đúng.",
                "action_code": "CORRECT_DATA",
                "action_title": "Bác bỏ & Hiệu chỉnh số liệu",
                "action_detail": f"Yêu cầu sửa số liệu chính thức theo ghi chú thực tế: '{extra_note}'; kiểm điểm PC."
            }

        # Check if competitor shelf cut / delisting
        if any(k in extra_lower for k in ["cắt", "bỏ mẫu", "đảo"]) and brand != "LG":
            return {
                "status": "ĐÃ_FEEDBACK",
                "validity": "PLAUSIBLE",
                "validity_label": "Đã làm rõ (Extra Note)",
                "validity_desc": f"SUP bổ sung thông tin thực địa: \"{extra_note}\".",
                "risk_level": "LOW",
                "risk_label": f"Đối thủ {brand} bị cắt giảm",
                "risk_desc": f"Thị trường thu hẹp trưng bày model đối thủ {brand} tại cửa hàng.",
                "action_code": "EXPAND_LG",
                "action_title": "Tận dụng chiếm đảo kệ",
                "action_detail": f"{brand} bị cắt giảm trưng bày. Đề xuất làm việc với shop để đưa thêm TV LG vào đảo trống."
            }

        # All other Extra Notes: Fully clarify the case and remove from SUSPICIOUS
        return {
            "status": "ĐÃ_FEEDBACK",
            "validity": "PLAUSIBLE",
            "validity_label": "Đã làm rõ (Extra Note)",
            "validity_desc": f"SUP bổ sung: \"{extra_note}\". Đã làm rõ nguyên nhân biến động thực tế.",
            "risk_level": "LOW",
            "risk_label": "Biến động đã làm rõ",
            "risk_desc": "Cửa hàng đã giải trình biến động thực tế.",
            "action_code": "ACCEPT",
            "action_title": "Phê duyệt giải trình (Có Extra Note)",
            "action_detail": f"Chấp thuận do SUP đã bổ sung nguyên nhân thực địa: '{extra_note}'."
        }

    # Rule SAN-01: Data drops to 0 but supervisor claims "normal fluctuations"
    if flags.get("zero_drop") and "tăng giảm đúng thực tế" in fb_lower:
        return {
            "status": "ĐÃ_FEEDBACK",
            "validity": "SUSPICIOUS",
            "validity_label": "Nghi vấn đối phó",
            "validity_desc": f"Dữ liệu về 0 nhưng ghi 'tăng giảm đúng thực tế'. Cần ảnh chụp quầy.",
            "risk_level": "CRITICAL" if brand == "LG" else "HIGH",
            "risk_label": "Mất SOF LG" if brand == "LG" else "Nghi vấn gian lận",
            "risk_desc": f"Nguy cơ mất trắng trưng bày {brand} tại shop nhưng phản hồi qua loa",
            "action_code": "REJECT_AND_AUDIT",
            "action_title": "Bác bỏ & Đòi ảnh thực tế",
            "action_detail": "Từ chối duyệt. Yêu cầu SUP gửi ảnh chụp kệ thực tế trong 24h."
        }

    # Rule SAN-02: Radical swing >= 8 sets with superficial explanation
    if flags.get("diff_8_4w") and "tăng giảm đúng thực tế" in fb_lower:
        return {
            "status": "ĐÃ_FEEDBACK",
            "validity": "SUSPICIOUS",
            "validity_label": "Nghi vấn đối phó",
            "validity_desc": f"Biến động lệch >8 sets nhưng giải trình chung chung, thiếu căn cứ.",
            "risk_level": "HIGH",
            "risk_label": "Nghi vấn đối phó",
            "risk_desc": "Khả năng copy-paste giải trình hàng loạt không qua kiểm tra thực tế",
            "action_code": "REJECT_AND_AUDIT",
            "action_title": "Yêu cầu ảnh & Biên bản",
            "action_detail": "Yêu cầu SUP giải trình chi tiết lý do biến động đột biến."
        }

    # Rule SAN-03: PC error admission
    if "báo sai" in fb_lower or "nhập sai" in fb_lower or "điều chỉnh lại" in fb_lower:
        return {
            "status": "ĐÃ_FEEDBACK",
            "validity": "PC_ERROR",
            "validity_label": "Thừa nhận PC báo sai",
            "validity_desc": "SUP thừa nhận nhân viên PC báo sai số tuần trước, tuần này sửa lại",
            "risk_level": "MEDIUM",
            "risk_label": "Lỗi vận hành PC",
            "risk_desc": "Số liệu quá khứ không đáng tin cậy. Cần kiểm điểm kỷ luật PC.",
            "action_code": "COACH_PC",
            "action_title": "Kiểm điểm & Đào tạo PC",
            "action_detail": "Yêu cầu SUP đào tạo lại quy trình kiểm đếm cho PC tại điểm bán."
        }

    # Commercial Risk: Delisting or shelf cut
    if any(k in fb_lower for k in ["cắt shop", "bỏ quầy", "dồn quầy", "hạ bục", "thu hồi"]):
        risk = "CRITICAL" if brand == "LG" else "HIGH"
        return {
            "status": "ĐÃ_FEEDBACK",
            "validity": "PLAUSIBLE",
            "validity_label": "Hợp lý (Có căn cứ)",
            "validity_desc": "Giải trình phản ánh việc đại lý cắt giảm hoặc thu hồi quầy kệ",
            "risk_level": risk,
            "risk_label": "Rủi ro mất quầy LG" if brand == "LG" else "Đại lý cắt quầy kệ",
            "risk_desc": f"Đại lý đang thu hẹp mặt bằng trưng bày {brand}",
            "action_code": "ESCALATE_KAM",
            "action_title": "Can thiệp KAM khẩn cấp",
            "action_detail": "Báo cáo Head of GTM & làm việc với KAM để bảo vệ hợp đồng quầy kệ."
        }

    # LG Display drop risk
    if brand == "LG" and delta < 0 and abs(delta) >= 2:
        return {
            "status": "ĐÃ_FEEDBACK",
            "validity": "PLAUSIBLE",
            "validity_label": "Hợp lý đạt chuẩn",
            "validity_desc": f"LG giảm {abs(delta)} sets. Cần theo dõi để tránh mất thị phần SOF.",
            "risk_level": "HIGH",
            "risk_label": "Rủi ro giảm trưng bày LG",
            "risk_desc": f"Số lượng trưng bày của LG bị giảm {abs(delta)} máy",
            "action_code": "ESCALATE_KAM",
            "action_title": "Theo dõi SOF & Kiểm tra shop",
            "action_detail": "Kiểm tra lý do giảm model LG và đôn đốc đưa thêm hàng trưng bày."
        }

    # Normal Plausible explanation
    return {
        "status": "ĐÃ_FEEDBACK",
        "validity": "PLAUSIBLE",
        "validity_label": "Hợp lý đạt chuẩn",
        "validity_desc": "Lý do phù hợp với biến động luân chuyển hàng hóa thực tế",
        "risk_level": "LOW",
        "risk_label": "Biến động bình thường",
        "risk_desc": "Thay đổi số lượng do relayout hoặc luân chuyển model bình thường",
        "action_code": "ACCEPT",
        "action_title": "Phê duyệt giải trình",
        "action_detail": "Chấp thuận dữ liệu đưa vào báo cáo SOF chính thức."
    }

def fetch_live_csv():
    print(f"[1/3] Fetching live data via Google Sheets CSV Export from {CSV_URL}...")
    req = urllib.request.Request(CSV_URL, headers={"User-Agent": "Mozilla/5.0"})
    content = urllib.request.urlopen(req).read().decode("utf-8", errors="ignore")
    import csv, io
    reader = csv.reader(io.StringIO(content))
    return list(reader)

def sync_live():
    store_master = load_store_master()
    rows = fetch_live_csv()
    print(f"[2/3] Processing {len(rows)} rows from Google Sheets calculation engine...")

    records = []
    for i, r in enumerate(rows):
        if i <= 1 or len(r) < 16:
            continue

        d2_str = str(r[12] or "").strip().lower()
        d8_str = str(r[13] or "").strip().lower()
        z0_str = str(r[14] or "").strip().lower()

        is_d2 = "x" in d2_str or d2_str == "1"
        is_d8 = "x" in d8_str or d8_str == "1"
        is_z0 = "x" in z0_str or z0_str == "1"

        if is_d2 or is_d8 or is_z0:
            shop_code = str(r[0] or "").strip()
            shop_name = r[1] or store_master.get(shop_code, {}).get("store_name", "")
            sup = r[2] or store_master.get(shop_code, {}).get("sup", "")
            pc_act_raw = r[3]
            try:
                pc_act = int(float(pc_act_raw)) if pc_act_raw and pc_act_raw.strip() else store_master.get(shop_code, {}).get("active_pc", 0)
            except (ValueError, TypeError):
                pc_act = store_master.get(shop_code, {}).get("active_pc", 0)
            reg = r[4] or "Middle"
            cat = r[5] or ""
            brand = r[6] or ""
            try:
                w37 = int(float(r[7])) if r[7] and r[7].strip() else 0
                w38 = int(float(r[8])) if r[8] and r[8].strip() else 0
                w39 = int(float(r[9])) if r[9] and r[9].strip() else 0
                w40 = int(float(r[10])) if r[10] and r[10].strip() else 0
                w41 = int(float(r[11])) if r[11] and r[11].strip() else 0
            except (ValueError, TypeError):
                w37 = w38 = w39 = w40 = w41 = 0
            fb = str(r[15] or "").strip()
            extra_note = str(r[17] or "").strip() if len(r) > 17 else ""

            rec = {
                "id": f"{shop_code}_{cat}_{brand}",
                "store_code": shop_code,
                "store_name": shop_name,
                "dealer": store_master.get(shop_code, {}).get("dealer", "DMX"),
                "channel": "MC" if store_master.get(shop_code, {}).get("dealer") in ["DMX", "CP", "MM", "VHC"] else "Tradi",
                "region": reg,
                "province": store_master.get(shop_code, {}).get("province", ""),
                "district": store_master.get(shop_code, {}).get("district", ""),
                "sup": sup,
                "active_pc": pc_act,
                "category": cat,
                "brand": brand,
                "w37": w37, "w38": w38, "w39": w39, "w40": w40, "w41": w41,
                "delta_wow": w41 - w40,
                "flags": {
                    "diff_8_4w": is_d8,
                    "diff_2_prev": is_d2,
                    "zero_drop": is_z0,
                    "lg_drop_50": bool(brand == "LG" and w40 > 0 and w41 <= w40 * 0.5)
                },
                "feedback_raw": fb,
                "extra_note": extra_note
            }
            rec["eval"] = evaluate_feedback(rec)
            records.append(rec)

    data_payload = {
        "audit_cycle": "W37-W41 (Google Sheet Live)",
        "cycle_short": "W41",
        "google_sheet_url": f"https://docs.google.com/spreadsheets/d/{GOOGLE_SHEET_ID}/edit",
        "weeks": ["W37", "W38", "W39", "W40", "W41"],
        "total_records": len(records),
        "records": records
    }

    print(f"[3/3] Saving {len(records)} live audited records...")
    with open(OUTPUT_JSON_W41, "w", encoding="utf-8") as f:
        json.dump(data_payload, f, ensure_ascii=False, indent=2)

    with open(OUTPUT_JS_W41, "w", encoding="utf-8") as f:
        f.write("// LG Electronics SOF Governance Cockpit - Live Google Sheet W41 Dataset\n")
        f.write("window.SOF_AUDIT_DATA_W41 = ")
        json.dump(data_payload, f, ensure_ascii=False, indent=2)
        f.write(";\n")

    print(f"      Saved JSON: {OUTPUT_JSON_W41}")
    print(f"      Saved JS: {OUTPUT_JS_W41}")

    if os.path.exists(os.path.dirname(ROOT_ASSETS_JS_W41)):
        with open(ROOT_ASSETS_JS_W41, "w", encoding="utf-8") as f:
            f.write("// LG Electronics SOF Governance Cockpit - Live Google Sheet W41 Dataset\n")
            f.write("window.SOF_AUDIT_DATA_W41 = ")
            json.dump(data_payload, f, ensure_ascii=False, indent=2)
            f.write(";\n")
        print(f"      Saved Root JS: {ROOT_ASSETS_JS_W41}")

    print("SUCCESS: Real-time sync completed successfully!")

if __name__ == "__main__":
    sync_live()
