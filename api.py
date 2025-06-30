from flask import Flask, request, jsonify
import yt_dlp

app = Flask(__name__)

@app.route('/api/download')
def download():
    url = request.args.get('url')
    if not url:
        return jsonify({"error": "No URL provided"}), 400

    ydl_opts = {'quiet': True, 'skip_download': True}
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)
            return jsonify({
                "title": info.get("title"),
                "thumbnail": info.get("thumbnail"),
                "formats": [
                    {
                        "quality": f.get("format_note"),
                        "url": f.get("url"),
                        "ext": f.get("ext"),
                        "filesize": f.get("filesize")
                    } for f in info.get("formats", []) if f.get("ext") == "mp4" and f.get("url")
                ]
            })
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
