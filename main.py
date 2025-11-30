import os
from datetime import datetime

import requests
import yt_dlp
from dotenv import load_dotenv


def main():
    print("Hello from websiteytvideos!")

    load_dotenv()

    YT_CHANNEL = os.getenv("YT_CHANNEL") or "https://youtube.com/@lunyauwu"

    WEBSITE_URL = os.getenv("WEBSITE_URL") or "https://lunya.pet"
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

        videos = []

        for i in info["entries"]:
            if not i:
                continue

            more_info = ydl.extract_info(i["url"], download=False)
            videos.append(
                {
                    "id": more_info["id"],
                    "link": more_info.get("url")
                    or f"https://youtube.com/watch?v={more_info.get('id')}",
                    "title": more_info.get("title"),
                    "createdAt": datetime.fromtimestamp(
                        int(more_info.get("timestamp") or 0)
                    ).isoformat(timespec="seconds", sep="T")
                    + "Z",
                }
            )

            if len(videos) >= 5:
                break

        result = requests.post(
            f"{WEBSITE_URL}/api/youtubevideos",
            headers={"Authorization": f"Bearer {WEBSITE_TOKEN}"},
            json=videos,
        )

        if not result.ok:
            print("Error: ", result.text)


if __name__ == "__main__":
    main()
