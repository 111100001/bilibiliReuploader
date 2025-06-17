from internetarchive import get_item
import json

item = get_item("BiliBili-BV1BX4y1P7G7_p5-8")

print(item.metadata)
with open("output.json", "w", encoding="utf-8") as f:
    json.dump(item.item_metadata, f, ensure_ascii=False, indent=2)
