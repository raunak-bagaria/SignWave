# SignWave : By Team DesiDecibels

SignWave is a bidirectional sign language translation application that bridges communication between users of Indian Sign Language (ISL) and English speakers.

## Overview

Our application leverages machine learning to provide real-time translation between Indian Sign Language and English, making communication more accessible for individuals with speech and hearing impairments. The system uses computer vision and natural language processing techniques to create an intuitive translation interface.

## Features

- **Voice/Text to Sign Language**: Convert spoken words or written text into corresponding sign language animations.
- **Sign Language to Text**: Capture hand gestures through a camera and translate them into English text in real-time.
- **User-friendly Interface**: Available in both desktop GUI (Tkinter) and web application (Streamlit) formats.
- **Real-time Processing**: Instant translations with minimal delay.

## How It Works

### Text/Voice to Sign Language:
1. Input text directly or use speech recognition to convert voice to text
2. The text is processed and mapped to corresponding sign language animations
3. Individual words are translated into sign language gestures and displayed as a continuous animation

### Sign Language to Text:
1. The webcam captures hand gestures in real-time
2. Computer vision algorithms detect and track hand positions
3. The machine learning model classifies the gestures into corresponding English words
4. Text output is displayed on the screen

## Usage

### Prerequisites
- Python 3.8
- Required libraries listed in `requirements.txt`

### Installation
1. Clone the repository
2. Install dependencies: `pip install -r requirements.txt`
3. Run the application:
   - For desktop UI: `python main.py`
   - For web UI: `streamlit run homepage.py`
