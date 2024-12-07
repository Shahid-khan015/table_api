from flask import Flask, Response , jsonify
from flask_cors import CORS
import os
from pathlib import Path

app = Flask(__name__)
CORS(app)

# Configure static folder for videos
app.config['STATIC_FOLDER'] = os.path.join(os.getcwd(), 'static')

@app.route("/api/health")
def health_check():
    """Health check endpoint"""
    return jsonify({"status": "healthy"})

@app.route("/api/videos")
def get_videos():
    """Get list of available videos"""
    try:
        static_dir = Path(app.config['STATIC_FOLDER'])
        if not static_dir.exists():
            return jsonify({"error": "Static directory not found"}), 404

        video_links = {}
        video_extensions = ('.mp4', '.avi', '.mov', '.mkv')

        # Scan only the static directory
        for item in static_dir.iterdir():
            if item.is_dir():
                videos = [
                    f"/api/stream/{item.name}/{video.name}"
                    for video in item.iterdir()
                    if video.suffix.lower() in video_extensions
                ]
                if videos:
                    video_links[item.name] = {"video_links": videos}

        return jsonify(video_links)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/api/stream/<folder>/<filename>")
def stream_video(folder, filename):
    """Stream video files"""
    try:
        return send_from_directory(
            os.path.join(app.config['STATIC_FOLDER'], folder),
            filename,
            mimetype='video/mp4'
        )
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Error handlers
@app.errorhandler(404)
def not_found_error(error):
    return jsonify({"error": "Resource not found"}), 404

@app.errorhandler(500)
def internal_error(error):
    return jsonify({"error": "Internal server error"}), 500



if __name__ == '__main__':
    app.run()
