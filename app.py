from flask import Flask, render_template, request, jsonify
from downloader import download_video
import os

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/get_thumbnail', methods=['POST'])
def get_thumbnail():
    video_url = request.json.get('url')
    video_id = video_url.split("v=")[-1]
    thumbnail_url = f'https://img.youtube.com/vi/{video_id}/0.jpg'
    return jsonify({'thumbnail_url': thumbnail_url})

@app.route('/download_video', methods=['POST'])
def download():
    video_url = request.json.get('url')
    download_status = download_video(video_url)

    def stream_status():
        while download_status.status['percentage'] != '100%':
            yield f"data: {jsonify(download_status.status)}\n\n"

    return app.response_class(stream_status(), mimetype='text/event-stream')

if __name__ == '__main__':
    if not os.path.exists('downloads'):
        os.makedirs('downloads')  # Ensure downloads directory exists
    app.run(debug=True)
