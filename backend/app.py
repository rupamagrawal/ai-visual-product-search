from pathlib import Path
import traceback
from uuid import uuid4

from flask import Flask, jsonify, request
from flask_cors import CORS
from werkzeug.utils import secure_filename

from model.predict import predict_object
from utils.color import detect_color_details
from utils.search import search_products


app = Flask(__name__)
CORS(app)
UPLOAD_DIR = Path("temp_uploads")
UPLOAD_DIR.mkdir(exist_ok=True)


@app.route("/api/health", methods=["GET"])
def health_check():
    return jsonify({"status": "ok", "message": "Backend is running"})


@app.route("/api/search-by-image", methods=["POST"])
def search_by_image():
    if "image" not in request.files:
        return jsonify({"error": "Image file is required with key 'image'"}), 400

    image_file = request.files["image"]
    if image_file.filename == "":
        return jsonify({"error": "Please select an image file"}), 400

    original_name = secure_filename(image_file.filename)
    suffix = Path(original_name).suffix.lower() or ".jpg"
    temp_path = UPLOAD_DIR / f"{uuid4().hex}{suffix}"

    image_file.save(temp_path)

    try:
        object_name = predict_object(str(temp_path))
        color_details = detect_color_details(str(temp_path))
        color_name = color_details["dominant_color"]
        secondary_color = color_details["secondary_color"]
        has_stripes = color_details["has_stripes"]

        query = f"{color_name} {object_name}".strip()
        if has_stripes and secondary_color != color_name:
            query = f"{query} with {secondary_color} stripes"

        results = search_products(query)

        return jsonify(
            {
                "object": object_name,
                "color": color_name,
                "secondary_color": secondary_color,
                "has_stripes": has_stripes,
                "query": query,
                "results": results,
            }
        )
    except ValueError as exc:
        return jsonify({"error": str(exc)}), 400
    except Exception as exc:
        traceback.print_exc()
        return jsonify({"error": f"Internal server error: {exc}"}), 500
    finally:
        if temp_path.exists():
            temp_path.unlink()


if __name__ == "__main__":
    app.run(debug=True)
