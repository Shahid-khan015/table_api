from flask import Blueprint, jsonify, send_from_directory, current_app
from pathlib import Path
import os
from utils.security import validate_path

video_bp = Blueprint('video', __name__)

@video_bp.route('/videos')
def get_videos():
    """Get list of available videos"""
    try:
        static_dir = Path(current_app.config['STATIC_FOLDER'])
        if not static_dir.exists():
            return jsonify({"error": "Static directory not found"}), 404

        video_links = {}
        
        # Scan only the static directory
        for item in static_dir.iterdir():
            if item.is_dir():
                videos = [
                    f"/api/stream/{item.name}/{video.name}"
                    for video in item.iterdir()
                    if video.suffix.lower() in current_app.config['ALLOWED_EXTENSIONS']
                ]
                if videos:
                    video_links[item.name] = {"video_links": videos}

        return jsonify(video_links)
    except Exception as e:
        current_app.logger.error(f"Error in get_videos: {str(e)}")
        return jsonify({"error": "Internal server error"}), 500

@video_bp.route('/stream/<folder>/<filename>')
def stream_video(folder, filename):
    """Stream video files"""
    try:
        # Validate path to prevent directory traversal
        if not validate_path(folder) or not validate_path(filename):
            return jsonify({"error": "Invalid path"}), 400
            
        file_path = os.path.join(current_app.config['STATIC_FOLDER'], folder)
        return send_from_directory(
            file_path,
            filename,
            mimetype='video/mp4'
        )
    except Exception as e:
        current_app.logger.error(f"Error in stream_video: {str(e)}")
        return jsonify({"error": "Internal server error"}), 500