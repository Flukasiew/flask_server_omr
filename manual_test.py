#!/usr/bin/env python3

import requests

from uuid import uuid4
from flask import Response

import io


def main():
    url = "http://127.0.0.1:5000/predict_uri"
    # my_img = {"image": open("./example_65909.jpg", "rb")}
    # img = {"image": io.BytesIO(b"some initial text data")}  #
    img = {"image": open("./test_data/test.jpg", "rb")}
    response = requests.post(url, files=img)

    print(response.json())
    with open("file://127.0.0.1:5000" + str(response.json()), "wb") as mp3file:
        mp3file.write(response.content)
    # convert server response into JSON format.
    # with open("new.mp3", "wb") as mp3file:
    #     mp3file.write(response.content)


if __name__ == "__main__":
    main()
