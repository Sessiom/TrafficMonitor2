# Smart Portable Traffic Signal System For Single Lane Roadside Construction​
This is part of my teams Senior Design Project in which we are building two street signs for 
single-lane roadside construction that communicate which each other much like traffic flaggers.
In addition to a website, this repository has the esp32 code, espCam code for each sign and the object detection code.
The webpage displays data from an esp32 using ble (bluetooth low energy). 
It builds off of [sessiom.github.io/trafficMonitor](sessiom.github.io/trafficMonitor).
The data from each session is then saved to mongoDB. 
# Below is the live stream from the espCam after object detection is done and a bounding box is added.
![Car Detection](https://github.com/Sessiom/Smart-Portable-Traffic-Signal-System-For-Single-Lane-Roadside-Construction/blob/master/readMeImages/carDetection.PNG)
# Next is the Live Home View.
![Home View](https://github.com/Sessiom/Smart-Portable-Traffic-Signal-System-For-Single-Lane-Roadside-Construction/blob/master/readMeImages/trafficMonitor.PNG)
# Next is the History View
![History View](https://github.com/Sessiom/Smart-Portable-Traffic-Signal-System-For-Single-Lane-Roadside-Construction/blob/master/readMeImages/historyTab.PNG)
