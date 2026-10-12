import openpyxl
import json
from collections import Counter

wb = openpyxl.load_workbook("data/google_sheet_latest.xlsx", read_only=True)
ws = wb["Check theo CAT, theo Brand"]

header = None
rows = []
for i, row in enumerate(ws.iter_rows(values_only=True)):
    if i == 1:
        header = list(row)
    elif i > 1:
        if any(cell is not None for cell in row):
            rows.append(row)

print("Header:", header)
print("Total data rows:", len(rows))

col_map = {name: idx for idx, name in enumerate(header) if name}
print("Col map:", col_map)

c_diff2 = col_map.get("Chênh lệch hơn 2 so với tuần cũ")
c_diff8 = col_map.get("Chênh lệch hơn 8 so với 4 tuần trước")
c_zero = col_map.get("Data về 0")
c_fb = col_map.get("Feedback")
c_sup = col_map.get("PC Sup")
c_reg = col_map.get("Region")
c_pc_active = col_map.get("PC active")
c_brand = col_map.get("Brand")
c_cat = col_map.get("CAT")
c_shop = col_map.get("Code Shop")
c_shop_name = col_map.get("Tên Shop")

diff2_count = sum(1 for r in rows if r[c_diff2] and str(r[c_diff2]).strip().lower() in ["x", "1", "true"])
diff8_count = sum(1 for r in rows if r[c_diff8] and str(r[c_diff8]).strip().lower() in ["x", "1", "true"])
zero_count = sum(1 for r in rows if r[c_zero] and str(r[c_zero]).strip().lower() in ["x", "1", "true"])

flagged_rows = [r for r in rows if (
    (r[c_diff2] and str(r[c_diff2]).strip().lower() in ["x", "1", "true"]) or
    (r[c_diff8] and str(r[c_diff8]).strip().lower() in ["x", "1", "true"]) or
    (r[c_zero] and str(r[c_zero]).strip().lower() in ["x", "1", "true"])
)]
fb_count = sum(1 for r in flagged_rows if r[c_fb] and str(r[c_fb]).strip())

print(f"Diff > 2: {diff2_count}")
print(f"Diff > 8: {diff8_count}")
print(f"Data ve 0: {zero_count}")
print(f"Total flagged (any of 3): {len(flagged_rows)}")
print(f"Flagged with feedback: {fb_count} / {len(flagged_rows)}")

# Region distribution
regions = Counter(r[c_reg] for r in flagged_rows)
print("\nFlagged by Region:", regions)

# PC Active distribution
pc_actives = Counter(r[c_pc_active] for r in flagged_rows)
print("\nFlagged by PC Active:", pc_actives)

# Sample flagged rows
print("\nSample flagged rows:")
for r in flagged_rows[:5]:
    history = [r[col_map[w]] for w in ["W37", "W38", "W39", "W40", "W41"] if w in col_map]
    print({
        "shop": r[c_shop],
        "shop_name": r[c_shop_name],
        "sup": r[c_sup],
        "pc_active": r[c_pc_active],
        "region": r[c_reg],
        "cat": r[c_cat],
        "brand": r[c_brand],
        "history": history,
        "diff2": r[c_diff2],
        "diff8": r[c_diff8],
        "zero": r[c_zero],
        "feedback": r[c_fb]
    })
