import json

def process_and_sort_items(file_path):
    """
    Reads a JSON file, extracts the last number from the 'name' field of each object,
    sorts the objects by this number, and prints the sorted names.

    :param file_path: Path to the JSON file containing the items.
    """
    with open(file_path, 'r', encoding='utf-8') as f:
        items = json.load(f)

    def extract_last_number(obj):
        # Extract the name value
        name = obj["name"]
        # Find the last number in the file name
        # Assuming the number is before the file extension
        number = ''.join(filter(str.isdigit, name.split('.')[0].split('_')[-1]))
        return int(number)

    # Sort the objects by the extracted number
    sorted_objects = sorted(items, key=extract_last_number)

    # Print the sorted objects
    for obj in sorted_objects:
        print(obj["name"])

# Example usage
# process_and_sort_items('items.json')