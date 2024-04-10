from flask import Flask, send_file
import requests
from PIL import Image
from io import BytesIO
from moviepy.editor import *

app = Flask(__name__)

@app.route('/bw/vid/<usern>')
def generate_video(usern):
    try:
        # Load the video file
        video_path = "well.mp4"
        video_clip = VideoFileClip(video_path)

        # Fetch the image from the API
        image_url = f"http://api.astralaxis.info:35819/vod/{usern}/yearly/ALL_MODES"
        response = requests.get(image_url)

        # Check if the request was successful
        if response.status_code != 200:
            return f"Error: Unable to fetch image from API. Status code: {response.status_code}"

        # Save the fetched image
        image = Image.open(BytesIO(response.content))
        image_path = f"image{usern}overlay.png"
        image.save(image_path)

        # Resize the image to match the video's dimensions
        image = image.resize((video_clip.size[0], video_clip.size[1]))

        # Add text overlay
        text = TextClip("Made by Kushi_k", fontsize=70, color='white')
        text = text.set_position(('center', 'bottom')).set_duration(video_clip.duration)

        # Composite the image and text clips over the video
        final_clip = CompositeVideoClip([video_clip, ImageClip(image_path).set_duration(video_clip.duration).set_position(('center', 'center')), text])

        # Write the modified video to a file
        output_path = f"{usern}_this shit took to much time bro.mp4"
        final_clip.write_videofile(output_path, codec='libx264', fps=video_clip.fps)

        # Close the video clip objects
        video_clip.close()
        final_clip.close()

        # Send the modified video file as a response
        return send_file(output_path, as_attachment=True)
    except Exception as e:
        return str(e)

if __name__ == '__main__':
    app.run(debug=True)
