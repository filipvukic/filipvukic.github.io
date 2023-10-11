import schedule
import time
from instagrapi import Client

client = Client()
client.login('plushy.se', 'Plushy1')

def upload_photo():
    media = client.photo_upload(
        "./example.jpg",
        "Test caption for photo with #hashtags and mention users such @example",
        extra_data={
            "custom_accessibility_caption": "alt text example",
            "like_and_view_counts_disabled": 1,
            "disable_comments": 1,
        }
    )
    print("Photo uploaded!")

# Schedule the photo to be uploaded at a specific time, e.g., 15:00 (3:00 PM)
schedule.every().day.at("15:22").do(upload_photo)

# Keep the script running
while True:
    schedule.run_pending()
    time.sleep(1)
