import re
import asyncio
from bilibili_api import video
import json


def getid(url):

    video_id = re.search(r"/video/([A-Za-z0-9]+)", url)
    
    return video_id.group(1)


def getpnum(url):

    part = re.search(r"\?p=(\d{1,2})", url)

    return part.group(1)


def geturls(obj: dict):
    urls = str(obj.get("originalurl", "")).split()
    # baseurl = urls[0].split("?")[0]
    # print(f"base is {baseurl}")
    return urls

def getdurations(info, part):
    duration = 0
    pages = info.get("pages", "")
    for page in pages:
        if int(page.get("page")) == int(part):
            duration = page.get("duration")
    return duration

def dumpdata(obj):
    with open("durationissues.json", "w", encoding="utf-8") as f :
        json.dump(obj,f,indent=4)




async def main():
    with open("matched.json", "r", encoding="utf-8") as f:
        data:list[dict] = json.load(f)

    info_dict = []
    count = 0

    for datum in data:
        urls = geturls(datum)
        vid_id = getid(urls[0])
        v = video.Video(bvid=vid_id)
        info = await v.get_info()
        durations = 0

        for url in urls:
            
            part = getpnum(url)
            durations += int(getdurations(info, part))

        durations_rouinded = round(float(durations) / 60 / 60, 1)
        archived_duration = float(datum.get("duration"))
        
        

        if abs(durations_rouinded - archived_duration) >= 0.5:
            info_dict.append({"item":datum, "bilibiliduration": durations_rouinded, })
            print(f"{durations_rouinded} = {archived_duration}")
            

    dumpdata(info_dict)


if __name__ == "__main__":
    asyncio.run(main())

