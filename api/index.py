from flask import Flask, request, redirect, jsonify, render_template_string
import yt_dlp

app = Flask(__name__)

# HTML com CSS embutido para um visual "Dark" e moderno
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="pt-br">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>YouTube Downloader</title>
    <style>
        body { font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; background-color: #121212; color: white; display: flex; justify-content: center; align-items: center; height: 100vh; margin: 0; }
        .container { background-color: #1e1e1e; padding: 30px; border-radius: 15px; box-shadow: 0 10px 30px rgba(0,0,0,0.5); text-align: center; width: 90%; max-width: 450px; }
        h2 { color: #ff0000; margin-bottom: 20px; }
        input { width: 100%; padding: 12px; margin-bottom: 20px; border: none; border-radius: 5px; background: #333; color: white; box-sizing: border-box; }
        button { width: 100%; padding: 12px; border: none; border-radius: 5px; background-color: #ff0000; color: white; font-weight: bold; cursor: pointer; transition: 0.3s; }
        button:hover { background-color: #cc0000; }
        .footer { margin-top: 20px; font-size: 12px; color: #777; }
    </style>
</head>
<body>
    <div class="container">
        <h2>YouTube Downloader</h2>
        <p>Cole o link do vídeo abaixo:</p>
        <form action="/download" method="get">
            <input type="text" name="url" placeholder="https://youtube.com/watch?v=..." required>
            <button type="submit">GERAR DOWNLOAD</button>
        </form>
        <div class="footer">Hospedado na Vercel via GitHub</div>
    </div>
</body>
</html>
"""

@app.route('/')
def home():
    return render_template_string(HTML_TEMPLATE)

@app.route('/download')
def download():
    video_url = request.args.get('url')
    if not video_url:
        return redirect('/')

    ydl_opts = {
        'format': 'best',
        'quiet': True,
        'user_agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(video_url, download=False)
            return redirect(info['url'])
    except Exception as e:
        return f"Erro ao processar: {str(e)}", 500
    
