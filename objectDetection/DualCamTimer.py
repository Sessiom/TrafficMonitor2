import multiprocessing
from ultralytics import YOLO
import cv2
import cvzone
import math
import urllib.request
import numpy as np
import requests
import time

# Replace with the IP address of your ESP32 devices
esp32_ips = ['192.168.8.230', '192.168.8.227']  

# Class names
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

def process_camera(esp32_ip):
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

    model = YOLO("yolov8m.pt")
    mask = cv2.imread("images/espCam1Mask.png")

    prev_message_str = None
    message_str = None

    car_detected = False
    car_detected_time = None
    no_car_detect_time = None

    while True:
        img_resp = urllib.request.urlopen(stream_url)

        imgnp = np.array(bytearray(img_resp.read()), dtype=np.uint8)
        img = cv2.imdecode(imgnp,-1)
        cv2.line(img, (400, 0), (400, 600), (0, 255, 0), 2)
        imgRegion = cv2.bitwise_and(img, mask)

        results = model(imgRegion, stream=True)
        for r in results:
            boxes = r.boxes
            for box in boxes:
                x1,y1,x2,y2 = box.xyxy[0]
                x1,y1,x2,y2 = int(x1), int(y1), int(x2), int(y2)
                w, h = x2-x1, y2-y1
                conf = math.ceil((box.conf[0] *100))/100   #round confidence to 2 decimal places
                cls = int(box.cls[0])
                currentClass = classNames[cls]

                if (currentClass == "car" or currentClass == 'truck' or currentClass == 'motorcycle' or currentClass == 'bus') and conf > 0.3:
                    cvzone.putTextRect(img, f'{currentClass} {conf}', (max(0, x1), max(35, y1)), 3, 3, (255,255,255), (0,255,0))
                    cvzone.cornerRect(img, (x1,y1,w,h), 30, 5, 1, (0, 255, 0), (0, 255, 0))
                    car_detected = True
                    if car_detected_time is None:
                        car_detected_time = time.time()
                    elif time.time() - car_detected_time >= 1:
                        message_str = "T"
                        print(message_str)
                        car_detected_time = None  # reset the timer
                        no_car_detected_time = None  # reset the no car detected timer

        if not car_detected:
            if no_car_detected_time is None:
                no_car_detected_time = time.time()
            elif time.time() - no_car_detected_time >= 1:
                message_str = "F"
                print(message_str)
                no_car_detected_time = None  # reset the timer
                car_detected_time = None  # reset the car detected timer

        if message_str != prev_message_str:
            data = {"value": message_str}
            response = requests.post(url, data=data)
            if response.status_code == 200:
                print("Message sent successfully.")
            else:
                print(f"Failed to send message. Status code: {response.status_code}")
            prev_message_str = message_str

        car_detected = False

        cv2.imshow("Image", img)
        cv2.waitKey(1)

if __name__ == "__main__":
    processes = []
    for ip in esp32_ips:
        p = multiprocessing.Process(target=process_camera, args=(ip,))
        p.start()
        processes.append(p)

    for p in processes:
        p.join()