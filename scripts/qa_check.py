import json
import os

ANNOTATION_FOLDER = "../annotations"

def check_annotation(filepath):
    with open(filepath, 'r') as f:
        data = json.load(f)
    errors = []

    x, y, w, h = data["bbox"]
    if w <= 10 or h <= 10:
        errors.append("Bounding box too small.")
    if x < 0 or y < 0:
        errors.append("Negative coordinates.")
    if not data.get("label"):
        errors.append("Missing label.")

    return errors

all_files = [f for f in os.listdir(ANNOTATION_FOLDER) if f.endswith(".json")]

for file in all_files:
    full_path = os.path.join(ANNOTATION_FOLDER, file)
    issues = check_annotation(full_path)
    if issues:
        print(f"❌ Issues in {file}:")
        for issue in issues:
            print("  -", issue)
    else:
        print(f"✅ {file} passed QA.")
