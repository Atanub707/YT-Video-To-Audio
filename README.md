# YouTube to MP3 Converter Web App

A beautiful, modern web application that converts YouTube videos to MP3 audio files using Flask and yt-dlp.

## Features

- 🎵 High-quality MP3 conversion
- 🌐 Modern, responsive web interface
- ⚡ Fast and secure downloads
- 🧹 Automatic file cleanup
- 📱 Mobile-friendly design
- 🔒 Works with all YouTube videos

## Prerequisites

- Python 3.7+
- ffmpeg (for audio conversion)

## Installation

1. **Install ffmpeg:**
   ```bash
   sudo apt update
   sudo apt install ffmpeg
   ```

2. **Install Python dependencies:**
   ```bash
   pip3 install -r requirements.txt
   ```

## Usage

1. **Start the web server:**
   ```bash
   python3 app.py
   ```

2. **Open your browser and go to:**
   ```
   http://localhost:5000
   ```

3. **Paste a YouTube URL and click "Convert to MP3"**

## API Endpoints

- `GET /` - Main web interface
- `POST /download` - Convert YouTube URL to MP3
- `GET /download_file/<filename>` - Download converted MP3 file
- `POST /cleanup` - Clean up old downloaded files

## File Structure

```
├── app.py                 # Main Flask application
├── templates/
│   └── index.html        # Web interface
├── downloads/            # Downloaded MP3 files (auto-created)
├── requirements.txt      # Python dependencies
└── README.md            # This file
```

## Configuration

The app automatically:
- Creates a `downloads` folder for MP3 files
- Cleans up files older than 1 hour
- Limits file size to 16MB
- Uses unique filenames to prevent conflicts

## Deployment

For production deployment, consider:
- Using a production WSGI server (Gunicorn, uWSGI)
- Setting up a reverse proxy (Nginx)
- Configuring SSL certificates
- Setting up proper file storage

## License

This project is open source and available under the MIT License. 