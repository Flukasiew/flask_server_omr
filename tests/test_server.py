import unittest
from os import remove, path
import numpy as np
from PIL import Image
from app import processing, file_cleanup, model_handler
from app import app


class TestProcessing(unittest.TestCase):
    def test_resize(self):
        image = np.ones((138, 560))
        result = processing.resize(image, 128)
        expected_width = int(float(128 * image.shape[1]) / image.shape[0])
        self.assertEqual((128, expected_width), result.shape)

        image = np.ones((100, 560))
        result = processing.resize(image, 128)
        expected_width = int(float(128 * image.shape[1]) / image.shape[0])
        self.assertEqual((128, expected_width), result.shape)

    def test_resize_wrong_dim(self):
        with self.assertRaises(ValueError):
            result = processing.resize(np.ones((0, 1)), 128)

    def test_generate_mid(self):
        self.assertEqual(
            processing.generate_mid("{ { c'''8 e''8 r4 c''2 } }", "test"), True
        )

    def test_generate_mid_invalid_input(self):
        self.assertEqual(processing.generate_mid("gibberish  sdf  ff", "test"), False)
        self.assertEqual(
            processing.generate_mid("{{wron_note c''' e'''}}", "test"), False
        )

    def test_generate_wav(self):
        self.assertEqual(processing.generate_wav("./test_data/example"), True)

    def test_generate_wav_wrong_file(self):
        self.assertEqual(processing.generate_wav("./test_data/I_dont_Exist"), False)

    def test_generate_wav_invalid_input(self):
        self.assertEqual(processing.generate_wav(""), False)

    def test_generate_audio(self):

        lily = "{ { c'''8 e''8 r4 c''2 } }"
        result = processing.generate_audio(lily)
        self.assertEqual("wav" in result, True)
        remove(result)
        remove(result[:-3] + "mid")

    def test_generate_audio_invalid_input(self):
        self.assertEqual(processing.generate_audio("gibeberish"), False)
        self.assertEqual(processing.generate_audio("{ not valid { c''' e'''}}"), False)

    def test_lily_fix_notation_base(self):
        # DOes this even need to be tested?
        self.assertEqual(
            processing.lily_fix_notation(
                " b''2 r2 | f''2 b''8 c'''8 r8 b''8 | r4 d''8 c''8 c''4 e''4"
            ),
            "{ { b''2 r2 } { f''2 b''8 c'''8 r8 b''8 } { r4 d''8 c''8 c''4 e''4 } }",
        )

        self.assertEqual(
            processing.lily_fix_notation(
                "| b''2 r2 | f''2 b''8 c'''8 r8 b''8 | r4 d''8 c''8 c''4 e''4|"
            ),
            "{ { b''2 r2 } { f''2 b''8 c'''8 r8 b''8 } { r4 d''8 c''8 c''4 e''4 } }",
        )
        self.assertEqual(
            processing.lily_fix_notation(
                "b''2 r2 | f''2 b''8 c'''8 r8 b''8 | r4 d''8 c''8 c''4 e''4|"
            ),
            "{ { b''2 r2 } { f''2 b''8 c'''8 r8 b''8 } { r4 d''8 c''8 c''4 e''4 } }",
        )

        self.assertEqual(
            processing.lily_fix_notation(
                "b''2 r2  f''2 b''8 c'''8 r8 b''8 | r4 d''8 c''8 c''4 e''4|"
            ),
            "{ { b''2 r2  f''2 b''8 c'''8 r8 b''8 } { r4 d''8 c''8 c''4 e''4 } }",
        )

    def test_lily_fix_notation_empty(self):
        self.assertEqual(processing.lily_fix_notation(""), "{ {  } }")

    def test_lily_fix_notation_letters(self):
        self.assertEqual(
            processing.lily_fix_notation("abcdefghijklmnoprstqwyz"),
            "{ { abcdefghijklmnoprstqwyz } }",
        )

    def test_lily_set_tempo(self):

        self.assertEqual(
            processing.lily_set_tempo(
                "{ { b''2 r2 } { f''2 b''8 c'''8 r8 b''8 } { r4 d''8 c''8 c''4 e''4 } }",
                1,
            ),
            r"{ \tempo 4 = 60 { b''2 r2 } { f''2 b''8 c'''8 r8 b''8 } { r4 d''8 c''8 c''4 e''4 } }",
        )
        self.assertEqual(
            processing.lily_set_tempo(
                "{ { b''2 r2 } { f''2 b''8 c'''8 r8 b''8 } { r4 d''8 c''8 c''4 e''4 } }",
                2,
            ),
            r"{ \tempo 4 = 120 { b''2 r2 } { f''2 b''8 c'''8 r8 b''8 } { r4 d''8 c''8 c''4 e''4 } }",
        )
        self.assertEqual(
            processing.lily_set_tempo(
                "{ { b''2 r2 } { f''2 b''8 c'''8 r8 b''8 } { r4 d''8 c''8 c''4 e''4 } }",
                3,
            ),
            r"{ \tempo 4 = 180 { b''2 r2 } { f''2 b''8 c'''8 r8 b''8 } { r4 d''8 c''8 c''4 e''4 } }",
        )

    def test_lily_set_tempo_broken_lily(self):
        self.assertEqual(
            processing.lily_set_tempo(
                "''2 b''8 c'''8 r8 b''8 } { r4 d''8 c''8 c''4 e''4 } }", 1
            ),
            r"''\tempo 4 = 60 2 b''8 c'''8 r8 b''8 } { r4 d''8 c''8 c''4 e''4 } }",
        )

    def test_apply_sharps(self):
        lily = "c''2 e''4 f''16 c''16 d''16 a'16 | b'4 a''4 f''2 | e''4 e'4 g'2 |"
        self.assertEqual(processing.apply_sharps(lily, 0), lily)
        self.assertEqual(
            processing.apply_sharps(lily, 1),
            "c''2 e''4 fis''16 c''16 d''16 a'16 | b'4 a''4 fis''2 | e''4 e'4 g'2 |",
        )
        self.assertEqual(
            processing.apply_sharps(lily, 2),
            "cis''2 e''4 fis''16 cis''16 d''16 a'16 | b'4 a''4 fis''2 | e''4 e'4 g'2 |",
        )
        self.assertEqual(
            processing.apply_sharps(lily, 3),
            "cis''2 e''4 fis''16 cis''16 d''16 a'16 | b'4 a''4 fis''2 | e''4 e'4 gis'2 |",
        )
        self.assertEqual(
            processing.apply_sharps(lily, 4),
            "cis''2 e''4 fis''16 cis''16 dis''16 a'16 | b'4 a''4 fis''2 | e''4 e'4 gis'2 |",
        )
        self.assertEqual(
            processing.apply_sharps(lily, 5),
            "cis''2 e''4 fis''16 cis''16 dis''16 ais'16 | b'4 ais''4 fis''2 | e''4 e'4 gis'2 |",
        )
        self.assertEqual(
            processing.apply_sharps(lily, 6),
            "cis''2 eis''4 fis''16 cis''16 dis''16 ais'16 | b'4 ais''4 fis''2 | eis''4 eis'4 gis'2 |",
        )

    def test_apply_flats(self):
        lily = "c''2 e''4 f''16 c''16 d''16 a'16 | b'4 a''4 f''2 | e''4 e'4 g'2 |"
        self.assertEqual(processing.apply_flats(lily, 0), lily)
        self.assertEqual(
            processing.apply_flats(lily, -1),
            "c''2 e''4 f''16 c''16 d''16 a'16 | bes'4 a''4 f''2 | e''4 e'4 g'2 |",
        )
        self.assertEqual(
            processing.apply_flats(lily, -2),
            "c''2  ees''4 f''16 c''16 d''16 a'16 | bes'4 a''4 f''2 |  ees''4  ees'4 g'2 |",
        )
        self.assertEqual(
            processing.apply_flats(lily, -3),
            "c''2  ees''4 f''16 c''16 d''16 aes'16 | bes'4 aes''4 f''2 |  ees''4  ees'4 g'2 |",
        )
        self.assertEqual(
            processing.apply_flats(lily, -4),
            "c''2  ees''4 f''16 c''16 des''16 aes'16 | bes'4 aes''4 f''2 |  ees''4  ees'4 g'2 |",
        )
        self.assertEqual(
            processing.apply_flats(lily, -5),
            "c''2  ees''4 f''16 c''16 des''16 aes'16 | bes'4 aes''4 f''2 |  ees''4  ees'4 ges'2 |",
        )
        self.assertEqual(
            processing.apply_flats(lily, -6),
            "ces''2  ees''4 f''16 ces''16 des''16 aes'16 | bes'4 aes''4 f''2 |  ees''4  ees'4 ges'2 |",
        )

    def test_adjust_from_bass_notation(self):
        lily = " c''2 e''4 f''16 c''16 d''16 a'16 | b'4 e''4 f''2 | e''4 b'8 e'8 g'2 |"
        self.assertEqual(
            processing.lily_adjust_from_bass_notation(lily),
            " e2 g4 a16 e16 f16 c16 | d4 g4 a2 | g4 d8 g,8 b,2 |",
        )
        lily = "c''2 e''4 f''16 c''16 d''16 a'16"
        self.assertEqual(
            processing.lily_adjust_from_bass_notation(lily),
            "e2 g4 a16 e16 f16 c16",
        )

    def test_adjust_from_bass_notation_broken_input(self):
        lily = "c''2 e''4 | | f''16 c''16 | d''16 a'16"
        self.assertEqual(
            processing.lily_adjust_from_bass_notation(lily),
            "e2 g4 | | a16 e16 | f16 c16",
        )

    def test_lily_set_key(self):
        lily = "c''2 e''4 f''16 c''16 d''16 a'16 | b'4 a''4 f''2 | e''4 e'4 g'2 |"
        self.assertEqual(processing.lily_set_key(lily, 0), lily)
        self.assertEqual(
            processing.lily_set_key(lily, -1),
            "c''2 e''4 f''16 c''16 d''16 a'16 | bes'4 a''4 f''2 | e''4 e'4 g'2 |",
        )
        self.assertEqual(
            processing.lily_set_key(lily, -2),
            "c''2  ees''4 f''16 c''16 d''16 a'16 | bes'4 a''4 f''2 |  ees''4  ees'4 g'2 |",
        )
        self.assertEqual(
            processing.lily_set_key(lily, -3),
            "c''2  ees''4 f''16 c''16 d''16 aes'16 | bes'4 aes''4 f''2 |  ees''4  ees'4 g'2 |",
        )
        self.assertEqual(
            processing.lily_set_key(lily, -4),
            "c''2  ees''4 f''16 c''16 des''16 aes'16 | bes'4 aes''4 f''2 |  ees''4  ees'4 g'2 |",
        )
        self.assertEqual(
            processing.lily_set_key(lily, -5),
            "c''2  ees''4 f''16 c''16 des''16 aes'16 | bes'4 aes''4 f''2 |  ees''4  ees'4 ges'2 |",
        )
        self.assertEqual(
            processing.lily_set_key(lily, -6),
            "ces''2  ees''4 f''16 ces''16 des''16 aes'16 | bes'4 aes''4 f''2 |  ees''4  ees'4 ges'2 |",
        )
        self.assertEqual(
            processing.lily_set_key(lily, 1),
            "c''2 e''4 fis''16 c''16 d''16 a'16 | b'4 a''4 fis''2 | e''4 e'4 g'2 |",
        )
        self.assertEqual(
            processing.lily_set_key(lily, 2),
            "cis''2 e''4 fis''16 cis''16 d''16 a'16 | b'4 a''4 fis''2 | e''4 e'4 g'2 |",
        )
        self.assertEqual(
            processing.lily_set_key(lily, 3),
            "cis''2 e''4 fis''16 cis''16 d''16 a'16 | b'4 a''4 fis''2 | e''4 e'4 gis'2 |",
        )
        self.assertEqual(
            processing.lily_set_key(lily, 4),
            "cis''2 e''4 fis''16 cis''16 dis''16 a'16 | b'4 a''4 fis''2 | e''4 e'4 gis'2 |",
        )
        self.assertEqual(
            processing.lily_set_key(lily, 5),
            "cis''2 e''4 fis''16 cis''16 dis''16 ais'16 | b'4 ais''4 fis''2 | e''4 e'4 gis'2 |",
        )
        self.assertEqual(
            processing.lily_set_key(lily, 6),
            "cis''2 eis''4 fis''16 cis''16 dis''16 ais'16 | b'4 ais''4 fis''2 | eis''4 eis'4 gis'2 |",
        )

    def test_lily_postprocess(self):
        with self.assertRaises(ValueError):
            result = processing.lily_postprocess("", 1, 1, 1)


class TestCleanUp(unittest.TestCase):
    def test_cleanup_old_files(self):
        for i in range(5):
            f = open(f"./app/static/{i}.txt", "w")
            f.close()
        self.assertEqual(file_cleanup.cleanup(1), 0)
        for i in range(5):
            s = "./app/static/" + str(i) + ".txt"
            if path.isfile(s):
                remove(s)

    def test_cleanup_base(self):
        file_cleanup.cleanup(0)
        for i in range(5):
            f = open(f"./app/static/{i}.txt", "w")
            f.close()
        self.assertEqual(file_cleanup.cleanup(1), 0)
        self.assertEqual(file_cleanup.cleanup(0), 5)
        for i in range(5):
            s = "./app/static/" + str(i) + ".txt"
            if path.isfile(s):
                remove(s)

    def test_cleanup_empty_dir(self):
        self.assertEqual(file_cleanup.cleanup(0), 0)


class TestRestAPI(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()

    def test_predict_base_filled_settings(self):
        settings = {
            "tempo": 2,
            "key": 5,
            "clef": 2,
            "image": open("./test_data/test.jpg", "rb"),
        }

        response = self.app.post(
            "/predict_uri", data=settings, content_type="multipart/form-data"
        )

        self.app.post()
        self.assertEqual(response.status_code, 200)

    def test_predict_invalid_settings(self):
        settings = {
            "tempo": "a",
            "key": 5,
            "clef": 2,
            "image": open("./test_data/test.jpg", "rb"),
        }

        response = self.app.post(
            "/predict_uri", data=settings, content_type="multipart/form-data"
        )

        self.app.post()
        self.assertEqual(response.status_code, 500)

    def test_predict_no_settings(self):
        settings = {
            "image": open("./test_data/test.jpg", "rb"),
        }

        response = self.app.post(
            "/predict_uri", data=settings, content_type="multipart/form-data"
        )

        self.app.post()
        self.assertEqual(response.status_code, 200)

    def test_predict_no_image(self):
        settings = {
            "tempo": 0,
            "key": 5,
            "clef": 2,
        }

        response = self.app.post(
            "/predict_uri", data=settings, content_type="multipart/form-data"
        )

        self.app.post()
        self.assertEqual(response.status_code, 400)
        settings = {}

        response = self.app.post(
            "/predict_uri", data=settings, content_type="multipart/form-data"
        )
        self.app.post()
        self.assertEqual(response.status_code, 400)

    def test_predict_invalid_form_names(self):
        settings = {
            "tempo": 0,
            "key": 5,
            "clef": 2,
            "wrong_name": open("./test_data/test.jpg", "rb"),
        }

        response = self.app.post(
            "/predict_uri", data=settings, content_type="multipart/form-data"
        )

        self.app.post()
        self.assertEqual(response.status_code, 400)

        settings = {
            "wrong": 0,
            "this_too": 5,
            "clef": 2,
            "image": open("./test_data/test.jpg", "rb"),
        }

        response = self.app.post(
            "/predict_uri", data=settings, content_type="multipart/form-data"
        )

        self.app.post()
        self.assertEqual(response.status_code, 200)

    def test_ping(self):
        response = self.app.get("/ping")
        self.assertEqual(response.status_code, 200)


class TestModelHandler(unittest.TestCase):
    def test_create_handler(self):
        model = model_handler.ModelHandler()

    def test_predict(self):
        model = model_handler.ModelHandler()
        img = np.asarray(Image.open("./test_data/test.jpg"))
        img = processing.preprocess_image(img, model.HEIGHT)
        predicted_lily = model.predict(img)
        self.assertEqual(type(predicted_lily), str)


if __name__ == "__main__":
    unittest.main()
