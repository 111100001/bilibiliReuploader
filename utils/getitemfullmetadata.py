import os
from internetarchive import get_item, search_items
import json
import re


def get_metadata():
    lst = list(
        search_items(query="uploader:(fqf1fqf@gmail.com) AND identifier:Bilibili-*")
    )
    print("done getting identifiers")

    with open("identifiers.json", "w", encoding="utf-8") as f:
        json.dump(lst, f, indent=4)

    if os.path.exists("itemmeta.json"):
        with open("itemmetaa-backup.json", "r", encoding="utf-8") as ids_file:
            ids_list = json.load(ids_file)
    else:
        ids_list = []

    existing_ids_pure_values = {item["metadata"]["identifier"] for item in ids_list}
    metadata = []

    counter = 0

    for idx, id in enumerate(lst, 1):
        if id["identifier"] not in existing_ids_pure_values:
            counter+=1
            print(f"getting {counter} / {len(lst)}")
            try:
                item = get_item(id["identifier"])
                files = item.item_metadata.get("files", [])
                item.item_metadata["files"] = [ # type: ignore
                    file
                    for file in files
                    if not re.search(r"\.thumbs", file.get("name", ""))
                ]
               
                metadata.append(item.item_metadata)
            except Exception as e:
                print(f"Error processing {id['identifier']}: {e}")

    combined_meta = ids_list + metadata

    with open("itemmeta.json", "w", encoding="utf-8") as f:
        json.dump(combined_meta, f, indent=4)


def get_files_names():
    with open("itemmeta.json", 'r', encoding='utf-8') as f:
        items_metadata = json.load(f)
    
    names_list = []
    items_with_no_videos = []

    for obj in items_metadata:
        array_of_files_obj = obj.get("files", [])
        if any(re.search(r"(?<!\.ia)\.mp4$", file_obj.get("name", "").strip()) for file_obj in array_of_files_obj):
            for file_obj in array_of_files_obj:
                if re.search(r"(?<!\.ia)\.mp4$", file_obj.get("name", "").strip()):
                    
                    names_list.append(file_obj["name"])
                    break
        else:
            names_list.append(f"item {obj['metadata']['identifier']} does not have a video")
            items_with_no_videos.append(obj['metadata']['identifier'])
    print(len(names_list))
    
    with open("filenames.txt", 'w', encoding='utf-8') as f:
        for name in names_list:
            f.write(name + '\n')
    with open("items_to_reupload.txt", 'w', encoding='utf-8') as fi:
            fi.write(str(items_with_no_videos))

get_metadata()
        
