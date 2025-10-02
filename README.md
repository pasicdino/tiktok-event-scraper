# TikTok Scraper

This project scrapes TikTok videos either:
- from a specific user account (`user_scraper.py`)
- or by hashtag (`hashtag_scraper.py`)

It is designed for collecting TikTok content related to specific events (e.g., elections) and stores the results in CSV format.

---

## Requirements

- Python 3.8+
- Chromium browser installed
- A valid TikTok `ms_token` (session token from your browser)

Install dependencies:

```bash
pip install TikTokApi pandas
```

---

## TikTokApi Credits

This project uses [TikTokApi](https://github.com/davidteather/TikTok-Api) by [David Teather](https://github.com/davidteather).  
All scraping functionality is provided by that library.

---

## Usage

### 1. Scrape videos from a TikTok user

**Edit `user_scraper.py`:**
- Set `username` to the TikTok account you want to scrape.
- Set `ms_token` to your TikTok session token.
- Set `csv_filename` to the desired output file path.

**Run:**

```bash
python user_scraper.py
```

This will:
- Scrape all available videos from the user
- Skip duplicates if the CSV already exists
- Save the data to CSV

---

### 2. Scrape videos from hashtags

**Step 1 – Create a `.pkl` file with hashtags (or any other format which will allow you to convert it back into a list):**

```python
import pickle
hashtags = ["election2025", "vote", "debate"]
with open("hashtags.pkl", "wb") as f:
    pickle.dump(hashtags, f)
```

**Step 2 – Edit `hashtag_scraper.py`:**
- Set the path to the `.pkl` file
- Set `ms_token`
- Set `csv_filename` to the output file

**Run:**

```bash
python hashtag_scraper.py
```

This will:
- Iterate over the hashtags
- Scrape videos per hashtag
- Save all data into one CSV file

---

## Output Format

The resulting CSV file(s) will include the following columns:

| Column         | Description                        |
|----------------|------------------------------------|
| `id`           | Video ID                           |
| `create_time`  | Unix timestamp of video upload     |
| `desc`         | Video description (caption)        |
| `duration`     | Duration of the video (seconds)    |
| `play_count`   | View count                         |
| `like_count`   | Number of likes                    |
| `comment_count`| Number of comments                 |
| `share_count`  | Number of shares                   |
| `video_url`    | Direct video URL                   |
| `author`       | TikTok username                    |
| `music`        | Music title                        |
| `music_url`    | URL to the audio track             |
| `hashtag`      | (Only in hashtag scraper)          |

---

## Notes

- TikTok may limit how many videos you can scrape (usually around 500–1000 per user/hashtag).
- Scraping too quickly or without valid tokens may result in blocks.
- Always comply with TikTok’s [Terms of Service](https://www.tiktok.com/legal/page/row/terms-of-service/en).
- The original link can be constructed by taking www.tiktok/@{author}/video/{id} and can be downloaded using [`yt-dlp`](https://github.com/yt-dlp/yt-dlp)

---

## License

For educational and research use only. No warranty provided.
