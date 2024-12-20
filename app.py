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
    video_links = data.get("video_links", [])
    results = []

    for url in video_links:
        try:
            ydl_opts = {
                "outtmpl": "%(title)s.%(ext)s",
                "format": "best",
                "quiet": True,
            }
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info_dict = ydl.extract_info(url, download=False)
                results.append({
                    "title": info_dict.get("title"),
                    "download_url": ydl.prepare_filename(info_dict),
                })
        except Exception as e:
            results.append({
                "url": url,
                "error": str(e),
            })

    return jsonify({"results": results}), 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)
