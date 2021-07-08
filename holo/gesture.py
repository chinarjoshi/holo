import cv2
import numpy as np
from tensorflow import keras
from keras.models import load_model


model = load_model('../models/VGG_cross_validated.h5')

gestures = {'L_': 'L',
           'fi': 'Fist',
           'C_': 'C',
           'ok': 'Okay',
           'pe': 'Peace',
           'pa': 'Palm'
            }

gesture_names = {0: 'C',
                 1: 'Fist',
                 2: 'L',
                 3: 'Okay',
                 4: 'Palm',
                 5: 'Peace'}

gestures_map = {'Fist' : 0,
                'L': 1,
                'Okay': 2,
                'Palm': 3,
                'Peace': 4
                }

def predict_image(image):
    image = np.array(image, dtype='float32')
    image /= 255
    pred_array = model.predict(image)

    # model.predict() returns an array of probabilities -
    # np.argmax grabs the index of the highest probability.
    result = gesture_names[np.argmax(pred_array)]

    # A bit of magic here - the score is a float, but I wanted to
    # display just 2 digits beyond the decimal point.
    score = float("%0.2f" % (max(pred_array[0]) * 100))
    print(f'Result: {result}, Score: {score}')
    return result, score



#starts the webcam, uses it as video source
# camera = cv2.VideoCapture(0) #uses webcam for video

# while camera.isOpened():
#     #ret returns True if camera is running, frame grabs each frame of the video feed
#     ret, frame = camera.read()

frame = cv2.imread('../images/L1.jpg')

# frame = np.stack((frame,)*3, axis=-1)
frame = cv2.resize(frame, (224, 224))
frame = frame.reshape(1, 224, 224, 3)
prediction, score = predict_image(frame)

# objects = {image: cv2.imread(f'../images/{image}.jpeg') for image in ('fist', 'palm', 'peace', 'ok')}
