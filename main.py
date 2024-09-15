import tkinter as tk
import tensorflow
from tkinter import Label, Text, Button
import numpy as np
import cv2
import os
from PIL import Image, ImageTk
import speech_recognition as sr
from tensorflow.keras.models import load_model

# Define image dimensions and paths
image_x, image_y = 64, 64
model_path = 'model.h5'
op_dest = "filtered_data"
alpha_dest ="alphabet"

# Load the model
classifier = load_model(model_path, compile=False)

def give_char():
    from tensorflow.keras.preprocessing import image
    test_image = image.load_img('tmp1.png', target_size=(64, 64))
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

# Prepare file map
dirListing = os.listdir(op_dest)
editFiles = [item for item in dirListing if ".webp" in item]
file_map = {i: i.replace(".webp", "").split() for i in editFiles}

def func(a):
    all_frames = []
    final = Image.new('RGB', (380, 260))
    words = a.split()
    for i in words:
        flag, sim = check_sim(i, file_map)
        if flag == -1:
            for j in i:
                im = Image.open(os.path.join(alpha_dest, f"{j.lower()}_small.gif"))
                frameCnt = im.n_frames
                for frame_cnt in range(frameCnt):
                    im.seek(frame_cnt)
                    im.save("tmp.png")
                    img = cv2.imread("tmp.png")
                    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
                    img = cv2.resize(img, (380, 260))
                    im_arr = Image.fromarray(img)
                    all_frames.extend([im_arr] * 15)
        else:
            im = Image.open(os.path.join(op_dest, sim))
            im.info.pop('background', None)
            im.save('tmp.gif', 'gif', save_all=True)
            im = Image.open("tmp.gif")
            frameCnt = im.n_frames
            for frame_cnt in range(frameCnt):
                im.seek(frame_cnt)
                im.save("tmp.png")
                img = cv2.imread("tmp.png")
                img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
                img = cv2.resize(img, (380, 260))
                im_arr = Image.fromarray(img)
                all_frames.append(im_arr)
    final.save("out.gif", save_all=True, append_images=all_frames, duration=100, loop=0)
    return all_frames

class Tk_Manage(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)
        self.frames = {}
        for F in (StartPage, VtoS, StoV):
            frame = F(container, self)
            self.frames[F] = frame
            frame.grid(row=0, column=0, sticky="nsew")
        self.show_frame(StartPage)

    def show_frame(self, cont):
        frame = self.frames[cont]
        frame.tkraise()

class StartPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text="Two Way Sign Language Translator", font=("Verdana", 12))
        label.pack(pady=10, padx=10)
        button = tk.Button(self, text="Voice to Sign", command=lambda: controller.show_frame(VtoS))
        button.pack()
        button2 = tk.Button(self, text="Sign to Voice", command=lambda: controller.show_frame(StoV))
        button2.pack()
        load = Image.open("Two Way Sign Language Translator.png")
        load = load.resize((620, 450))
        render = ImageTk.PhotoImage(load)
        img = Label(self, image=render)
        img.image = render
        img.place(x=100, y=200)

class VtoS(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.cnt = 0
        self.gif_frames = []
        self.inputtxt = None
        label = tk.Label(self, text="Voice to Sign", font=("Verdana", 12))
        label.pack(pady=10, padx=10)
        gif_box = tk.Label(self)
        button1 = tk.Button(self, text="Back to Home", command=lambda: controller.show_frame(StartPage))
        button1.pack()
        button2 = tk.Button(self, text="Sign to Voice", command=lambda: controller.show_frame(StoV))
        button2.pack()

        def gif_stream():
            if self.cnt >= len(self.gif_frames):
                return
            img = self.gif_frames[self.cnt]
            self.cnt += 1
            imgtk = ImageTk.PhotoImage(image=img)
            gif_box.imgtk = imgtk
            gif_box.configure(image=imgtk)
            gif_box.after(50, gif_stream)

        def hear_voice():
            store = sr.Recognizer()
            with sr.Microphone() as s:
                audio_input = store.record(s, duration=10)
                try:
                    text_output = store.recognize_google(audio_input)
                    self.inputtxt.insert(tk.END, text_output)
                except:
                    print("Error Hearing Voice")
                    self.inputtxt.insert(tk.END, '')

        def take_input():
            INPUT = self.inputtxt.get("1.0", "end-1c")
            print(INPUT)
            self.gif_frames = func(INPUT)
            self.cnt = 0
            gif_stream()
            gif_box.place(x=400, y=160)

        l = tk.Label(self, text="Enter Text or Voice:")
        l1 = tk.Label(self, text="OR")
        self.inputtxt = tk.Text(self, height=4, width=25)
        voice_button = tk.Button(self, height=2, width=20, text="Record Voice", command=hear_voice)
        voice_button.place(x=50, y=180)
        display = tk.Button(self, height=2, width=20, text="Convert", command=take_input)
        l.place(x=50, y=160)
        l1.place(x=115, y=230)
        self.inputtxt.place(x=50, y=250)
        display.pack()

class StoV(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text="Sign to Voice", font=("Verdana", 12))
        label.pack(pady=10, padx=10)
        button1 = tk.Button(self, text="Back to Home", command=lambda: controller.show_frame(StartPage))
        button1.pack()
        button2 = tk.Button(self, text="Voice to Sign", command=lambda: controller.show_frame(VtoS))
        button2.pack()
        disp_txt = tk.Text(self, height=4, width=25)

        def start_video():
            video_frame = tk.Label(self)
            cam = cv2.VideoCapture(0)
            self.img_counter = 0
            self.img_text = ''

            def video_stream():
                if self.img_counter > 200:
                    return
                self.img_counter += 1
                ret, frame = cam.read()
                frame = cv2.flip(frame, 1)
                img = cv2.rectangle(frame, (425, 100), (625, 300), (0, 255, 0), thickness=2)
                lower_blue = np.array([35, 10, 0])
                upper_blue = np.array([160, 230, 255])
                imcrop = img[102:298, 427:623]
                hsv = cv2.cvtColor(imcrop, cv2.COLOR_BGR2HSV)
                mask = cv2.inRange(hsv, lower_blue, upper_blue)
                cv2.putText(frame, self.img_text, (30, 400), cv2.FONT_HERSHEY_TRIPLEX, 1.5, (0, 255, 0))
                img_name = "tmp1.png"
                save_img = cv2.resize(mask, (image_x, image_y))
                cv2.imwrite(img_name, save_img)
                tmp_text = self.img_text[:]
                self.img_text = give_char()
                if tmp_text != self.img_text:
                    print(tmp_text)
                    disp_txt.insert(tk.END, tmp_text)
                img = Image.fromarray(frame)
                imgtk = ImageTk.PhotoImage(image=img)
                video_frame.imgtk = imgtk
                video_frame.configure(image=imgtk)
                video_frame.after(1, video_stream)

            video_stream()
            disp_txt.pack()
            video_frame.pack()

        start_vid = tk.Button(self, height=2, width=20, text="Start Video", command=start_video)
        start_vid.pack()

if __name__ == "__main__":
    app = Tk_Manage()
    app.geometry("800x750")
    app.mainloop()