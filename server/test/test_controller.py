import unittest2
from server.controller import *
from PIL import Image

class TestController(unittest2.TestCase):

    def test_allowed_file(self):
        true_filename = "image.jpg"
        false_filename = "doc.pdf"

        self.assertEqual(allowed_file(true_filename), True)
        self.assertEqual(allowed_file(false_filename), False)

    def test_files_handler(self):
        file = Image.open("real-1-custom.jpg")
        file_expected_result = "datas/real-1-custom.jpg"

        self.assertEqual(files_handler(file), file_expected_result)


if __name__ == "__main__":
    unittest2.main()
