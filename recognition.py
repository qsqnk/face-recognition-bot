import cv2
import numpy as np

from io import BytesIO
from typing import List
from telegram import InputMediaPhoto
from deepface.detectors import FaceDetector

MODEL_NAME = 'retinaface'
DETECTOR = FaceDetector.build_model(MODEL_NAME)


def recognize_faces(input_stream: BytesIO) -> List[InputMediaPhoto]:
    image = cv2.imdecode(
        np.frombuffer(input_stream.read(), np.uint8), -1
    )

    _, regions = zip(
        *FaceDetector.detect_faces(DETECTOR, MODEL_NAME, image)
    )

    faces = []

    for region in regions:
        x, dx = region[0], region[2]
        y, dy = region[1], region[3]

        face = image[y: y + dy, x: x + dx]

        _, encoded = cv2.imencode('.png', face)
        byte_image = encoded.tobytes()

        faces.append(
            InputMediaPhoto(byte_image)
        )

    return faces
