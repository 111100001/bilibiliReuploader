from concurrent.futures import ThreadPoolExecutor, as_completed
from internetarchive import get_item
import json

def update_identifiers_with_sizes(input_file, output_file, max_workers=10):
    """Update identifiers with sizes and save to a new JSON file."""
    # Load identifiers from the JSON file
    with open(input_file, "r", encoding="utf-8") as f:
        idx = json.load(f)

    def process_item(index, identifier):
        """Fetch item size and return the result."""
        item = get_item(identifier)
        for obj in idx:
            if obj.get("identifier") == identifier:
                obj["size"] = item.item_size
                print(f"updated object: {obj}")
                break
        else:
            print(f"identifier {identifier} not found in json file")
        return None

    # Use ThreadPoolExecutor for concurrent processing
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        futures = {
            executor.submit(process_item, i, num["identifier"]): i
            for i, num in enumerate(idx)
        }

        for future in as_completed(futures):
            result = future.result()
            if result is not None:
                print(f"Item {result} has size less than 10000")

    with open(output_file, 'w', encoding='utf-8') as file:
        json.dump(idx, file, indent=4)

def sort_by_size():
    with open("identifierswithsizes.json" , 'r', encoding='utf-8') as file:
        items = json.load(file)
    
    def get_size(obj):
        size = obj["size"]
        return int(size)

    sorted_items_by_size = sorted(items, key = get_size)

    with open('sorted_by_size.json', 'w', encoding= 'utf-8') as f:
        json.dump(sorted_items_by_size, f , indent=4)
sort_by_size()