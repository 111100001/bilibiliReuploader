import json

with open('items.json', 'r', encoding='utf-8') as f:
    items = json.load(f)

with open('identifiers.json', 'r', encoding='utf-8') as f2:
    identifiers = json.load(f2)

# Collect all item identifiers into a set for faster lookup
item_identifiers = {item['identifier'] for item in items}

# Find identifiers in identifiers.json that are not in items.json
for identifier in identifiers:
    if identifier['identifier'] not in item_identifiers:
        print(identifier['identifier'])
