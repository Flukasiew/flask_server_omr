from app import app
from app.processing import preprocess_image, lily_postprocess, generate_audio
from app.model_handler import ModelHandler
from flask import (
    request,
    render_template,
    jsonify,
    send_from_directory,
    url_for,
    redirect,
)
from PIL import UnidentifiedImageError, Image
import numpy as np


model_handler = ModelHandler()

@app.route("/predict_uri", methods=["POST"])
def predict_uri():

    try:
        img = request.files["image"]
    except:
        return "No image supplied in request", 400
    try:
        img = np.asarray(Image.open(img.stream))
    except UnidentifiedImageError:
        return "Could not read the supplied file", 400
    try:
        img = preprocess_image(img, model_handler.HEIGHT)
    except ValueError as exception:
        return str(exception), 500

    settings = request.form.to_dict()
    try:
        predicted_lily = model_handler.predict(img)
    except:
        return "Internal Model error", 500

    try:
        clef = int(settings.get("clef", 1))
        key = int(settings.get("key", 0))
        tempo = int(settings.get("tempo", 1))
    except ValueError:
        return "Wrong settings format they should be convertible to int", 500

    try:
        processed_lily = lily_postprocess(predicted_lily, clef, key, tempo)
    except:
        return "Processing error", 500

    path = generate_audio(processed_lily)

    return jsonify(url_for("static", filename=path.split(r"/")[-1]))


@app.route("/ping", methods=["GET"])
def ping():
    return "sucess"


