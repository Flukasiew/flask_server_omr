from subprocess import Popen
from os import remove
from re import findall
from midi2audio import FluidSynth
import cv2
from PIL import Image
import numpy as np


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
    sample_img = cv2.resize(image, (width, height))
    return sample_img


def preprocess_image(image, height):
    image = threshold_image(image)
    image = resize(image, height)
    image = (255.0 - image) / 255.0
    return image


def fix_notation(lily):
    lily = "{ { " + lily.replace("|", "} {")
    if lily[-1] == "{":
        lily = lily[:-2]
    else:
        lily += "}"

    return lily


# lily - lilypond w formie stringu, key - oznaczenie tonacji, int w przedziale [-6;6]
def change_lilypond_key(lily, key):
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
        lily = lily.replace(" e", " ees")
    if key <= -3:
        lily = lily.replace("a", "aes")
    if key <= -4:
        lily = lily.replace("d", "des")
    if key <= -5:
        lily = lily.replace("g", "ges")
    if key <= -6:
        lily = lily.replace("c", "ces")
    return lily


def adjust_from_bass_notation(lily):
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


def postprocess_lily(lily, options):
    lily = fix_notation(lily)

    # Here we check for options and applly them also

    return lily


def generate_mid(ly_string, filename):
    ly_string = '\\version "2.10.33"\n' + ly_string
    try:
        f = open(filename + ".ly", "w")
        f.write(ly_string)
        f.close()
    except:
        return False
    command = f"lilypond -dmidi-extension=mid -o ./app/data/{filename} {filename}.ly"
    p = Popen(command, shell=True).wait()
    remove(filename + ".ly")
    return True


def generate_flac(path):
    fs = FluidSynth()
    output_path = f"{path[:-4]}.flac"
    fs.midi_to_audio("path", output_path)

    return output_path


def generate_audio(filename):
    pass
