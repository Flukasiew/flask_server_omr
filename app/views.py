from app import app
from app.processing import *
from app.model_handler import ModelHandler
from flask import request, render_template, jsonify


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


@app.route("/img_info", methods=["POST"])
def img_info():
    """
    Test function returning img.width, img.height
    """
    file = request.files["image"]
    img = Image.open(file.stream)

    return jsonify({"msg": "sucess", "size": [img.width, img.height]})


@app.route("/img_score", methods=["POST"])
def img_score():
    file = request.files["image"]
    img = np.asarray(Image.open(file.stream))

    print(img.shape, type(img))
    settings = request.form.to_dict()

    img = preprocess_image(img, model_handler.HEIGHT)

    result = model_handler.predict(img)

    return jsonify(
        {
            "msg": result,
        }
    )


@app.route("/ping")
def ping():
    pass


@app.route("/demo_audio")
def demo_audio():
    pass
