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


@app.route("/")
def index():

    """
    This route will render a template.
    If a query string comes into the URL, it will return a parsed
    dictionary of the query string keys & values, using request.args
    """

    args = None
    if request.args:

        args = request.args

        return render_template("public/index.html", args=args)

    return render_template("public/index.html", args=args)


@app.route("/predict_file", methods=["POST"])
def predict_file():

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

    processed_lily = lily_postprocess(
        predicted_lily,
        int(settings.get("clef", 1)),
        int(settings.get("key", 0)),
        int(settings.get("tempo", 1)),
    )

    path = generate_audio(processed_lily)
    return send_from_directory(
        "static", path.split("/")[-1], mimetype="audio/mpeg", as_attachment=True
    )


@app.route("/predict_uri", methods=["POST"])
def predict():

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

    processed_lily = lily_postprocess(
        predicted_lily,
        int(settings.get("clef", 1)),
        int(settings.get("key", 0)),
        int(settings.get("tempo", 1)),
    )

    path = generate_audio(processed_lily)

    return jsonify(url_for("static", filename=path.split(r"/")[-1]))
