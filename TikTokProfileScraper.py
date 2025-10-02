from TikTokApi import TikTokApi
import asyncio
import os
import pandas as pd


ms_token = ''
username = ""  
csv_filename = f"data/tiktok/{username}_videos.csv"  #File where data is to be stored

async def user_videos():
    #Load existing data if the CSV exists, this is because not everything might be scraped the first time, this way you can rerun without duplicates
    if os.path.exists(csv_filename):
        df_existing = pd.read_csv(csv_filename, dtype=str)  
        saved_video_ids = set(df_existing["id"]) 
    else:
        df_existing = pd.DataFrame()
        saved_video_ids = set()  #No saved videos yet

    async with TikTokApi() as api:
        await api.create_sessions(ms_tokens=[ms_token], num_sessions=1, sleep_after=3, browser="chromium", headless=False)

        user = api.user(username)
        all_videos = []

        #Might need to change count, but in my experience, I rarely got over 500 regardless
        async for video in user.videos(count=9999):  
            video_info = video.as_dict
            video_id = video_info.get("id")

            if not video_id:
                continue  #Skip if no ID is found

            all_videos.append({
                "id": video_id,
                "create_time": video_info.get("createTime"),
                "desc": video_info.get("desc"),
                "duration": video_info.get("video", {}).get("duration"),
                "play_count": video_info.get("stats", {}).get("playCount"),
                "like_count": video_info.get("stats", {}).get("diggCount"),
                "comment_count": video_info.get("stats", {}).get("commentCount"),
                "share_count": video_info.get("stats", {}).get("shareCount"),
                "video_url": video_info.get("video", {}).get("playAddr"),
                "author": video_info.get("author", {}).get("uniqueId"),
                "music": video_info.get("music", {}).get("title"),
                "music_url": video_info.get("music", {}).get("playUrl"),
            })

    
        #Filter out already saved videos
        new_video_data = [video for video in all_videos if video["id"] not in saved_video_ids]

        #Save new videos to CSV
        if new_video_data:
            df_new = pd.DataFrame(new_video_data)
            df_combined = pd.concat([df_existing, df_new], ignore_index=True)  #Append to existing file
            df_combined.to_csv(csv_filename, index=False, encoding="utf-8")
            print(f"Added {len(new_video_data)} new videos to {csv_filename}")
        else:
            print("No new videos found.")

if __name__ == "__main__":
    asyncio.run(user_videos())
