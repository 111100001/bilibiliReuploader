import json
import re

with open("matched.json", "r", encoding="utf-8") as f:
    data = json.load(f)

allowed_diff = 1

results = []
for match in data:
    archive_dur = float(match["duration"])
    tracker_dur = match["match"]["duration"]
    duration_match = re.search(r"\d+\.?\d*", tracker_dur)
    tracker_dur = float(duration_match.group() if duration_match else 0)

    diff = abs(tracker_dur - archive_dur)
    if diff >= allowed_diff:
        results.append(match)

with open("out.json", "w", encoding="utf-8") as out:
    json.dump(results, out,indent=2)
        