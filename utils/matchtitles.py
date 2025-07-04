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
    # else:
    # print(f"no date found here:{title}")


def normalize_date(date_str):
    date_str = date_str.strip()
    """Convert a date string to a datetime object."""
    for fmt in ["%d/%b/%Y", "%d/%b/%Y %H:%M", "%Y-%m-%d", "%Y.%m.%d"]:
        try:
            return datetime.strptime(date_str, fmt)
        except ValueError:
            continue

    print(f"could't parse this: {repr(date_str)}")
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
    dates1 = [(obj, date) for obj, date in dates1 if date]
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

            exact_dates = [obj for obj, date in dates2 if date == closest_date]

            archived_len = round(float(obj1.get("files")[0].get("length")) / 60 / 60, 1)
            exact_date_durations = [
                (float((re.search(r"\d+\.?\d*", i.get("duration")).group(0))), i)
                for i in exact_dates
            ]

            match = re.search(r"\d+\.?\d*", obj2.get("duration"))

            if match:
                tt_len = float(match.group())

            if len(exact_date_durations) > 1:
                smallest_diff = float("inf")
                closest_obj = None
                for i in exact_date_durations:
                    diff = abs(i[0] - archived_len)
                    if diff < smallest_diff:
                        smallest_diff = diff
                        closest_obj = i

                if closest_obj is not None:
                    matched_pairs.append(
                        (
                            obj1,
                            closest_obj[1],
                            "matched by closest duration among same date streams",
                        )
                    )
            else:
                matched_pairs.append((obj1, obj2, "matched by same date"))

    return matched_pairs


def match_objects_by_date_with_duration_window(file1, file2):
    """Match objects from two JSON files based on dates and duration within a 3-day window."""
    data1 = parse_json(file1)
    data2 = parse_json(file2)

    # Extract and normalize dates from both files
    dates1 = [(obj, get_date_from_title(obj)) for obj in data1]
    dates2 = [(obj, normalize_date(obj.get("end", "").split()[0])) for obj in data2]

    # Filter out objects with invalid dates
    dates1 = [(obj, date) for obj, date in dates1 if date]
    # dates2 = [(obj, date) for obj, date in dates2 if date] #there shouldn't be invalid dates here

    matched_pairs = []

    # Find matches for each object in file1
    for obj1, date1 in dates1:
        # Get duration from file1 object
        archived_len = round(float(obj1.get("files")[0].get("length")) / 60 / 60, 1)

        # Find objects within 3-day window (day before, same day, day after)
        window_objects = []
        for obj2, date2 in dates2:
            date_diff = abs((date1.date() - date2.date()).days)
            if date_diff <= 1:  # Within 1 day (yesterday, today, tomorrow)
                # Extract duration from obj2
                duration_match = re.search(r"\d+\.?\d*", obj2.get("duration", ""))
                if duration_match:
                    obj2_duration = float(duration_match.group())
                    window_objects.append((obj2, date2, obj2_duration))

        if not window_objects:
            continue

        # Check for exact duration match within the 3-day window
        exact_duration_match = None
        for obj2, date2, obj2_duration in window_objects:
            if obj2_duration == archived_len:  # Exact duration match
                exact_duration_match = (obj2, date2, obj2_duration)
                break

        if (
            False
        ):  # exact_duration_match: #match by the duration only if the date is not the same
            # Found exact duration match within 3-day window
            matched_pairs.append(
                (obj1, exact_duration_match[0], "exact_duration_3day_match")
            )
        else:
            # No exact duration match, fall back to original logic
            # Find objects with exact same date
            same_date_objects = [
                (obj2, obj2_duration)
                for obj2, date2, obj2_duration in window_objects
                if date2.date() == date1.date()
            ]

            if len(same_date_objects) > 1:
                # Multiple objects on same date, find closest duration
                smallest_diff = float("inf")
                closest_obj = None
                for obj2, obj2_duration in same_date_objects:
                    diff = abs(obj2_duration - archived_len)
                    if diff < smallest_diff:
                        smallest_diff = diff
                        closest_obj = obj2

                if closest_obj is not None:
                    matched_pairs.append(
                        (obj1, closest_obj, "closest_duration_same_date")
                    )
            elif same_date_objects:
                # Only one object on same date
                matched_pairs.append(
                    (obj1, same_date_objects[0][0], "only_match_same_date")
                )
            # else:
            #     # No same date objects, find closest date within window that wasnt already matched before
            #     closest_by_date = min(
            #         window_objects, key=lambda x: abs((date1.date() - x[1].date()).days)
            #     )
            #     matched_pairs.append((obj1, closest_by_date[0],"closest_date_in_window"))

    return matched_pairs


# Example usage
file1 = "/home/ubuntu/bilibiliReuploader/itemmetaa-backup.json"
file2 = "/home/ubuntu/bilibiliReuploader/scraper/tracker.json"

matched = match_objects_by_date_with_duration_window(file1, file2)

for i in matched:
    try:
        if i[3] is not None:
            print(i[3])
    except IndexError:
        continue

matched_compact = [
    {
        "identifier": obj1.get("metadata").get("identifier"),
        "title": obj1.get("metadata").get("title"),
        "duration": round(float(obj1.get("files")[0].get("length")) / 60 / 60, 1),
        "originalurl": obj1.get("metadata").get("originalurl"),
        "date": str(get_date_from_title(obj1).strftime("%d/%b/%Y")),
        "match": obj2,
        "match type": matchtype,
    }
    for obj1, obj2, matchtype in matched
]

sorteddict = sorted(
    matched_compact, key=lambda x: datetime.strptime(x["date"], "%d/%b/%Y")
)

with open("matched.json", "w", encoding="utf-8") as f:
    json.dump(sorteddict, f, indent=4)
count = 0

# for obj1, obj2 in matched:
#     print(
#         f"Matched:\nFile1: {obj1.get("metadata","").get("title","")} {obj1.get("metadata","").get("identifier","")} {round((float(obj1.get("files")[0].get("length"))/60/60), 1)} \nFile2: {obj2}\n"
#     )
#     count += 1
# print(count)
