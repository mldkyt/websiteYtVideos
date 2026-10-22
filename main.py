import datetime
import os
from pprint import pprint

import requests
import yt_dlp
from dotenv import load_dotenv


def main():
    print("Hello from websiteytvideos!")

    load_dotenv()

    YT_CHANNEL = os.getenv("YT_CHANNEL") or "https://youtube.com/@mldkyt"

    WEBSITE_URL = os.getenv("WEBSITE_URL") or "https://mldkyt.com"
    WEBSITE_TOKEN = os.getenv("WEBSITE_TOKEN")

    if not WEBSITE_TOKEN:
        raise ValueError("Missing env: WEBSITE_TOKEN")

    # Get the list of videos using yt-dlp

    with yt_dlp.YoutubeDL(
        {
            "extract_flat": False,
            "skip_download": True,
            "no_warnings": True,
        }
    ) as ydl:
        info = ydl.extract_info(f"{YT_CHANNEL}/videos", download=False, process=False)

        if "entries" not in info:
            print("mreow")
            return

        for i in info["entries"]:
            if not i:
                continue

            existing = requests.get(f"{WEBSITE_URL}/api/videos",
                                    headers={"Authorization": f"Bearer {WEBSITE_TOKEN}"},
                                    params={"video_id": i["id"]})

            if existing.ok:
                continue

            more_info = ydl.extract_info(i["url"], download=False)

            title = more_info["title"]
            thumbnail = more_info["thumbnail"]
            length = more_info["duration"]
            created_at = more_info["upload_date"]
            created_at = datetime.datetime.strptime(created_at, "%Y%m%d")

            requests.post(f"{WEBSITE_URL}/api/videos",
                          headers={"Authorization": f"Bearer {WEBSITE_TOKEN}"},
                          json={
                              "id": more_info["id"],
                              "title": title,
                              "thumbnailUrl": thumbnail,
                              "length": length,
                              "createdAt": created_at.isoformat(),
                          }).raise_for_status()

if __name__ == "__main__":
    main()
