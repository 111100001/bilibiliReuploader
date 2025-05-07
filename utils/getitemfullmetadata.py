from operator import indexOf
from internetarchive import get_item, search_items
import json

def get_metadata():
    lst = list(search_items(query="uploader:(fqf1fqf@gmail.com) AND identifier:Bilibili-*"))
    print("done getting identifiers")

    with open('identifiers.json', 'w', encoding='utf-8') as f:
        json.dump(lst, f, indent=4)
    f.close()

    with open('identifiers.json', 'r', encoding='utf-8') as t:
        ids = json.load(fp=t)
    f.close()


    with open('itemmeta.json', 'r', encoding='utf-8') as ids_file:
        ids_list = json.load(ids_file)

    
    existing_ids_pure_values = {item["identifier"] for item in ids}
    
    metadata = []
    for id in lst:
        if id["identifier"] not in existing_ids_pure_values:
            print(f"getting {indexOf(lst,id)} / {len(lst)}")
            item = get_item(id["identifier"] )
            metadata.append(item.item_metadata)
    combined_meta = ids_list + metadata

    with open("itemmeta.json", 'w', encoding='utf-8') as f:
        json.dump(combined_meta,f,indent= 4) 
get_metadata()
    
    
    