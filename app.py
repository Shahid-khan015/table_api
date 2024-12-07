from flask import Flask, jsonify , Response ,send_from_directory
import os
from flask_cors import CORS

app = Flask(__name__)

CORS(app)

application = app

num_folder = r"website\DataSet\Output"
numbers_links = {}
for nl in os.listdir(num_folder):
    numbers_links[nl] = os.path.join(num_folder , nl)

video_links = {}

@app.route("/")
def tab_api():
    video_extensions = ('.mp4', '.avi', '.mov', '.mkv')

    for dir in numbers_links:
        video_links[dir] = { 'video_links' : list(os.path.join(numbers_links[dir],f) for f in os.listdir(numbers_links[dir]) if f.endswith(video_extensions)) }

    return jsonify(video_links)

@app.route("/<path:filename>")
def serve_video(filename):
    try:
        def generate(video_path):

            with open(video_path, 'rb') as f:
              while True:
                chunk = f.read(1024 * 1024)
                if not chunk:
                    break
                yield chunk

        return Response(generate(filename) , mimetype="video/mp4")
        
    except Exception as f:
       return (f"An error occurred: {f}")


    




if __name__ == '__main__':
    app.run(debug=True)
