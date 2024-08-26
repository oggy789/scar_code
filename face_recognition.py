import face_recognition
import cv2
import numpy as np
import os
import pyttsx3
import tkinter as tk
from tkinter import messagebox

# Initialize text-to-speech engine
engine = pyttsx3.init()

# Load a sample picture and learn how to recognize it.
known_face_encodings = []
known_face_names = []

# Load sample images and get encodings
def load_known_faces():
    image_files = ['saved_face1.jpg', 'saved_face2.jpg']  # Add all your saved faces here
    names = ['Person1', 'Person2']  # Corresponding names for the images

    for image_file, name in zip(image_files, names):
        image = face_recognition.load_image_file(image_file)
        encoding = face_recognition.face_encodings(image)[0]
        known_face_encodings.append(encoding)
        known_face_names.append(name)

def start_jarvis(name):
    engine.say(f"Hello, {name}. Jarvis activated.")
    engine.runAndWait()
    # Example: Open Notepad or any application
    os.system("notepad.exe")

def recognize_faces():
    video_capture = cv2.VideoCapture(0)  # Initialize webcam

    while True:
        # Grab a single frame of video
        ret, frame = video_capture.read()

        # Resize frame for faster processing
        small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)
        rgb_small_frame = small_frame[:, :, ::-1]

        # Find all the faces and face encodings in the frame
        face_locations = face_recognition.face_locations(rgb_small_frame)
        face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)

        for face_encoding in face_encodings:
            matches = face_recognition.compare_faces(known_face_encodings, face_encoding)
            name = "Unknown"

            # If a match was found in known_face_encodings, use the first one.
            face_distances = face_recognition.face_distance(known_face_encodings, face_encoding)
            best_match_index = np.argmin(face_distances)
            if matches[best_match_index]:
                name = known_face_names[best_match_index]

            if name != "Unknown":
                start_jarvis(name)
                video_capture.release()
                cv2.destroyAllWindows()
                return  # Exit the function after recognizing

        # Display the resulting image
        cv2.imshow('Video', frame)

        # Hit 'q' on the keyboard to quit!
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # Release handle to the webcam
    video_capture.release()
    cv2.destroyAllWindows()

def on_button_click():
    recognize_faces()

# Load known faces initially
load_known_faces()

# Setup GUI using tkinter
root = tk.Tk()
root.title("Face Recognition Tool")

frame = tk.Frame(root)
frame.pack()

recognize_button = tk.Button(frame, text="Start Face Recognition", command=on_button_click)
recognize_button.pack(side=tk.LEFT)

quit_button = tk.Button(frame, text="QUIT", fg="red", command=quit)
quit_button.pack(side=tk.LEFT)

root.mainloop()
