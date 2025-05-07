import os
import json
from concurrent.futures import ThreadPoolExecutor, as_completed
from internetarchive import get_item, search_items

def fetch_metadata(identifier):
    """Fetch metadata for a single identifier."""
    try:
        item = get_item(identifier)
        return item.item_metadata['metadata']
    except Exception as e:
        print(f"Failed to fetch metadata for {identifier}: {e}")
        return None

def get_uploaded_items():
    # Fetch the list of identifiers
    lst = list(search_items(query="uploader:(fqf1fqf@gmail.com) AND identifier:Bilibili-*"))
    print("Done getting identifiers.")

    # Save the identifiers to a file
    with open('identifiers.json', 'w', encoding='utf-8') as f:
        json.dump(lst, f, indent=4)

    # Load the identifiers from the file
    with open('identifiers.json', 'r', encoding='utf-8') as f:
        identifiers = json.load(f)

    meta = []

    # Use ThreadPoolExecutor to fetch metadata in parallel
    with ThreadPoolExecutor(max_workers=10) as executor:  # Adjust max_workers as needed
        futures = {executor.submit(fetch_metadata, identifier['identifier']): identifier for identifier in identifiers}

        for future in as_completed(futures):
            result = future.result()
            if result:
                meta.append(result)
                print(f"Fetched metadata for {len(meta)} / {len(identifiers)}")

    # Save the metadata to a file
    with open('items.json', 'w', encoding='utf-8') as t:
        json.dump(meta, t, indent=4)

    print("Done getting items metadata.")
    return os.path.abspath('items.json')

get_uploaded_items()