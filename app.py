from flask import Flask, render_template, request, Response, stream_with_context
import instaloader
import requests

app = Flask(__name__)

L = instaloader.Instaloader()

L.save_metadata = False
L.download_pictures = False
L.download_video_thumbnails = False
L.download_geotags = False
L.download_comments = False

@app.route("/", methods=['GET', 'POST'])
def index():
    message = None
    video_url = None
    original_caption = None  # New variable for the original caption
    button = None
    
    if request.method == 'POST':
        url = request.form.get('url')
        button = request.form.get('button')
        shortcode = url.split("/")[-2]
        post = instaloader.Post.from_shortcode(L.context, shortcode)
        username = post.owner_username
        
        video_url = post.video_url
        
        # Get the original caption of the post
        original_caption = post.caption  # Adding this line to get the caption
        
        message = create_message(username, button)
    
    # Passing the original_caption to the template
    return render_template("index.html", message=message, video_url=video_url, account_name=button, original_caption=original_caption)


@app.route("/download")
def download():
    video_url = request.args.get('video_url')
    response = requests.get(video_url, stream=True)

    def generate():
        for chunk in response.iter_content(chunk_size=8192):
            yield chunk
    
    return Response(stream_with_context(generate()), content_type='video/mp4')

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
        "powdervibe": f"Living the proper powder life 😍\n\n"
                      f"Follow 👉 @powdervibe for the best skiing & snowboarding content! ⛷\n\n"
                      f"Credit: @{username}\n\n"
                      f"#powdervibe #powderskiing #powday #skiingday #winterwonderland",
                      
        "thesnowboarding": f"The crew is vibing this winter 👊🏂\n\n"
                           f"Follow 👉 @thesnowboarding for the best snowboarding content! ⛷\n\n"
                           f"Credit: @{username}\n\n"
                           f"#thesnowboarding #snowboarding #snowseason #winterwonderland #powderday",
                           
        "for.skiing": f"Tag your skiing buddy 😎\n\n"
                      f"Follow 👉 @for.skiing for the best skiing content! ⛷\n\n"
                      f"Credit: @{username}\n\n"
                      f"#forskiing #skiing #snowboarding #skiseason #winterwonderland",

        "skiingviral":  f"Who would you share this run with? 🤩 \n\n"
                        f"Tag someone that needs to see this 👊\n\n"
                        f"Follow 👉 @skiingviral for your ultimate skiing and snowboarding content 🦍\n\n"
                        f"Credit: @{username}\n"
                        f"#skiingviral\n\n"
                        f"#skiing #powder #winterseason #snowboardlife #skiinglife #freeride #snowboardingday #snowboardingseason #snowboardingmadness #offpiste #forskiing #snowboarding #skiseason #skiingseason #winterwonderland #snow #pow #powpow #snowboard #freestyle"
    }
    return messages.get(button, "Unknown button")

if __name__ == "__main__":
    app.run(debug=True)
