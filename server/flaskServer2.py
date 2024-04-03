from flask import Flask, Response
import threading
from ultralytics import YOLO
import cv2
import cvzone
import math
import urllib.request
import numpy as np
import requests
from http.client import IncompleteRead
#from dotenv import load_dotenv
#import os

#load_dotenv()

app = Flask(__name__)

# Replace with the IP address of your ESP32 device
#esp32_ip = os.getenv('CAMERA2_URL')  
esp32_ip = '192.168.8.227'
# URL for the WebServer
url = f"http://{esp32_ip}:81/"

# URL for the AsyncWebServer
stream_url = f"http://{esp32_ip}:80/cam-hi.jpg"


# Create a VideoCapture object
cap = cv2.VideoCapture(stream_url)

# Check if the IP camera stream is opened successfully
if not cap.isOpened():
    print("Failed to open the IP camera stream")
    exit()

model = YOLO("yolov8l.pt")

classNames = ["person", "bicycle", "car", "motorcycle", "airplane", "bus", "train", "truck", 
              "boat", "traffic light", "fire hydrant", "stop sign", "parking meter", "bench", "bird", "cat",
              "dog", "horse", "sheep", "cow", "elephant", "bear", "zebra", "giraffe", "backpack", "umbrella",
              "handbag", "tie", "suitcase", "frisbee", "skis", "snowboard", "sports ball", "kite", "baseball bat",
              "baseball glove", "skateboard", "surfboard", "tennis racket", "bottle", "wine glass", "cup", "fork",
              "knife", "spoon", "bowl", "banana", "apple", "sandwich", "orange", "broccoli", "carrot", "hot dog",
              "pizza", "donut", "cake", "chair", "couch", "potted plant", "bed", "dining table", "toilet", "tv",
              "laptop", "mouse", "remote", "keyboard", "cell phone", "microwave", "oven", "toaster", "sink",
              "refrigerator", "book", "clock", "vase", "scissors", "teddy bear", "hair drier", "toothbrush",
             ]
mask = cv2.imread("server/images/espCam1Mask.png")
prev_message_str = None

car_detected = False

def run_detection():
    global cap, model, classNames, prev_message_str, car_detected
    while True:
        img_resp = urllib.request.urlopen(stream_url)

        try:
            imgnp = np.array(bytearray(img_resp.read()), dtype=np.uint8)
        except IncompleteRead as e:
            imgnp = np.array(bytearray(e.partial), dtype=np.uint8)

        img = cv2.imdecode(imgnp,-1)
        cv2.line(img, (400, 0), (400, 600), (0, 255, 0), 2)
        imgRegion = cv2.bitwise_and(img, mask)

        results = model(imgRegion, stream=True)
        for r in results:
            boxes = r.boxes
            for box in boxes:

                # Bounding Box
                x1,y1,x2,y2 = box.xyxy[0]
                x1,y1,x2,y2 = int(x1), int(y1), int(x2), int(y2)

                w, h = x2-x1, y2-y1

                # Confidence
                conf = math.ceil((box.conf[0] *100))/100   #round confidence to 2 decimal places

                # Class Name
                cls = int(box.cls[0])
                currentClass = classNames[cls]

                # Draw only vehicles
                if currentClass == "car" and conf > 0.3:
                    cvzone.putTextRect(img, f'{currentClass} {conf}', (max(0, x1), max(35, y1)), 3, 3, (255,255,255), (0,255,0))
                    cvzone.cornerRect(img, (x1,y1,w,h), 30, 5, 1, (0, 255, 0), (0, 255, 0))
                    message_str = "T"
                    car_detected = True

        # Convert the image to JPEG
        ret, jpeg = cv2.imencode('.jpg', img)
        frame = jpeg.tobytes()

        # Yield the frame to the client
        yield (b'--frame\r\n'
            b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')

        if not car_detected:
            message_str = "F"

        if message_str != prev_message_str:
            data = {"value": message_str}
            response = requests.post(url, data=data)
            prev_message_str = message_str

        car_detected = False

@app.route('/video_feed')
def index():
    return Response(run_detection(), mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == '__main__':
    t = threading.Thread(target=run_detection)
    t.start()
    app.run(host='0.0.0.0', port=5002)  # Run the server on port 6000