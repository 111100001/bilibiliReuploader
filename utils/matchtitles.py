import json
from datetime import datetime, timedelta
import re
import math


def parse_json(file_path):
    """Load JSON data from a file."""
    with open(file_path, "r", encoding="utf-8") as f:
        return json.load(f)


def get_title(obj: dict):
    """
    fetches title from obj
    """
    return obj.get("metadata", {}).get("title", "no title found")


def get_date_from_title(obj):

    title = get_title(obj)

    extracted_date = "-1"

    pattern = r"(?P<yearandmonth>\d{4}\.\d{1,2}\.)(?P<day>\d{1,2})-?(?P<dayrange>\d{1,2})?/?(?P<otherday>\d{1,2})?(?P<othermonth>\.(?P<othernmonthnodot>\d{1,2}))?"

    match = re.search(pattern, title)

    if match:  # if there is a regex match

        if (
            match.group("day")  # if the date is like 2020.02.23
            and match.group("dayrange") is None
            and match.group("otherday") is None
            and match.group("othermonth") is None
            and match.group("othernmonthnodot") is None
        ):

            extracted_date = match.group(0)
            return normalize_date(extracted_date)

        elif match.group("otherday") is not None:
            # if there is a day/otherday in the date

            day_match = re.search(r"p\d\d\s(\d\d?.?(/?\d?\d?))\s{0,1}?", title)
            day = ""
            if day_match is not None:

                if day_match.group(
                    2
                ):  # if group 2 doesnt exist, it returns an empty str appearntly
                    day = day_match.group(2)
                else:
                    day = day_match.group(1)

            extracted_date = f"{match.group('yearandmonth')}{day}"

            return normalize_date(extracted_date)

        elif match.group("dayrange"):
            title = obj.get("metadata", {}).get("title")

            p = re.findall(r"(p\d\d)\s(\d\d?.?(/?\d?\d?))(?=\s|$|\")", title)

            # get_p_num = [re.search(r"\d+", i[0]).group(0) for i in p]
            # min_p = min(get_p_num)
            # print(p)
            # print(get_p_num)
            # print(min_p)

            def extract_p_num(x):
                match = re.search(r"p(\d+)", x[0])
                return int(match.group(1)) if match else float("inf")

            min_tuple = min(p, key=extract_p_num)
            day = min_tuple[1]

            extracted_date = f"{match.group("yearandmonth")}{day}"

            return normalize_date(extracted_date)


def normalize_date(date_str):
    """Convert a date string to a datetime object."""
    for fmt in ["%d/%b/%Y", "%Y-%m-%d", "%Y.%m.%d"]:
        try:
            return datetime.strptime(date_str, fmt)
        except ValueError:
            continue
    return None  # Return None if no format matches


def find_closest_match(date, dates_list):
    """Find the closest date in dates_list to the given date."""
    closest_date = None
    smallest_diff = timedelta.max  # Initialize with a large difference

    for other_date in dates_list:
        if date == other_date:
            closest_date = other_date
            break
        # diff = abs(date - other_date)
        # if diff < smallest_diff:
        #     smallest_diff = diff
        #     closest_date = other_date

    return closest_date


def match_objects_by_date(file1, file2):
    """Match objects from two JSON files based on closest dates."""
    data1 = parse_json(file1)
    data2 = parse_json(file2)

    # Extract and normalize dates from both files
    # normalize_date(obj.get("metadata","").get("date", ""))
    dates1 = [(obj, get_date_from_title(obj)) for obj in data1]
    dates2 = [(obj, normalize_date(obj.get("date", "").split()[0])) for obj in data2]

    # Filter out objects with invalid dates
    dates1 = [(obj, date) for obj, date in dates1 if date and date.year == 2020]
    dates2 = [(obj, date) for obj, date in dates2 if date]

    # Extract just the dates from the second file for comparison
    dates2_only = [date for _, date in dates2]
    matched_pairs = []

    # Find the closest match for each date in the first file
    for obj1, date1 in dates1:
        closest_date = find_closest_match(date1, dates2_only)
        if closest_date:
            # Find the corresponding object in data2
            obj2 = next(obj for obj, date in dates2 if date == closest_date)
            matched_pairs.append((obj1, obj2))

    return matched_pairs

def match_by_duration(obj):
    file = "/home/ubuntu/bilibiliReuploader/scraper/tracker2020.json"
    data = parse_json(file)

    tt_durations = [(item, item.get("duration")) for item in data]
   



    

# Example usage
file1 = "/home/ubuntu/bilibiliReuploader/itemmetaa.json"
file2 = "/home/ubuntu/bilibiliReuploader/scraper/tracker2020.json"

matched = match_objects_by_date(file1, file2)

matched_compact = [{"identifier": obj1.get("metadata").get("identifier"), "title" : obj1.get("metadata").get("title"), "duration" : round(float(obj1.get("files")[0].get("length"))/60/60, 1) ,"originalurl": obj1.get("metadata").get("originalurl"), "match" : obj2} for obj1, obj2 in matched]

with open("matched.json", "w", encoding="utf-8") as f:
    json.dump(matched_compact, f, indent=4)
count = 0

for obj1, obj2 in matched:
    print(
        f"Matched:\nFile1: {obj1.get("metadata","").get("title","")} {obj1.get("metadata","").get("identifier","")} {round((float(obj1.get("files")[0].get("length"))/60/60), 1)} \nFile2: {obj2}\n"
    )
    count += 1
print(count)
