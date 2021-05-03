from flask import current_app as app
from tensorflow import keras
from PIL import Image
import os
import cv2
import numpy as np
from werkzeug.utils import secure_filename


class RoadSignClassifier:
    CLASSES = {
        0: 'Speed limit (20km/h)',
        1: 'Speed limit (30km/h)',
        2: 'Speed limit (50km/h)',
        3: 'Speed limit (60km/h)',
        4: 'Speed limit (70km/h)',
        5: 'Speed limit (80km/h)',
        6: 'End of speed limit (80km/h)',
        7: 'Speed limit (100km/h)',
        8: 'Speed limit (120km/h)',
        9: 'No passing',
        10: 'No passing veh over 3.5 tons',
        11: 'Right-of-way at intersection',
        12: 'Priority road',
        13: 'Yield',
        14: 'Stop',
        15: 'No vehicles',
        16: 'Veh > 3.5 tons prohibited',
        17: 'No entry',
        18: 'General caution',
        19: 'Dangerous curve left',
        20: 'Dangerous curve right',
        21: 'Double curve',
        22: 'Bumpy road',
        23: 'Slippery road',
        24: 'Road narrows on the right',
        25: 'Road work',
        26: 'Traffic signals',
        27: 'Pedestrians',
        28: 'Children crossing',
        29: 'Bicycles crossing',
        30: 'Beware of ice/snow',
        31: 'Wild animals crossing',
        32: 'End speed + passing limits',
        33: 'Turn right ahead',
        34: 'Turn left ahead',
        35: 'Ahead only',
        36: 'Go straight or right',
        37: 'Go straight or left',
        38: 'Keep right',
        39: 'Keep left',
        40: 'Roundabout mandatory',
        41: 'End of no passing',
        42: 'End no passing veh > 3.5 tons'
    }

    def __init__(self):
        self._load_model()

    def _load_model(self):
        self.model = keras.models.load_model(os.path.join(app.root_path, 'TrafficSignRecognitionCNN'))

    def predict(self, image):
        self._prepare_image(image)
        return self.model.predict(self.data)

    def _prepare_image(self, temp_image):
        data = []
        image_fromarray = Image.fromarray(self._read_image(temp_image), 'RGB')
        temp_image.seek(0)
        resize_image = image_fromarray.resize((32, 32))
        data.append(np.array(resize_image))
        x = np.array(data)
        self.data = x / 255

    def _read_image(self, image_file):
        filename = secure_filename(image_file.filename)
        filepath = os.path.join(app.root_path, 'temp', filename)
        image_file.save(filepath)
        image_data = cv2.imread(filepath)[..., ::-1]
        os.remove(filepath)
        return image_data
