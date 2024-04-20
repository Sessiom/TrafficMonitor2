import threading
from ultralytics import YOLO
import cv2
import cvzone
import math
import urllib.request
import numpy as np
import requests
from http.client import IncompleteRead
from threading import Thread



# Replace with the IP address of your ESP32 device
esp32_ip1 = '192.168.8.227'
esp32_ip2 = '192.168.8.230'

# URL for the WebServer
url1 = f"http://{esp32_ip1}:81/"
url2 = f"http://{esp32_ip2}:81/"

# URL for the AsyncWebServer
stream_url1 = f"http://{esp32_ip1}:80/cam-hi.jpg"
stream_url2 = f"http://{esp32_ip2}:80/cam-hi.jpg"

# Create a VideoCapture object
cap1 = cv2.VideoCapture(stream_url1)
cap2 = cv2.VideoCapture(stream_url2)

# Check if the IP camera stream is opened successfully
if not cap1.isOpened():
    print("Failed to open the IP camera stream")
    exit()
if not cap2.isOpened():
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

prev_message_str = None

car_detected = False
mask = cv2.imread("images/espCamMask.png")

def send_post_request(url, data):
    try:
        requests.post(url, data=data)
    except requests.exceptions.RequestException as e:
        print(f"Failed to send POST request: {e}")

def run_detection1():
    global cap, model, classNames, prev_message_str, car_detected
    while True:
        img_resp = urllib.request.urlopen(stream_url1)

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

                # Display the resulting frame
                cv2.imshow('Frame1', img)

                # Break the loop on 'q' key press
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break

        if not car_detected:
            message_str = "F"

        if message_str != prev_message_str:
            data = {"value": message_str}
            Thread(target=send_post_request, args=(url1, data)).start()
            prev_message_str = message_str

        car_detected = False

def run_detection2():
    global cap, model, classNames, prev_message_str, car_detected
    while True:
        img_resp = urllib.request.urlopen(stream_url2)

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

                # Display the resulting frame
                cv2.imshow('Frame2', img)

                # Break the loop on 'q' key press
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break

        if not car_detected:
            message_str = "F"

        if message_str != prev_message_str:
            data = {"value": message_str}
            Thread(target=send_post_request, args=(url2, data)).start()
            prev_message_str = message_str

        car_detected = False

if __name__ == '__main__':
    # Run the detection functions in separate threads
    p1 = threading.Thread(target=run_detection1)       #Process(target=run_detection1)
    p2 = threading.Thread(target=run_detection2)       #Process(target=run_detection2)
    p1.start()
    p2.start()
    p1.join()
    p2.join()