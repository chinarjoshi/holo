import os
import cv2
import numpy as np
from tensorflow import keras
from keras.models import load_model


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


# Open palm for expand, close palm for retract, ok for right, peace for left, L for rotate up and down.


def predict_image(image: np.ndarray, model: keras.Model) -> np.int64:
    """Returns gesture result and confidence given cv2 image.

    Formats a given image to fit tensorflow image size requireemnts, takes
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
    pred_array = model.predict(image)

    return np.argmax(pred_array)


def gesture_names(gestures: tuple = ("Fist", "L", "Okay", "Palm", "Peace")) -> dict:
    """Maps gestures to their index for use in confidence array."""
    return {index: gesture for index, gesture in enumerate(gestures)}


def map_gestures(confidence_index: np.int64, gesture_names: dict) -> str:
    """Returns gesture type and confidence given max index from confidence array."""
    result = gesture_names[confidence_index]
    score = float("%0.2f" % (max(pred_array[0]) * 100))
    return result, score


def prediction_from_camera():
    """Enables webcam and returns transformation type and confidence."""
    camera = cv2.VideoCapture(0)

    while camera.isOpened():
        # ret returns True if camera is running, frame grabs each frame of the video feed
        running, frame = camera.read()

        if not running:
            break

        frame = np.stack((frame,)*3, axis=-1)

    else:
        frame = cv2.imread("../images/L.jpg")

        frame = cv2.resize(frame, (224, 224))
        frame = frame.reshape(1, 224, 224, 3)
        prediction, score = predict_image(frame, gesture_names, get_model())


if __name__ == "__main__":
    print(prediction_from_camera())
