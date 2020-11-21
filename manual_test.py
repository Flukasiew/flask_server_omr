#!/usr/bin/env python3

import requests


def main():
    url = "http://127.0.0.1:5000/img_score"
    # my_img = {"image": open("./example_65909.jpg", "rb")}
    my_img = {"image": open("test.jpg", "rb")}
    response = requests.post(url, files=my_img)

    # convert server response into JSON format.
    print(response.json())


if __name__ == "__main__":
    main()
