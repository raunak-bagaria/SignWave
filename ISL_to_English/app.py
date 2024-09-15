import numpy_compat
import streamlit as st
import cv2
from cvzone.HandTrackingModule import HandDetector
from cvzone.ClassificationModule import Classifier
import numpy as np
import math

# Load model and labels
def app():
    classifier = Classifier("/home/raunak/Desktop/SignWave/ISL_to_English/keras_model.h5", "/home/raunak/Desktop/SignWave/ISL_to_English/labels.txt")
    detector = HandDetector(maxHands=1)
    offset = 20
    imgSize = 300

    # Define labels (must match the order used in training)
    labels = ["Afternoon","Evening","Good","Hello","I love you","Nice","No","Please","Thank you","Today","Yes"]

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
                prediction, index = classifier.getPrediction(imgWhite, draw=False)
            else:
                k = imgSize / w
                hCal = math.ceil(k * h)
                imgResize = cv2.resize(imgCrop, (imgSize, hCal))
                imgResizeShape = imgResize.shape
                hGap = math.ceil((imgSize - hCal) / 2)
                imgWhite[hGap: hCal + hGap, :] = imgResize
                prediction, index = classifier.getPrediction(imgWhite, draw=False)
                
            cv2.rectangle(imgOutput, (x-offset, y-offset-70), (x-offset+400, y-offset+60-50), (0, 255, 0), cv2.FILLED)
            cv2.putText(imgOutput, labels[index], (x, y-30), cv2.FONT_HERSHEY_COMPLEX, 2, (0, 0, 0), 2)
            cv2.rectangle(imgOutput, (x-offset, y-offset), (x + w + offset, y + h + offset), (0, 255, 0), 4)

        # Convert BGR image to RGB
        img_rgb = cv2.cvtColor(imgOutput, cv2.COLOR_BGR2RGB)

        # Display the image
        stframe.image(img_rgb, channels="RGB", use_column_width=True)