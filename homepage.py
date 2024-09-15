import streamlit as st
import tensorflow as tf
import numpy as np
import cv2
import os
from PIL import Image
import speech_recognition as sr
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing import image
import tempfile
import imageio

image_x, image_y = 64, 64
model_path = 'model.h5'
op_dest = "filtered_data"
alpha_dest = "alphabet"


FRAME_WIDTH, FRAME_HEIGHT = 380, 260


@st.cache_resource
def load_classifier():
    return load_model(model_path, compile=False)

classifier = load_classifier()

def give_char(image):
    test_image = image.resize((64, 64))
    test_image = image.img_to_array(test_image)
    test_image = np.expand_dims(test_image, axis=0)
    result = classifier.predict(test_image)
    chars = "ABCDEFGHIJKMNOPQRSTUVWXYZ"
    indx = np.argmax(result[0])
    return chars[indx]

def check_sim(i, file_map):
    for item in file_map:
        for word in file_map[item]:
            if i == word:
                return 1, item
    return -1, ""


@st.cache_data
def prepare_file_map():
    dirListing = os.listdir(op_dest)
    editFiles = [item for item in dirListing if ".webp" in item]
    return {i: i.replace(".webp", "").split() for i in editFiles}

file_map = prepare_file_map()

def resize_frame(img):
    return img.resize((FRAME_WIDTH, FRAME_HEIGHT), Image.LANCZOS)

def func(a):
    all_frames = []
    words = a.split()
    for i in words:
        flag, sim = check_sim(i, file_map)
        if flag == -1:
            for j in i:
                im = Image.open(os.path.join(alpha_dest, f"{j.lower()}_small.gif"))
                frameCnt = im.n_frames
                for frame_cnt in range(frameCnt):
                    im.seek(frame_cnt)
                    img = im.copy()
                    img = resize_frame(img)
                    all_frames.extend([img] * 5) 
        else:
            im = Image.open(os.path.join(op_dest, sim))
            frameCnt = getattr(im, 'n_frames', 1)
            for frame_cnt in range(frameCnt):
                if frameCnt > 1:
                    im.seek(frame_cnt)
                img = im.copy()
                img = resize_frame(img)
                all_frames.append(img)
    return all_frames

def resize_frame(img):
    return img.convert('RGB').resize((FRAME_WIDTH, FRAME_HEIGHT), Image.LANCZOS)

def create_gif(frames, output_path, fps=10):
    if not frames:
        raise ValueError("No frames to create GIF")
    
    np_frames = [np.array(frame) for frame in frames]
    
    imageio.mimsave(output_path, np_frames, fps=fps, loop=0)

    if not os.path.exists(output_path) or os.path.getsize(output_path) == 0:
        raise IOError("Failed to create GIF file")

def main():
    st.title("Welcome to SignWave!")

    menu = ["Voice to Sign", "Sign to Voice"]
    choice = st.sidebar.selectbox("Select Mode", menu)

    if choice == "Voice to Sign":
        st.header("Voice to Sign")
        
        input_method = st.radio("Choose input method", ("Text", "Voice"))
        
        if input_method == "Text":
            text_input = st.text_input("Enter text:")
            if st.button("Convert"):
                with st.spinner("Generating GIF..."):
                    frames = func(text_input)
                    
                    if not frames:
                        st.error("No frames generated. Please try a different input.")
                    else:
                        with tempfile.NamedTemporaryFile(delete=False, suffix='.gif') as tmpfile:
                            gif_path = tmpfile.name
                        try:
                            create_gif(frames, gif_path)
                            st.image(gif_path)
                            st.success(f"GIF created successfully with {len(frames)} frames.")
                        except Exception as e:
                            st.error(f"Error creating GIF: {str(e)}")
                
        else:
            if st.button("Record Voice"):
                with st.spinner("Recording..."):
                    store = sr.Recognizer()
                    with sr.Microphone() as s:
                        audio_input = store.record(s, duration=5)
                        try:
                            text_output = store.recognize_google(audio_input)
                            st.success(f"Recognized: {text_output}")
                            
                            with st.spinner("Generating GIF..."):
                                frames = func(text_output)
                                
                                if not frames:
                                    st.error("No frames generated. Please try a different input.")
                                else:
                                    # Create and display GIF
                                    with tempfile.NamedTemporaryFile(delete=False, suffix='.gif') as tmpfile:
                                        gif_path = tmpfile.name
                                    try:
                                        create_gif(frames, gif_path)
                                        st.image(gif_path)
                                        st.success(f"GIF created successfully with {len(frames)} frames.")
                                    except Exception as e:
                                        st.error(f"Error creating GIF: {str(e)}")
                        except:
                            st.error("Error Hearing Voice")

    elif choice == "Sign to Voice":
        st.header("Sign to Voice")
        st.write("Click here for ISL to English")
        if st.button("Click Here"):
            from ISL_to_English.app import app
            app()

if __name__ == "__main__":
    main()
