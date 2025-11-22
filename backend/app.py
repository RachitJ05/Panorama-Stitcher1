from flask import Flask, request, jsonify, send_file
from werkzeug.utils import secure_filename
import os
from stitcher import stitch_images
# from flask_cors import CORS

UPLOAD_FOLDER = 'uploads'
ALLOWED_EXT = {'png', 'jpg', 'jpeg'}

app = Flask(__name__)
# CORS(app)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXT

@app.route('/ping')
def ping():
    return jsonify({'status': 'ok'})

@app.route('/stitch', methods=['POST'])
def stitch_route():
    # Expect multiple files in field 'images'
    if 'images' not in request.files:
        return jsonify({'error': 'No images part in the request'}), 400

    files = request.files.getlist('images')
    if len(files) < 2:
        return jsonify({'error': 'Upload at least 2 images'}), 400

    saved_paths = []
    for f in files:
        if f and allowed_file(f.filename):
            fname = secure_filename(f.filename)
            path = os.path.join(app.config['UPLOAD_FOLDER'], fname)
            f.save(path)
            saved_paths.append(path)

    try:
        # stitch_images returns dict with keys: stitched, cropped, overlay, contour, mask
        result = stitch_images(saved_paths, out_dir=app.config['UPLOAD_FOLDER'])
    except Exception as e:
        return jsonify({'error': 'Stitching failed', 'message': str(e)}), 500

    return jsonify(result)

@app.route('/download')
def download_file():
    # ?path=<relative_path>
    path = request.args.get('path')
    if not path:
        return jsonify({'error': 'path missing'}), 400
    # Sanitize: prevent path traversal
    safe_path = os.path.normpath(path)
    if '..' in safe_path or safe_path.startswith('/'):
        return jsonify({'error': 'invalid path'}), 400
    full = os.path.join(app.root_path, safe_path)
    if not os.path.exists(full):
        return jsonify({'error': 'file not found'}), 404
    return send_file(full, as_attachment=True)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
