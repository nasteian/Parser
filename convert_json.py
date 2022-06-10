import json


def save_json(items, path):
    """Saving data to a json file"""
    with open(path, 'w', newline='', encoding='utf-8') as file:
        json.dump(items, file, indent=4, ensure_ascii=False)
    print("File {} has been saved".format(path))

