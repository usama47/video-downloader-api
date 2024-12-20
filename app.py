from flask import Flask, request, jsonify
import os
import yt_dlp

app = Flask(__name__)

@app.route('/download', methods=['POST'])
def download_videos():
    data = request.json
    video_links = data.get('video_links')
    save_path = 'downloads'  # Save path on the server

    if not os.path.exists(save_path):
        os.makedirs(save_path)

    ydl_opts = {
        "outtmpl": os.path.join(save_path, "%(title)s.%(ext)s"),
        "format": "best",
        "nocheckcertificate": True,
        "force_ipv4": True,
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download(video_links)
        return jsonify({"message": "Videos downloaded successfully"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
