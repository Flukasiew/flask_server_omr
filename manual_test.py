#!/usr/bin/env python3
import requests
from uuid import uuid4
from flask import Response

import io
from midi2audio import FluidSynth


def main():
    url = "http://solfege.northeurope.cloudapp.azure.com/predict_uri"
    img = {"image": open("./test_data/test.jpg", "rb")}
    settings = {"tempo": 2, "key": -5, "clef": 2}
    response = requests.post(url, files=img, data=settings)
    print(response.content)

    # response = requests.get("http://solfege.northeurope.cloudapp.azure.com/ping")
    # print(response.content)

    with open("uri.txt", "w") as uri_file:
        uri_file.write(response.json())


def local_main():
    url = "http://localhost:5000/predict_uri"
    img = {"image": open("./test_data/test.jpg", "rb")}
    # Clef 2 gives bass, anything else gives standard
    settings = {"tempo": 3, "key": -5, "clef": 2}
    response = requests.post(url, files=img, data=settings)
    print(response.content)

    with open("uri.txt", "w") as uri_file:
        uri_file.write(response.json())


def get_file():
    url = "http://localhost:5000/geturi"
    # url = "http://solfege.northeurope.cloudapp.azure.com/ping"
    response = requests.get(url)
    print(response.content)


if __name__ == "__main__":
    # local_main()
    # main()
    get_file()

# FluidSynth().midi_to_audio("./test_data/example.midi", "output.wav")
