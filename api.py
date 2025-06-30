from flask import Flask, request, jsonify
import yt_dlp

app = Flask(__name__)

@app.route('/api/download', methods=['GET'])
def download_video():
    url = request.args.get('url')
    if not url:
        return jsonify({"error": "URL parametresi gerekli"}), 400

    cookies = {
        "SID": "g.a000xwgcmyzP-deGA3oPcb1zMxezIZ2-nA9FYUS_ocdzw_3R3nffK2XCP2xvEX_utGYCy58u9QACgYKAcwSARUSFQHGX2Mi0YeopImQPuIz6SCKHfY5eBoVAUF8yKrE9b6jko8wDsE0TwkbZO780076",
        "HSID": "A3E9g5IEdjf8ZPZZr",
        "SSID": "AngX9jIQU2k40ISSd",
        "APISID": "W6Emi28bEu0YGk-x/AKKqWcdlwhCsCxgqA",
        "SAPISID": "8Pg0qxXUJ4pIdr4w/A7rMBcm57Zv3StMBk"
        # Aşağıdaki satırlar geçici olarak çıkarıldı çünkü 502'ye neden olabiliyor
        # "LOGIN_INFO": "...",
        # "YSC": "..."
    }

    ydl_opts = {
        'quiet': True,
        'skip_download': True,
        'cookiefile': None,
        'cookies': cookies
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)
            return jsonify({
                "title": info.get("title"),
                "thumbnail": info.get("thumbnail"),
                "formats": [
                    {
                        "quality": f.get("format_note"),
                        "url": f.get("url")
                    }
                    for f in info.get("formats", []) if f.get("url")
                ]
            })
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
