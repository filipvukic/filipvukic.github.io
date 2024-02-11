import instaloader
import os
from moviepy.editor import VideoFileClip

# Create an instance of Instaloader
L = instaloader.Instaloader()

# Disable unnecessary downloads
L.save_metadata = False
L.download_pictures = False
L.download_video_thumbnails = False
L.download_geotags = False
L.download_comments = False

# Attempt to load session from file.
try:
    L.load_session_from_file('plushy.se')
except FileNotFoundError:
    # If session file does not exist, login and create one.
    L.login('plushy.se', 'Plushy1')
    L.save_session_to_file()


def preprocess_video(input_path):
    """
    Preprocess the video to reduce frame rate and resolution using MoviePy.
    """
    output_path = input_path  # Overwrite the original video
    try:
        clip = VideoFileClip(input_path)
        # Reduce frame rate to 5fps and resize to 640x360
        processed_clip = clip.resize(newsize=(640, 360)).set_fps(5)
        processed_clip.write_videofile(output_path, codec='libx264', audio_codec='aac', temp_audiofile='temp-audio.m4a', remove_temp=True)
        print(f"Video processed and saved to {output_path}")
    except Exception as e:
        print(f"Failed to preprocess video {input_path}: {e}")

def get_unique_captions_and_download_videos(username):
    i = 0
    captions = set()  # Use a set to store unique captions
    profile = instaloader.Profile.from_username(L.context, username)
    for post in profile.get_posts():
        # Save caption
        first_line = post.caption.split('\n', 1)[0] if post.caption else ''
        # Download video if present
        if first_line and '@' not in first_line and '#' not in first_line:
            captions.add(first_line)
            if post.is_video:
                new_path = i
                L.download_post(post, target=new_path)
                txt_filename = f"{new_path}/{post.date_utc.strftime('%Y-%m-%d_%H-%M-%S')}_UTC.txt"
                with open(txt_filename, 'w', encoding='utf-8') as f:
                    print(f"Writing caption to {txt_filename}")
                    f.write(first_line)
                
                # Preprocess the video
                video_filename = f"{new_path}/{post.date_utc.strftime('%Y-%m-%d_%H-%M-%S')}_UTC.mp4"
                print(f"Preprocessing video {video_filename}")
                preprocess_video(video_filename)
                i += 1
    return list(captions)

def main():
    username = input("Enter the username of the profile: ")
    captions = get_unique_captions_and_download_videos(username)
    print("Captions and videos downloaded successfully!")

if __name__ == "__main__":
    main()
