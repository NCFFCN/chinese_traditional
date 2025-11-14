import os
import json
import csv

FOLDER_PATH = r"G:\Program Files (x86)\Steam\steamapps\common\ZERO Sievert\ZS_vanilla\gamedata"
OUTPUT_CSV = "zs_item_data.csv"


def write_to_csv(data_rows):
    with open(OUTPUT_CSV, mode="w", encoding="utf-8", newline="") as csvfile:
        writer = csv.writer(csvfile)
        for row in data_rows:
            writer.writerow(row)


def extract_data_from_json(file_path, filename_no_ext):
    data_rows = []
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            json_data = json.load(f)

        if "data" not in json_data or not isinstance(json_data["data"], dict):
            print(f"[SKIP] No 'data' section in {filename_no_ext}.json")
            return data_rows

        data_section = json_data["data"]

        for key, value in data_section.items():
            if not isinstance(value, dict) or "basic" not in value:
                continue

            basic_data = value["basic"]
            name = basic_data.get("name", "")
            description = basic_data.get("description", "")

            if name.strip() != "":
                data_rows.append([name, filename_no_ext])

            if description.strip() != "":
                data_rows.append([description, filename_no_ext])

    except json.JSONDecodeError as e:
        print(f"[ERROR] Failed to parse JSON in {filename_no_ext}.json: {e}")
    except Exception as e:
        print(f"[ERROR] Unexpected error reading {filename_no_ext}.json: {e}")

    return data_rows


all_rows = []

if not os.path.exists(FOLDER_PATH):
    print(f"❌ Folder not found: {FOLDER_PATH}")
    exit(0)

for filename in os.listdir(FOLDER_PATH):
    file_path = os.path.join(FOLDER_PATH, filename)

    if not os.path.isfile(file_path):
        continue

    if not filename.lower().endswith(".json"):
        continue

    filename_no_ext = os.path.splitext(filename)[0]

    rows = extract_data_from_json(file_path, filename_no_ext)
    all_rows.extend(rows)

if all_rows:
    write_to_csv(all_rows)
    print(f"\n✅ Successfully extracted {len(all_rows)} rows to '{OUTPUT_CSV}'")
