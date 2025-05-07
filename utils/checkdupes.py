import json
from collections import Counter

# Load the JSON file
with open("../items.json", "r", encoding="utf-8") as file:
    data = json.load(file)

# Extract all identifiers
identifiers = [item["originalurl"] for item in data]

# Count occurrences of each identifier
identifier_counts = Counter(identifiers)

# Find duplicates (identifiers with a count greater than 1)
duplicates = {key: count for key, count in identifier_counts.items() if count > 1}

sum_count = 0
# Print the duplicates
if duplicates:
    print("Duplicate identifiers found:")
    for identifier, count in duplicates.items():
        print(f"{identifier}: {count} times")
        sum_count += count
    print("\n")
    print(sum_count)
else:
    print("No duplicate identifiers found.")