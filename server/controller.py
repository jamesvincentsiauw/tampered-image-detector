from PIL import Image, ImageChops, ImageEnhance
from skimage import transform
import numpy as np
import os
import shutil

ALLOWED_EXTENSIONS = {'tif', 'jpg', 'jpeg', 'png'}


def allowed_file(filename):
    # Return boolean based on the ALLOWED_EXTENSION list
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def convert_to_ela_image(path, quality):
    filename = path
    resaved_filename = filename.split('.')[0] + '.resaved.jpg'
    ELA_filename = filename.split('.')[0] + '.ela.png'

    im = Image.open(filename).convert('RGB')
    im.save(resaved_filename, 'JPEG', quality=quality)
    resaved_im = Image.open(resaved_filename)

    ela_im = ImageChops.difference(im, resaved_im)

    extrema = ela_im.getextrema()
    max_diff = max([ex[1] for ex in extrema])
    if max_diff == 0:
        max_diff = 1
    scale = 255.0 / max_diff

    ela_im = ImageEnhance.Brightness(ela_im).enhance(scale)

    return ela_im


def load(filename):
    np_image = convert_to_ela_image(filename, 90)
    np_image = np.array(np_image).astype('float32') / 255
    np_image = transform.resize(np_image, (128, 128, 3))
    np_image = np.expand_dims(np_image, axis=0)
    return np_image


def get_class_name(label):
    if label:
        return 'Tampered Image'
    return 'Real Image'


def choose_model(version):
    if version == 'v1':
        used_model = 'saved-models/model-v1-with-casia.h5'
    elif version == 'v2':
        used_model = 'saved-models/model-v2-with-mixed-dataset.h5'
    elif version == 'v3':
        used_model = 'saved-models/model-v3-with-real-fake-dataset.h5'
    elif version == 'v4':
        used_model = 'saved-models/model-v4-with-mixed-dataset.h5'
    else:
        return 'error'
    return used_model


def files_handler(file):
    if not allowed_file(file.filename):
        return 'error'

    # check the directory to save the file
    if not os.path.exists('data/'):
        # make a directory if it doesn't exist
        os.makedirs('data')

    filepath = 'data/'
    # save file to /data/files/finalTasks
    file.save(os.path.join(filepath, file.filename))

    return filepath + file.filename


def process_prediction(model, img):
    try:
        for i in zip(model.predict_proba(img, batch_size=50), model.predict_classes(img, batch_size=50),
                     model.predict(img, batch_size=50)):
            val = {
                'status': 'success',
                'message': 'Predicting Image Succeed',
                'results': {
                    'prediction': get_class_name(i[1]),
                    'probability': str(round(max(i[0]) * 100, 2)) + '%'
                }
            }
        if os.path.exists('data'):
            shutil.rmtree('data')
        return val
    except Exception as e:
        return {
            'status': 'error',
            'message': e.args
        }
