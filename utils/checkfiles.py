from math import e
import os
from re import search

from internetarchive import get_files, search_items, get_item, delete
import json



# print(list(search_items(query="publicdate:[2008-02-01 TO 2008-03-01] AND contributor:smithsonian")))

def get_uploaded_items():
    lst = list(search_items(query="uploader:(fqf1fqf@gmail.com) AND identifier:Bilibili-*"))
    print("done getting identifiers")


    with open('identifiers.json', 'w', encoding='utf-8') as f:
        json.dump(lst, f, indent=4)
    f.close()

    
    with open('identifiers.json', 'r', encoding='utf-8') as f:
        identifiers = json.load(f)
        meta = []
        if os.path.exists('items.json'):
            with open('items.json', 'r', encoding= 'utf-8') as existing_items_file:
                try:
                    existing_items = json.load(existing_items_file)
                except json.JSONDecodeError:
                    print("error items.json crupt")
                    existing_items = []
        else:
            existing_items = []

        existing_identifiers = {item['identifier'] for item in existing_items}
        for identifier in identifiers:
            # for f in get_files(identifier=f'{item["identifier"]}',glob_pattern='*concatenated*[!.ia].mp4'):
            #     fnames = f.__dict__
            #     fnames.pop('auth', None)
            #     fnames.pop('item', None)
            #     meta.append(fnames)
            if identifier['identifier'] not in existing_identifiers:
                item = get_item(identifier['identifier'])
                print(f"getting {len(meta)} / {len(identifiers) - len(existing_items)}")
                meta.append(item.item_metadata['metadata'])
        combined_items = existing_items + meta
        with open('items.json','w', encoding='utf-8') as t:
            json.dump(combined_items,t, indent=4)
    print("done getting items metadata")
    
    return os.path.abspath('items.json')



def process_and_sort_items(file_path):
    """
    Reads a JSON file, extracts the last number from the 'name' field of each object,
    sorts the objects by this number, and prints the sorted names.

    :param file_path: Path to the JSON file containing the items.
    """
    with open(file_path, 'r', encoding='utf-8') as f:
        items = json.load(f)

    filenames = []

    items_ids = {item['identifier'] for item in items}


    for identifier in items:
        if identifier['identifier'] not in items_ids:
            for f in get_files(identifier=f'{identifier["identifier"]}',glob_pattern='*concatenated*[!.ia].mp4'):
                    print(f"processing {len(filenames)} / {len(items)}")
                    fnames = f.__dict__
                    fnames.pop('auth', None)
                    fnames.pop('item', None)
                    filenames.append(fnames)

    def extract_last_number(obj):
        # Extract the name value
        name = obj["name"]
        # Find the last number in the file name
        # Assuming the number is before the file extension
        number = ''.join(filter(str.isdigit, name.split('.')[0].split('_')[-1]))
        return int(number)

    # Sort the objects by the extracted number
    print("sorting the dict")
    sorted_objects = sorted(filenames, key=extract_last_number)

    # Print the sorted objects
    with open('namesofvideos.txt','w', encoding='utf-8') as t:
        for obj in sorted_objects:
            t.write(obj["name"]+ '\n')
    t.close()

def del_items():
    with open('todel.json', 'r', encoding='utf-8') as f:
        items = json.load(f)
        for item in items:
            identifier = item['identifier']
            try:
                delete(identifier, secret_key='s1jgX4mlZdq48bvc', access_key='7XwnfpsJw4du4s5z', verbose=True, cascade_delete=True)
            except Exception as e:
                print(f"Failed to delete {identifier}: {e}")

#print(list(get_files(identifier='',glob_pattern='*.mp4')))

process_and_sort_items(get_uploaded_items())

