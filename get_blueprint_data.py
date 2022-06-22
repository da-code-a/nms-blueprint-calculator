import json
import csv
from unicodedata import category

def find_unmatched_names() -> list:
    unmatched = []
    with open('items.csv', 'r') as f:
        csv_items = [{k: v for k, v in row.items()} for row in csv.DictReader(f, skipinitialspace=True)]
    with open('converted.json', 'r') as f:
        editor_items = json.load(f)
    for item in csv_items:
        found = 0
        for category in editor_items["items"]:
            for editor_item in editor_items["items"][category]:
                if item["Name"] == editor_item["_name"]:
                    found = 1
                    break
        if not found:
            unmatched.append(item["Name"])
    return unmatched

def clean_converted() -> dict:
    clean_dict = {}
    with open('converted.json', 'r') as f:
        editor_items = json.load(f)
    unamtched_names = find_unmatched_names()
    for category in editor_items["items"]:
        for item in editor_items["items"][category]:
            if item["_name"] not in unamtched_names:
                clean_dict[item["_name"]] = item
    return clean_dict

def make_blueprint_entries() -> dict:
    blueprints = {}
    with open('items.csv', 'r') as f:
        csv_items = [{k: v for k, v in row.items()} for row in csv.DictReader(f, skipinitialspace=True)]
    cleaned = clean_converted()
    for item in csv_items:
        category = item["Category"].lower().replace(" ", "_")
        item_key = item["Name"].lower().replace(" ", "_")
        if category not in blueprints:
            blueprints[category] = {}
        this_item = {
            "owned": False,
            "name": item["Name"],
            "cost": int(item["Cost"]),
            "requires": item["Requirements"].split(', ') if item["Requirements"] else None
        }
        if item["Name"] in cleaned:
            this_item["image_file"] = cleaned[item["Name"]]["_icon"]
        else:
            this_item["image_file"] = None
        blueprints[category][item_key] = this_item
    return blueprints

def save_blueprints() -> None:
    with open('nms_blueprint_calculator/static/blueprints.json', 'w') as f:
        json.dump(make_blueprint_entries(), f, indent=2)



if __name__ == '__main__':
    save_blueprints()
