from flask import Flask, request, jsonify
from flask_cors import CORS
import yt_dlp

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

@app.route("/", methods=["GET"])
def hello_world():
    return "Hello, World!"

@app.route("/download", methods=["POST"])
def download_videos():
    data = request.json
    video_links = data.get("video_links")

    if not video_links or not isinstance(video_links, list):
        return jsonify({"error": "Please provide a list of video links"}), 400

    ydl_opts = {
        "format": "best",  # Stream the best available quality
        "noplaylist": True,
    }

    results = []

    try:
        for video_url in video_links:
            try:
                with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                    info = ydl.extract_info(video_url, download=False)
                    title = info.get("title", "Unknown Title")
                    direct_url = info["url"]
                    results.append({"url": video_url, "title": title, "download_url": direct_url})
            except Exception as e:
                results.append({"url": video_url, "error": str(e)})

        return jsonify({"results": results}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)
