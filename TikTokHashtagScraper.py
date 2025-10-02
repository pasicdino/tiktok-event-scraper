from TikTokApi import TikTokApi
import asyncio
import os
import pandas as pd
import random
import pickle
print(os.getcwd())

#Load the list of hashtags
with open('EDA/saved_hashtags.pkl', 'rb') as f:
    all_hashtags = pickle.load(f)

print('Number of hashtags: ' + str(len(all_hashtags)))

csv_filename = f""  #File where you want to save the data

async def fetch_videos_for_hashtag(tag):
    ms_token = ''
    hashtag_name = tag

    async with TikTokApi() as api:
        await api.create_sessions(ms_tokens=[ms_token], num_sessions=1, sleep_after=3, browser="chromium", headless=False)

        hashtag = api.hashtag(name=hashtag_name)
        all_videos = []
        async for video in hashtag.videos(count=10000):
            video_info = video.as_dict
            video_id = video_info.get("id")
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
                "hashtag": tag
            })
        random.shuffle(all_videos)
    return all_videos



#Hashtags must be stored in 'all_hashtags'
async def main():
    all_videos_data = []
    count = 0
    for tag in all_hashtags:
        print(count)
        videos = await fetch_videos_for_hashtag(tag)
        all_videos_data.extend(videos)
        count+=1

    #Save all scraped posts
    if all_videos_data:
        df_all_videos = pd.DataFrame(all_videos_data)
        df_all_videos.to_csv(csv_filename, index=False, encoding="utf-8")
        print(f"Saved {len(all_videos_data)} videos to {csv_filename}")
    else:
        print("No videos to save.")




if __name__ == "__main__":
    asyncio.run(main())
