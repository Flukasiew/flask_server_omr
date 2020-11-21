import unittest
import numpy as np
from app import processing


class TestProcessing(unittest.TestCase):
    def setUp(self):
        pass

    def test_threshold_image_empty(self):
        image = np.zeros((128, 512, 3))
        image[:, :256, :] = 1
        pass

    def test_resize(self):
        image = np.ones((138, 560))
        result = processing.resize(image, 128)
        expected_width = int(float(128 * image.shape[1]) / image.shape[0])
        self.assertEqual((128, expected_width), result.shape)

        image = np.ones((100, 560))
        result = processing.resize(image, 128)
        expected_width = int(float(128 * image.shape[1]) / image.shape[0])
        self.assertEqual((128, expected_width), result.shape)

        with self.assertRaises(ValueError):
            result = processing.resize(np.ones((0, 1)), 128)


if __name__ == "__main__":
    unittest.main()
