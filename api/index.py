from flask import Flask, render_template, request, jsonify, send_file
import yt_dlp
import os
import uuid
from werkzeug.utils import secure_filename

app = Flask(__name__, template_folder="templates")
app.config['UPLOAD_FOLDER'] = '/tmp'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size

def download_youtube_audio(url, output_folder):
    """Download YouTube audio as MP3 using yt-dlp"""
    try:
        unique_id = str(uuid.uuid4())[:8]
        output_template = os.path.join(output_folder, f'{unique_id}_%(title)s.%(ext)s')
        ydl_opts = {
            'format': 'bestaudio/best',
            'outtmpl': output_template,
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }],
            'quiet': True,
        }
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            for file in os.listdir(output_folder):
                if file.startswith(unique_id) and file.endswith('.mp3'):
                    return os.path.join(output_folder, file)
        return None
    except Exception as e:
        raise Exception(f"Download failed: {str(e)}")

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/download', methods=['POST'])
def download():
    try:
        data = request.get_json()
        url = data.get('url')
        if not url:
            return jsonify({'error': 'URL is required'}), 400
        mp3_file = download_youtube_audio(url, app.config['UPLOAD_FOLDER'])
        if mp3_file and os.path.exists(mp3_file):
            filename = os.path.basename(mp3_file)
            return jsonify({
                'success': True,
                'filename': filename,
                'message': 'Download completed successfully!'
            })
        else:
            return jsonify({'error': 'Failed to download audio'}), 500
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/download_file/<filename>')
def download_file(filename):
    try:
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        if os.path.exists(file_path):
            return send_file(file_path, as_attachment=True)
        else:
            return jsonify({'error': 'File not found'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/cleanup', methods=['POST'])
def cleanup():
    try:
        import time
        current_time = time.time()
        deleted_count = 0
        for filename in os.listdir(app.config['UPLOAD_FOLDER']):
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            if os.path.isfile(file_path) and (current_time - os.path.getmtime(file_path)) > 3600:
                os.remove(file_path)
                deleted_count += 1
        return jsonify({'message': f'Cleaned up {deleted_count} old files'})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Do NOT include any handler or app.run block. Vercel will use 'app' as the WSGI entry point. 