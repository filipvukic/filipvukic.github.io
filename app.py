import random
from flask import Flask, render_template, request, Response, stream_with_context, jsonify
from instagrapi import Client
import requests

app = Flask(__name__)

cl = Client()
# You need to login with your Instagram account
# Make sure to use environment variables or another secure way to handle credentials
cl.login('plushy.se', 'Plushy1')

@app.route("/", methods=['GET', 'POST'])
def index():
    message = None
    video_url = None
    original_caption = None
    button = None
    caption_choices = None
    
    if request.method == 'POST':
        try:
            print("Form data received")
            url = request.form.get('url')
            button = request.form.get('button')
            shortcode = url.split("/")[-2]
            media_id = shortcode_to_media_id(shortcode)
            media_info = cl.media_info(media_id)
            username = media_info.user.username
            
            if media_info.media_type == 2:  # Check if it's a video
                video_url = media_info.video_url
            original_caption = media_info.caption_text
            
            message = create_message(username, button)
            
            # Get 5 random captions based on the button pressed
            caption_choices = get_random_captions(button)
        except Exception as e:
            # Send back the error message to client
            return jsonify({'error': str(e)}), 500
    
    return render_template("index.html", message=message, video_url=video_url, account_name=button, original_caption=original_caption, caption_choices=caption_choices)

def shortcode_to_media_id(shortcode):
    return cl.media_pk_from_code(shortcode)

def get_random_captions(button):
    try:
        filename = f"{button}_captions.txt"
        with open(filename, "r", encoding='utf-8') as file:  # Specify encoding here
            print(f"Reading captions from {filename}")
            captions = file.readlines()
            captions = list(set([caption.strip() for caption in captions]))
            selected_captions = random.sample(captions, min(len(captions), 5))
        print(f"Selected captions: {selected_captions}")
        return selected_captions
    except FileNotFoundError:
        print(f"File not found: {filename}")
        return []
    except UnicodeDecodeError as e:
        print(f"Unicode decode error: {e}")
        return []

@app.route("/download")
def download():
    video_url = request.args.get('video_url')
    response = requests.get(video_url, stream=True)
        
    print("Downloading video from: ", video_url)

    def generate():
        for chunk in response.iter_content(chunk_size=8192):
            yield chunk

    return Response(stream_with_context(generate()), content_type='video/mp4')

@app.route("/generate_captions", methods=['POST'])
def generate_captions():
    button = request.form.get('button')
    print(f"Button: {button}")
    if not button:
        return jsonify({'error': 'Button value not provided'}), 400

    captions = get_random_captions(button)
    if captions:
        return jsonify({'captions': captions})
    else:
        return jsonify({'error': 'Could not generate captions'}), 500
    
@app.route("/video_stream", methods=['GET'])
def video_stream():
    video_url = request.args.get('url')
    response = requests.get(video_url, stream=True)

    def generate():
        for chunk in response.iter_content(chunk_size=8192):
            yield chunk
    
    return Response(generate(), content_type='video/mp4')

def create_message(username, button):
    messages = {
        "powdervibe": f"Follow 👉 @powdervibe for the best skiing & snowboarding content! ⛷\n\n"
                      f"Credit: @{username}\n\n"
                      f"#powdervibe #powderskiing #powday #skiingday #winterwonderland",
                      
        "thesnowboarding": f"Follow 👉 @thesnowboarding for the best snowboarding content! ⛷\n\n"
                           f"Credit: @{username}\n\n"
                           f"#thesnowboarding #snowboarding #snowseason #winterwonderland #powderday",
                           
        "for.skiing": f"Follow 👉 @for.skiing for the best skiing content! ⛷\n\n"
                      f"Credit: @{username}\n\n"
                      f"#forskiing #skiing #snowboarding #skiseason #winterwonderland",

        "skiingviral":  f"Tag someone that needs to see this 👊\n\n"
                        f"Follow 👉 @skiingviral for your ultimate skiing and snowboarding content 🦍\n\n"
                        f"Credit: @{username}\n"
                        f"#skiingviral\n\n"
                        f"#skiing #powder #winterseason #snowboardlife #skiinglife #freeride #snowboardingday #snowboardingseason #snowboardingmadness #offpiste #forskiing #snowboarding #skiseason #skiingseason #winterwonderland #snow #pow #powpow #snowboard #freestyle"
    }
    return messages.get(button, "Unknown button")

if __name__ == "__main__":
    app.run(debug=True)