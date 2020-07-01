import unittest2
from server.controller import *
from PIL import Image
from keras.models import load_model


class TestController(unittest2.TestCase):

    def test_allowed_file(self):
        true_filename = 'image.jpg'
        false_filename = 'doc.pdf'

        self.assertEqual(allowed_file(true_filename), True)
        self.assertEqual(allowed_file(false_filename), False)

    def test_files_handler(self):
        file = Image.open('real-1-custom.jpg')
        file_expected_result = 'datas/real-1-custom.jpg'

        self.assertEqual(files_handler(file), file_expected_result)

    def test_class_name(self):
        self.assertEqual(get_class_name(1), 'Tampered Image')
        self.assertEqual(get_class_name(0), 'Real Image')

    def test_choose_model(self):
        model_dict = {
            'v1': 'saved-models/model-v1-with-casia.h5',
            'v2': 'saved-models/model-v2-with-mixed-dataset.h5',
            'v3': 'saved-models/model-v3-with-real-fake-dataset.h5'
        }
        model_version = ['v1', 'v2', 'v3']
        for item in model_version:
            self.assertEqual(choose_model(item), model_dict[item])
        self.assertEqual(choose_model('v4'), 'error')

    def test_prediction(self):
        model_dict = {
            'v1': '../saved-models/model-v1-with-casia.h5',
            'v2': '../saved-models/model-v2-with-mixed-dataset.h5',
            'v3': '../saved-models/model-v3-with-real-fake-dataset.h5'
        }
        model_version = ['v2', 'v1', 'v3']
        img = load('real-1-custom.jpg')
        expected_result = ['status', 'message', 'results']

        for item in model_version:
            model = load_model(model_dict[item])
            result = process_prediction(model, img)
            self.assertEqual(list(result.keys()), expected_result)


if __name__ == '__main__':
    unittest2.main()
