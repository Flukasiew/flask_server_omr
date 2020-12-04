#!/usr/bin/env python3
import requests
from uuid import uuid4
from flask import Response

import io
from midi2audio import FluidSynth


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
    # Clef 2 gives bass, anything else gives standard
    settings = {"tempo": 3, "key": -5, "clef": 2}
    response = requests.post(url, files=img, data=settings)
    print(response.content)

    with open("uri.txt", "w") as uri_file:
        uri_file.write(response.json())


if __name__ == "__main__":
    local_main()
    # main()

    # FluidSynth().midi_to_audio("./test_data/example.midi", "output.wav")
