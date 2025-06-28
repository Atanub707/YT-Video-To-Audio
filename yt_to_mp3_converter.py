import yt_dlp
import os

def download_youtube_audio(url, output_folder="."):
    try:
        print("Downloading and converting to MP3...")
        ydl_opts = {
            'format': 'bestaudio/best',
            'outtmpl': os.path.join(output_folder, '%(title)s.%(ext)s'),
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }],
            'quiet': False,
        }
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
        print("✅ MP3 download complete.")
    except Exception as e:
        print("❌ Error:", e)

if __name__ == "__main__":
    video_url = input("🔗 Enter YouTube Video URL: ")
    output_dir = input("📁 Enter output directory (or leave empty for current folder): ").strip() or "."
    download_youtube_audio(video_url, output_dir)
