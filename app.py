import numpy_compat
import tensorflow as tf
import numpy as np
import streamlit as st
import cv2
from cvzone.HandTrackingModule import HandDetector
import math

# Load model and labels
def app():
    model = tf.keras.models.load_model("keras_model.h5")  # Load the Keras model
    labels = []
    with open("labels.txt", "r") as f:
        labels = [line.strip() for line in f.readlines()]  # Load labels from file

    detector = HandDetector(maxHands=1)
    offset = 20
    imgSize = 300

    st.title("Sign Language Detection")
    st.write("This app detects hand signs using a machine learning model.")

    # Webcam input
    stframe = st.empty()
    cap = cv2.VideoCapture(0)

    while True:
        success, img = cap.read()
        imgOutput = img.copy()
        hands, img = detector.findHands(img)

        if hands:
            hand = hands[0]
            x, y, w, h = hand['bbox']

            imgWhite = np.ones((imgSize, imgSize, 3), np.uint8) * 255
            imgCrop = img[y-offset:y + h + offset, x-offset:x + w + offset]
            imgCropShape = imgCrop.shape
            aspectRatio = h / w

            if aspectRatio > 1:
                k = imgSize / h
                wCal = math.ceil(k * w)
                imgResize = cv2.resize(imgCrop, (wCal, imgSize))
                imgResizeShape = imgResize.shape
                wGap = math.ceil((imgSize - wCal) / 2)
                imgWhite[:, wGap: wCal + wGap] = imgResize
                imgWhite = np.expand_dims(imgWhite, axis=0)  # Add batch dimension
                prediction = model.predict(imgWhite)
                index = np.argmax(prediction)
            else:
                k = imgSize / w
                hCal = math.ceil(k * h)
                imgResize = cv2.resize(imgCrop, (imgSize, hCal))
                imgResizeShape = imgResize.shape
                hGap = math.ceil((imgSize - hCal) / 2)
                imgWhite[hGap: hCal + hGap, :] = imgResize
                imgWhite = np.expand_dims(imgWhite, axis=0)  # Add batch dimension
                prediction = model.predict(imgWhite)
                index = np.argmax(prediction)
                
            cv2.rectangle(imgOutput, (x-offset, y-offset-70), (x-offset+400, y-offset+60-50), (0, 255, 0), cv2.FILLED)
            cv2.putText(imgOutput, labels[index], (x, y-30), cv2.FONT_HERSHEY_COMPLEX, 2, (0, 0, 0), 2)
            cv2.rectangle(imgOutput, (x-offset, y-offset), (x + w + offset, y + h + offset), (0, 255, 0), 4)

        # Convert BGR image to RGB
        img_rgb = cv2.cvtColor(imgOutput, cv2.COLOR_BGR2RGB)

        # Display the image
        stframe.image(img_rgb, channels="RGB", use_column_width=True)

app()