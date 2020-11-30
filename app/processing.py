from subprocess import Popen, run, CalledProcessError, PIPE
from os import remove
from re import findall
import cv2
from PIL import Image
import numpy as np
from uuid import uuid4
from pathlib import Path
from midi2audio import FluidSynth


def threshold_image(image):
    """"""
    grayImage = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
    return cv2.threshold(grayImage, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]
    # image = cv2.cvtColor(post_bin, cv2.COLOR_GRAY2RGB)
    # return post_bin


def resize(image, height):
    if len(image.shape) != 2 or image.shape[0] == 0 or image.shape[1] == 0:
        raise ValueError("Wrong shape of image in resize")
    width = int(float(height * image.shape[1]) / image.shape[0])
    resized_img = cv2.resize(image, (width, height))
    return resized_img


def preprocess_image(image, height):
    if len(image.shape) != 3:
        raise ValueError("Wrong shape of image")
    image = threshold_image(image)
    image = resize(image, height)
    image = (255.0 - image) / 255.0
    return image


def lily_fix_notation(lily):
    lily = "{ { " + lily.strip("| ").replace("|", "} {")
    lily += " } }"
    return lily


# lily - lilypond w formie stringu, key - oznaczenie tonacji, int w przedziale [-6;6]
def lily_set_key(lily, key):
    if key > 0:
        return apply_sharps(lily, key)
    if key < 0:
        return apply_flats(lily, key)
    return lily


def apply_sharps(lily, key):
    if key >= 1:
        lily = lily.replace("f", "fis")
    if key >= 2:
        lily = lily.replace("c", "cis")
    if key >= 3:
        lily = lily.replace("g", "gis")
    if key >= 4:
        lily = lily.replace("d", "dis")
    if key >= 5:
        lily = lily.replace("a", "ais")
    if key >= 6:
        lily = lily.replace("e", "eis")
    return lily


def apply_flats(lily, key):
    if key <= -1:
        lily = lily.replace("b", "bes")
    if key <= -2:
        lily = lily.replace("e", " ees")
    if key <= -3:
        lily = lily.replace("a", "aes")
    if key <= -4:
        lily = lily.replace("d", "des")
    if key <= -5:
        lily = lily.replace("g", "ges")
    if key <= -6:
        lily = lily.replace("c", "ces")
    return lily


def lily_adjust_from_bass_notation(lily):
    """
    bierze lilypond string, zwraca ten string dostosowany do klucza basowego f
    """
    pitches = [
        "c,",
        "d,",
        "e,",
        "f,",
        "g,",
        "a,",
        "b,",
        "c",
        "d",
        "e",
        "f",
        "g",
        "a",
        "b",
        "c'",
        "d'",
        "e'",
        "f'",
        "g'",
        "a'",
        "b'",
        "c''",
        "d''",
        "e''",
        "f''",
        "g''",
        "a''",
        "b''",
        "c'''",
    ]

    note_pattern = r"\w{1}'*,*\d"
    for note in findall(note_pattern, lily):
        pitch = findall(r"[^\d]+", note)[0]
        duration = findall(r"\d+", note)[0]
        index = pitches.index(pitch)

        lily = lily.replace(str(note), pitches[index - 12] + duration)

    return lily


def lily_set_tempo(lily, tempo):
    if tempo == 1:
        lily = lily[:2] + r"\tempo 4 = 60 " + lily[2:]
    elif tempo == 2:
        lily = lily[:2] + r"\tempo 4 = 120 " + lily[2:]
    elif tempo == 3:
        lily = lily[:2] + r"\tempo 4 = 180 " + lily[2:]

    return lily


def lily_postprocess(lily, clef=1, key=0, tempo=1):
    if lily == "":
        raise ValueError("Empty Lilypond String")
    if clef == 2:
        lily = lily_adjust_from_bass_notation(lily)
    lily = lily_set_key(lily, key)
    if clef == 2:
        lily = lily[:2] + r"\clef bass " + lily[2:]
    lily = lily_fix_notation(lily)
    lily = lily_set_tempo(lily, tempo)

    return lily


def generate_mid(lily, path):
    ly_string = '\\version "2.10.33"\n'
    ly_string += "\\score{\n"
    ly_string += lily + "\n"
    ly_string += "\\midi{}}"
    try:
        f = open(path + ".ly", "w")
        f.write(ly_string)
        f.close()
    except:
        return False
    # command = f"lilypond -dmidi-extension=midi -o {path} {path}.ly"
    try:
        # run_result = run(command, shell=True, check=True)
        run_result = run(
            ["lilypond", "-dmidi-extension=midi", "-o", f"{path}", f"{path}.ly"],
            check=True,
        )
    except CalledProcessError:
        if Path(path + ".ly").is_file():
            remove(path + ".ly")
        if Path(path + ".midi").is_file():
            remove(path + ".midi")
        return False

    if Path(path + ".ly").is_file():
        remove(path + ".ly")
    return True


def generate_wav(path):
    if not Path(f"{path}.midi").is_file():
        return False
    FluidSynth().midi_to_audio(f"{path}.midi", f"{path}.wav")
    if not Path(f"{path}.wav").is_file():
        return False
    return True


def generate_audio(lily, dir_path="./app/static"):
    filename = uuid4().hex
    path = f"{dir_path}/{filename}"

    if generate_mid(lily, path):
        if generate_wav(path):
            return f"{path}.wav"
    else:
        return False
