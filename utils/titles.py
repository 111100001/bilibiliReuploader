from datetime import datetime
import json
import re
import readline


def get_titles():
    """
    Fetches the titles of items from the Internet Archive.
    """
    # Search for items uploaded by a specific user
    with open("itemmetaa.json", "r", encoding="utf-8") as f:
        items = json.load(f)

    return items


def get_title(obj: dict):
    """
    fetches title from obj
    """
    return obj.get("metadata", {}).get("title", "no title found")


def parse_json(file_path):
    """Load JSON data from a file."""
    with open(file_path, "r", encoding="utf-8") as f:
        return json.load(f)


def save_json(file_path, data):
    """Save data back to JSON file."""
    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def normalize_date(date_str):
    """Convert a date string to a datetime object."""
    for fmt in ["%d/%b/%Y", "%Y-%m-%d", "%Y.%m.%d"]:
        try:
            return datetime.strptime(date_str, fmt)
        except ValueError:
            continue
    return None


def input_with_prefill(prompt, text):
    """Input function with pre-filled text."""

    def hook():
        readline.insert_text(text)
        readline.redisplay()

    readline.set_pre_input_hook(hook)
    result = input(prompt)
    readline.set_pre_input_hook()
    return result


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
    #     print(f"no match found here: {title}")


dates = [(obj, get_date_from_title(obj)) for obj in get_titles()]


my_list = [(title.get("metadata", {}).get("title"), str(date)) for title, date in dates]

# def process_titles(file_path):
#     """Process all titles and save changes."""
#     data = parse_json(file_path)

#     for obj in data:
#         result = get_date_from_title(obj)
#         if result:
#             print(f"Extracted date: {result} from: {get_title(obj)}")
#         else:
#             print(f"No date found in: {get_title(obj)}")

#     # Save all changes back to the file
#     save_json("/home/ubuntu/bilibiliReuploader/fixedrange-itemmeta.json", data)
#     print(f"File saved with all changes: {file_path}")


# # Usage
# if __name__ == "__main__":
#     file_path = "/home/ubuntu/bilibiliReuploader/itemmeta.json"
#     process_titles(file_path)


# seen = set()
# dupes = set()
# titles = []
# for title, item in my_list:
#     if item in seen:
        
#         if item != "None":
#             print(item)
#             dupes.add(item)
#             titles.append(title)

#     else:
#         seen.add(item)

# print("Duplicates:", dupes)
# print("titles", titles)

# for item in dates:
#     if item[1] is None:
#         print("---------------------")
#         print(item[0].get("metadata", {}).get("title"))
#         print("")
#         print(item[1])


# with open("dates.json",'w', encoding='utf-8') as f:
#     json.dump(dates,f, indent= 4)

# %%
