import os
from dataclasses import dataclass

import time
import cv2
import numpy as np
from tensorflow import keras
from keras.models import load_model


@dataclass
class GestureOutput:
    gesture: str
    confidence: int

    def __repr__(self):
        return f'gesture: {self.gesture}, confidence: {self.confidence}%'


def get_model(path: str = "../models/VGG_cross_validated.h5") -> keras.Model:
    """Returns model interface from a path to keras h5 model file.

    :param path: path to the keras h5 file
    :type path: str
    :return: keras model interface
    :rtype: keras.Model
    """
    if os.path.exists(path):
        return load_model("../models/VGG_cross_validated.h5")
    else:
        raise Exception(f"Model not found in relative path: {path}")


def predict_gesture(image: np.ndarray, model: keras.Model) -> np.int64:
    """Returns gesture result and confidence given cv2 image.

    Formats a given image to fit tensorflow image size requirements, takes
    prediction of image from model, finds index of highest confidence value,
    and finally returns the name after mapping index to gesture name.

    :param image: frame from webcam for processing
    :param gesture_names: mapping of gesture name to confidence index
    :param model: pretrained model to return gesture type and confidence
    :type image: np.ndarray
    :type gesture_names: dict
    :type model: keras.Model
    :return: gesture identification and confidence percentage
    :rtype: int
    """
    image = np.array(image, dtype="float32")
    image /= 255
    return model.predict(image)


def gesture_names(return_transformations: bool = True) -> dict:
    """Maps gestures to their index for use in confidence array.

    Gesture mapping is as follows:
      Fist  : retract
      L     : rotate
      Okay  : right
      Palm  : expand
      Peace : left
    """
    transformations = ('retract', 'rotate', 'right', 'expand', 'left')
    gestures = ('Fist', 'L', 'Okay', 'Palm', 'Peace')
    return {index: gesture
            for index, gesture in enumerate(transformations if return_transformations else gestures)}


def map_gestures(confidence_array: np.array, gesture_names: dict) -> tuple:
    """Returns gesture type and confidence given max index from confidence array."""
    gesture = gesture_names[np.argmax(confidence_array)]
    confidence = round(max(confidence_array[0] * 100))
    return GestureOutput(gesture, confidence)


def process_frame(image: np.ndarray) -> np.ndarray:
    frame = np.stack((image,) * 3, axis=-1)
    frame = cv2.resize(image, (224, 224))
    frame = frame.reshape(1, 224, 224, 3)
    return frame


def prediction_from_camera() -> GestureOutput:
    """Enables webcam and returns transformation type and confidence."""
    camera = cv2.VideoCapture(0)
    model = get_model()
    while camera.isOpened():
        _, frame = camera.read()
        prediction_index = predict_gesture(image=process_frame(frame), model=model)

        yield map_gestures(confidence_array=prediction_index, gesture_names=gesture_names(return_transformations=False))


# def run_process():
#     while True:
#         yield prediction_from_camera()


if __name__ == "__main__":
    for gesture in prediction_from_camera():
        print(gesture.gesture, gesture.confidence)
