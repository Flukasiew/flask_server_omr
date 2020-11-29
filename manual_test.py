#!/usr/bin/env python3

import requests

from uuid import uuid4
from flask import Response

import io


def main():
    url = "http://solfege.northeurope.cloudapp.azure.com/predict_uri"
    img = {"image": open("./test_data/test.jpg", "rb")}
    response = requests.post(url, files=img)
    print(response.content)

    # with open("new.mp3", "wb") as mp3file:
    #     mp3file.write(response.content)


def local_main():
    url = "http://localhost:5000/predict_uri"
    img = {"image": open("./test_data/test.jpg", "rb")}
    response = requests.post(url, files=img)
    print(response.content)


if __name__ == "__main__":
    local_main()
