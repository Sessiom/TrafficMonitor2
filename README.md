# Smart Portable Traffic Signal System For Single Lane Roadside Construction​
This is part of my teams Senior Design Project in which we are building two street signs for 
single-lane roadside construction that communicate which each other much like traffic flaggers.
In addition to a website, this repository has the esp32 code, espCam code for each sign and the object detection code.
The webpage displays data from an esp32 using ble (bluetooth low energy). 
It builds off of [sessiom.github.io/trafficMonitor](sessiom.github.io/trafficMonitor).
The data from each session is then saved to mongoDB. 
## References
-  ESP-NOW: https://randomnerdtutorials.com/esp-now-esp32-arduino-ide/
-  Ble: https://randomnerdtutorials.com/esp32-web-bluetooth/
-  Object Detection: https://www.youtube.com/watch?v=WgPbbWmnXJ8& 
-  Vue Full Stack: https://www.youtube.com/watch?v=j55fHUJqtyw&, https://www.youtube.com/watch?v=X-JZ-QPApUs


# Below is the live stream from the espCam after object detection is done and a bounding box is added.
![Car Detection](https://github.com/Sessiom/Smart-Portable-Traffic-Signal-System-For-Single-Lane-Roadside-Construction/blob/master/readMeImages/carDetection.PNG)
# Next is the Live Home View.
![Home View](https://github.com/Sessiom/Smart-Portable-Traffic-Signal-System-For-Single-Lane-Roadside-Construction/blob/master/readMeImages/trafficMonitor.PNG)
# Next is the History View
![History View](https://github.com/Sessiom/Smart-Portable-Traffic-Signal-System-For-Single-Lane-Roadside-Construction/blob/master/readMeImages/historyTab.PNG)
