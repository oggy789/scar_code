import cv2
import numpy as np
import urllib.request
import os
import webbrowser

# Function to download files
def download_file(url, filename):
    if not os.path.exists(filename):
        print(f"Downloading {filename}...")
        urllib.request.urlretrieve(url, filename)
        print(f"Downloaded {filename}")
    else:
        print(f"{filename} already exists. Skipping download.")

# URLs for the YOLO model files
coco_url = "https://raw.githubusercontent.com/pjreddie/darknet/master/data/coco.names"
cfg_url = "https://raw.githubusercontent.com/pjreddie/darknet/master/cfg/yolov3.cfg"
weights_url = "https://pjreddie.com/media/files/yolov3.weights"

# File paths
labels_path = "coco.names"
config_path = "yolov3.cfg"
weights_path = "yolov3.weights"

# Download necessary files
download_file(coco_url, labels_path)
download_file(cfg_url, config_path)
download_file(weights_url, weights_path)

# Load the COCO class labels that YOLO model was trained on
LABELS = open(labels_path).read().strip().split("\n")

# Load the YOLO object detector trained on COCO dataset (80 classes)
net = cv2.dnn.readNetFromDarknet(config_path, weights_path)

# Initialize the video capture
cap = cv2.VideoCapture(0)

def search_google(query):
    search_url = f"https://www.google.com/search?q={query}"
    webbrowser.open(search_url)

# Loop over the frames from the video stream
while True:
    ret, frame = cap.read()
    if not ret:
        break

    # Get spatial dimensions of the frame
    (H, W) = frame.shape[:2]

    # Create a blob from the input frame and perform a forward pass of YOLO
    blob = cv2.dnn.blobFromImage(frame, 1 / 255.0, (416, 416), swapRB=True, crop=False)
    net.setInput(blob)
    layer_names = net.getLayerNames()
    layer_names = [layer_names[i - 1] for i in net.getUnconnectedOutLayers()]
    detections = net.forward(layer_names)

    # Initialize lists to hold detection information
    boxes = []
    confidences = []
    class_ids = []

    # Loop over detections
    for output in detections:
        for detection in output:
            scores = detection[5:]
            class_id = np.argmax(scores)
            confidence = scores[class_id]

            if confidence > 0.5:
                box = detection[0:4] * np.array([W, H, W, H])
                (centerX, centerY, width, height) = box.astype("int")
                x = int(centerX - (width / 2))
                y = int(centerY - (height / 2))
                boxes.append([x, y, int(width), int(height)])
                confidences.append(float(confidence))
                class_ids.append(class_id)

    # Apply non-maxima suppression to suppress weak, overlapping bounding boxes
    idxs = cv2.dnn.NMSBoxes(boxes, confidences, 0.5, 0.3)

    # Ensure at least one detection exists
    if len(idxs) > 0:
        for i in idxs.flatten():
            (x, y) = (boxes[i][0], boxes[i][1])
            (w, h) = (boxes[i][2], boxes[i][3])
            color = [0, 255, 0]
            cv2.rectangle(frame, (x, y), (x + w, y + h), color, 2)
            text = "{}: {:.4f}".format(LABELS[class_ids[i]], confidences[i])
            cv2.putText(frame, text, (x, y - 5), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)

            # Print object label and confidence
            print(f"Detected: {LABELS[class_ids[i]]} with confidence {confidences[i]:.4f}")

            # Trigger Google search
            search_google(LABELS[class_ids[i]])

    # Show the output frame
    cv2.imshow("Frame", frame)

    # Break the loop if 'q' is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the video capture object and close all OpenCV windows
cap.release()
cv2.destroyAllWindows()
