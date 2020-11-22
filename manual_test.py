#!/usr/bin/env python3

import requests

# from app import processing
from uuid import uuid4
from flask import Response

# from app import file_cleanup


def model_request():
    url = "http://127.0.1:9090/predict"
    # my_img = {"image": open("./example_65909.jpg", "rb")}
    my_img = {"image": open("./test_data/test.jpg", "rb")}
    response = requests.post(
        url, files=my_img, data={"clef": 2, "key": 1}, timeout=1000
    )

    print("here")
    # convert server response into JSON format.
    with open("new.mp3", "wb") as mp3file:
        mp3file.write(response.content)


# def clean_up_check():
#     for i in range(5):
#         f = open(f"./app/data/{i}.txt", "w")
#         f.close()

#     print(file_cleanup.cleanup(1))
#     print(file_cleanup.cleanup(0))


# def main():
#     # model_request()
#     lily = ""
#     processing.generate_mid(lily, "test")
#     processing.generate_mp3("test")


if __name__ == "__main__":
    # main()
    model_request()
    # clean_up_check()
