<template>
    <div class="content">

        <div class="notification" v-if ="this.bleState == 'Connected'"> 
            <p><i class="fas fa-wifi fa-rotate-270"></i><i class="fas fa-wifi fa-rotate-90" style="position: relative; left: -10px;"></i>Live</p >
        </div>

        <div class="card-grid">
            <div class="card">
                <p>
                    <button class="connectButton" @click="connectButton"> Connect </button>
                    <button class="disconnectButton" @click="disconnectDevice"> Disconnect </button>
                </p>
                <p class="gray-label">Device state: <strong><span :style="{ color: bleState === 'Connected' ? '#24af37' : '#d13a30' }">{{ bleState }}</span></strong></p>
            </div>
        </div>

        <div class="card-grid">
            <div class="card">
                <h2>Stop-Stop Override</h2>
                <button id="onButton" class="onButton" @click="onButton">ON</button>
                <button id="offButton" class="offButton" @click="offButton">OFF</button>
                <p class="gray-label">Last value sent: <span id="valueSent">{{ latestValueSent }}</span></p>
            </div>
        </div>

        <!-- <div class="card-grid">
            <div class="card">
                <h2>Stream 1</h2>
                <img class="stream" :src="stream1Url" v-if="stream1Playing" />
                <button class="streamButton" @click="toggleStream1">{{ stream1Playing ? 'Stop Stream' : 'Start Stream' }}</button>
                </div>

                <div class="card">
                <h2>Stream 2</h2>
                <img class="stream" :src="stream2Url" v-if="stream2Playing" />
                <button class="streamButton" @click="toggleStream2">{{ stream2Playing ? 'Stop Stream' : 'Start Stream' }}</button>
            </div>
        </div> -->

        <div class="card-grid">
            <div class="card">
                <h2>Sign 1</h2>
                <!-- <p class="reading"><span id="valueContainer1">{{ retrievedValue }}</span></p> -->
                <img :src="imageSourceRetrieved" class="my-image"/>
                <i class="fas fa-car-on" :class="carColor"></i>
                
                <p class="gray-label">Last reading: <span class="timestamp">{{ timestampContainers[0] }}</span></p>
            </div>

            <div class="card">
                <h2>Sign 2 </h2>
                <!-- <p class="reading"><span id="valueContainer2">{{ secondValue }}</span></p>-->
                <img :src="imageSourceSecond" class="my-image"/>
                <i class="fas fa-car-on" :class="carColor2"></i>
                <p class="gray-label">Last reading: <span class="timestamp">{{ timestampContainers[0] }}</span></p>
            </div>

        </div>

        <div class="card-grid">
            <div class="card">
                <h2>Cars In Lane</h2>
                <p class="reading"><span id="valueContainer3">{{ thirdValue }}</span></p>
                <p class="gray-label">Last reading: <span class="timestamp">{{ timestampContainers[0] }}</span></p>
            </div>
        </div>

        <div class="card-grid">
            <div class="card">
                <h2>Car Counts</h2>
                <p class="reading"><span>Sign 1: </span><span id="valueContainer4">{{ fourthValue }}</span></p>
                <p class="reading"><span>Sign 2: </span><span id="valueContainer5">{{ fifthValue }}</span></p>
                <p class="reading"><span>Total: </span><span>{{ total }}</span></p>
                <p class="gray-label">Last reading: <span class="timestamp">{{ timestampContainers[0] }}</span></p>
            </div>
        </div>

    </div>
    <div class="footer">
        <p></p>
        <p></p>
    </div>
</template>

<script>
import PostService from '../PostService';
import { useToast } from 'vue-toastification';
const toast = useToast();

export default {
  data() {
    return {
      stream1Url: 'http://localhost:5004/video_feed',
      stream2Url: 'http://localhost:5002/video_feed',
      stream1Playing: false,
      stream2Playing: false,

      deviceName: 'ESP32',
      bleService: '6c744422-08a1-40c7-807a-576b64b52437',
      characteristics: [       
      'de420cdd-4085-4066-8ee7-a6c5e28316d5',      // Red characteristic
      '2bd7866c-14ca-4191-a09f-c4985352cc96',      // Sign1 characteristic
      'dc51766b-fe18-4d8f-bb31-d49e82e59e18',      // Sign2 characteristic
      'c28e246d-5632-44d7-8fdb-124f4243eb10',      // CarsInLane characteristic
      '65037f44-f9f5-48a4-8205-e9d3dc574316',      // Sign1count characteristic
      '55a12381-bb3c-4731-9cde-99fcbc13fca2',      // Sign2count characteristic
      'd9001af2-630c-4a44-ad33-2520d5fc93ff',      // carWaitingLeft characteristic
      '0d044a6c-fdf5-485f-b0f0-55c8d9f3854a'       // carWaitingRight characteristic
      ],
      bleServer: null,
      bleServiceFound: null,
      sensorCharacteristicFound: null,
      latestValueSent: '',
      retrievedValue: 'SLOW',   // Sign 1
      secondValue: 'STOP',      // Sign 2
      thirdValue: '0',          // Cars in lane
      fourthValue: '0',         // Sign 1 count
      fifthValue: '0',          // Sign 2 count
      sixthValue: 0,            // Sign 1 car waiting
      seventhValue: 0,          // Sign 2 car waiting
      isOverride: false,
      startTime: null,
      endTime: null,
      displayTotalTime: null,
      location: '',
      sign1: 0,
      sign2: 0,
      total: 0,
      bleState: 'Disconnected',
      timestampContainers: ['', '', '']
    };
  },
  computed: {
    calculatedTotal() {
      let sign1 = parseInt(this.fourthValue, 10); 
      let sign2 = parseInt(this.fifthValue, 10);
      return sign1 + sign2;
    },
    duration() {
        if (this.startTime && this.endTime) {
        const durationMs = this.endTime - this.startTime; // duration in milliseconds
        const durationSec = Math.floor(durationMs / 1000); // convert to seconds
        const hours = Math.floor(durationSec / 3600);
        const minutes = Math.floor((durationSec % 3600) / 60);
        const seconds = durationSec % 60;
        return `${hours.toString().padStart(2, '0')}:${minutes.toString().padStart(2, '0')}:${seconds.toString().padStart(2, '0')}`;
        }
      return '00:00:00';
    },
    imageSourceSecond() {
      if (this.secondValue === 'STOP') {
        return require('@/assets/stop.png');
      } else if (this.secondValue === 'SLOW') {
        return require('@/assets/slow.png');
      }
      return '';
    },
    imageSourceRetrieved() {
      if (this.retrievedValue === 'STOP') {
        return require('@/assets/stop.png');
      } else if (this.retrievedValue === 'SLOW') {
        return require('@/assets/slow.png');
      }
      return '';
    },
    carColor() {
      return this.sixthValue === 1 ? 'blue' : 'lightgray';
    },
    carColor2() {
      return this.seventhValue === 1 ? 'blue' : 'lightgray';
    }
  },
  watch: {
    calculatedTotal(newTotal) {
        this.total = newTotal;
    },
    duration(newDuration) {
        this.displayTotalTime = newDuration;
    }
  },
  methods: {
    toggleStream1() {
        if (this.stream1Playing) {
            this.stream1Url = null; // This will stop loading the image
        } else {
            this.stream1Url = 'http://localhost:5004/video_feed'; // Replace with your actual stream URL
        }
        this.stream1Playing = !this.stream1Playing;
    },
    toggleStream2() {
        if (this.stream2Playing) {
            this.stream2Url = null; // This will stop loading the image
        } else {
            this.stream2Url = 'http://localhost:5002/video_feed'; // Replace with your actual stream URL
        }
        this.stream2Playing = !this.stream2Playing;
    },
    connectButton() {
      if (this.isWebBluetoothEnabled()) {
        this.connectToDevice();
      }
    },
    isWebBluetoothEnabled() {
        if (!navigator.bluetooth) {
            toast.error('Web Bluetooth API is not available in this browser/device');
            console.log('Web Bluetooth API is not available in this browser');
            this.bleState = "Web Bluetooth API is not available in this browser/device";
            return false;
        }
        console.log('Web Bluetooth API supported in this browser.');
        return true;
    },
    connectToDevice() {
        console.log('Initializing Bluetooth...');
        navigator.bluetooth.requestDevice({
            filters: [{ name: this.deviceName }],
            optionalServices: [this.bleService]
        })
        .then(device => {
            console.log('Device Selected:', device.name);
            this.bleState = 'Connected'// to device ' + device.name;
            this.startTime = new Date();
            this.location = "1 Hawk Dr, New Paltz, NY 12561";
            device.addEventListener('gattserverdisconnected', this.onDisconnected);
            return device.gatt.connect();
        })
        .then(gattServer => {
            this.bleServer = gattServer;
            console.log("Connected to GATT Server");
            return this.bleServer.getPrimaryService(this.bleService);
        })
        .then(service => {
            this.bleServiceFound = service;
            console.log("Service discovered:", service.uuid);
            return Promise.all(this.characteristics.map(uuid => service.getCharacteristic(uuid)))
        })
        .then(characteristics => {
            // Save the characteristics for later use
            this.characteristicsFound = characteristics;
            console.log("led Characteristic discovered:", characteristics[0].uuid);
            console.log("sensor Characteristic discovered:", characteristics[1].uuid);
            console.log("second Characteristic discovered:", characteristics[2].uuid);
            console.log("third Characteristic discovered:", characteristics[3].uuid);
            console.log("fourth Characteristic discovered:", characteristics[4].uuid);
            console.log("fifth Characteristic discovered:", characteristics[5].uuid);
            console.log("sixth Characteristic discovered:", characteristics[6].uuid);
            console.log("seventh Characteristic discovered:", characteristics[7].uuid);
            // Now you can read or write the values of the characteristics as needed
            // For example, to read the values:
            const sensorCharacteristic = characteristics[1];
            const secondCharacteristic = characteristics[2];
            const thirdCharacteristic = characteristics[3];
            const fourthCharacteristic = characteristics[4];
            const fifthCharacteristic = characteristics[5];
            const sixthCharacteristic = characteristics[6];
            const seventhCharacteristic = characteristics[7];

            sensorCharacteristic.addEventListener('characteristicvaluechanged', this.handleCharacteristicValueChanged);
            secondCharacteristic.addEventListener('characteristicvaluechanged', this.handleCharacteristicValueChanged);
            thirdCharacteristic.addEventListener('characteristicvaluechanged', this.handleCharacteristicValueChanged);
            fourthCharacteristic.addEventListener('characteristicvaluechanged', this.handleCharacteristicValueChanged);
            fifthCharacteristic.addEventListener('characteristicvaluechanged', this.handleCharacteristicValueChanged);
            sixthCharacteristic.addEventListener('characteristicvaluechanged', this.handleCharacteristicValueChanged);
            seventhCharacteristic.addEventListener('characteristicvaluechanged', this.handleCharacteristicValueChanged);

            sensorCharacteristic.startNotifications();
            secondCharacteristic.startNotifications();
            thirdCharacteristic.startNotifications();
            fourthCharacteristic.startNotifications();
            fifthCharacteristic.startNotifications();
            sixthCharacteristic.startNotifications();
            seventhCharacteristic.startNotifications();

            console.log("Notifications started for Sensor Characteristic");
            console.log("Notifications started for Second Characteristic");
            console.log("Notifications started for Third Characteristic");
            console.log("Notifications started for Fourth Characteristic");
            console.log("Notifications started for Fifth Characteristic");
            console.log("Notifications started for Sixth Characteristic");
            console.log("Notifications started for Seventh Characteristic");
            //return characteristics[1].readValue();
        })
        /*.then(values => {
            // Process the values here
            console.log("Read value: ", values);
            const decodedValue = new TextDecoder().decode(values);
            console.log("Decoded value: ", decodedValue);
            this.retrievedValue = decodedValue;
        })*/
        .catch(error => {
            console.error("Error:", error);
        })
    },
    handleCharacteristicValueChanged(event) {
        const characteristic = event.target;
        const value = new TextDecoder().decode(characteristic.value);
        console.log(`Value of characteristic ${characteristic.uuid}:`, value);

        if (characteristic.uuid === this.characteristicsFound[1].uuid) {
            if(this.isOverride === true){
                this.retrievedValue = 'STOP'
            }
            else{
                if(value === "1"){
                    this.retrievedValue = "SLOW"
                }
                else{
                    this.retrievedValue = "STOP"
                }
            }
        } else if (characteristic.uuid === this.characteristicsFound[2].uuid) {
            if(this.isOverride === true){
                this.secondValue = 'STOP';
            }
            else{
                if(value === "1"){
                    this.secondValue = "SLOW"
                }
                else{
                    this.secondValue = "STOP"
                }
            }
        }
        else if (characteristic.uuid === this.characteristicsFound[3].uuid) {
            if(this.isOverride === true){
                this.thirdValue = '0';
            }
            else{
                this.thirdValue = value;
            }
        }
        else if (characteristic.uuid === this.characteristicsFound[4].uuid) {
            this.fourthValue = value;
            this.sign1 = parseInt(this.fourthValue, 10);
        }
        else if (characteristic.uuid === this.characteristicsFound[5].uuid) {
            this.fifthValue = value;
            this.sign2 = parseInt(this.fifthValue, 10);
        }
        else if (characteristic.uuid === this.characteristicsFound[6].uuid) {
            this.sixthValue = parseInt(value, 10);
        }
        else if (characteristic.uuid === this.characteristicsFound[7].uuid) {
            this.seventhValue = parseInt(value, 10);
        }
        this.timestampContainers[0] = this.getDateTime();
    },
    onDisconnected(device) {
        console.log('Device Disconnected:', device.name);
        this.bleState = 'Device Disconnected';
        this.connectToDevice();
    },
    onButton() {
      this.writeOnCharacteristic(1);
    },
    offButton() {
      this.writeOnCharacteristic(0);
    },
    writeOnCharacteristic(value) {                         //TODO update this for array of characteristics
        if (this.bleServer && this.bleServer.connected) {
            const characteristic = this.characteristicsFound[0];
            console.log("Found the LED characteristic: ", characteristic.uuid);
            const data = new Uint8Array([value]);
            characteristic.writeValue(data)
            .then(() => {
                this.latestValueSent = value;
                console.log("Value written to LEDcharacteristic:", value);
                    if(value === 1){
                    this.isOverride = true;
                    }
                    else{
                        this.isOverride = false;
                    }
            })
            .catch(error => {
                console.error("Error writing to the LED characteristic: ", error);
            });
        } else {
            console.error ("Bluetooth is not connected. Cannot write to characteristic.")
            window.alert("Bluetooth is not connected. Cannot write to characteristic. \nConnect to BLE first!")
        }
    },
    disconnectDevice() {
        this.endTime = new Date();
        console.log("Disconnect Device.");
        if (this.bleServer && this.bleServer.connected) {
            const stopNotificationPromises = this.characteristicsFound
                .filter(characteristic => characteristic && characteristic.properties.notify)
                .map(characteristic => characteristic.stopNotifications());

            Promise.all(stopNotificationPromises)
                .then(() => {
                    console.log("Notifications Stopped");
                    return this.bleServer.disconnect();
                })
                .then(() => {
                    console.log("Device Disconnected");
                    this.bleState = "Disconnected";
                    this.createPost();
                })
                .catch(error => {
                    console.log("An error occurred:", error);
                });
        } else {
            // Throw an error if Bluetooth is not connected
            console.error("Bluetooth is not connected.");
            window.alert("Bluetooth is not connected.")
        }
    },
    getDateTime() {
        var currentdate = new Date();
        var day = ("00" + currentdate.getDate()).slice(-2); // Convert day to string and slice
        var month = ("00" + (currentdate.getMonth() + 1)).slice(-2);
        var year = currentdate.getFullYear();
        var hours = ("00" + currentdate.getHours()).slice(-2);
        var minutes = ("00" + currentdate.getMinutes()).slice(-2);
        var seconds = ("00" + currentdate.getSeconds()).slice(-2);

        var datetime = month + "/" + day + "/" + year + " at " + hours + ":" + minutes + ":" + seconds;
        return datetime;
    },
    async createPost() { 
      try {
        await PostService.insertPost(this.sign1, this.sign2, this.total, this.startTime, this.endTime, this.displayTotalTime, this.location);  //calculated in computed property
        const posts = await PostService.getPosts();
        this.posts = posts.sort((a, b) => new Date(b.createdAt) - new Date(a.createdAt));
        toast.success('New post added.');
      } catch (error) {
        toast.error('Failed to add new post.');
      }
      this.sign1 = 0;
      this.sign2 = 0;
      this.total = 0;
    },
  },
};
</script>

<style scoped>
.content {
    padding: 50px;
}
.card-grid {
    max-width: 800px;
    margin: 0 auto;
    margin-bottom: 30px;
    display: grid;
    grid-gap: 2rem;
    grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
}
.card {
    text-align: center;
    background-color: white;
    box-shadow: 2px 2px 12px 1px rgba(140,140,140,.5);
}
button {
    color: white;
    padding: 14px 20px;
    margin: 8px 0;
    border: none;
    cursor: pointer;
    border-radius: 4px;
}
.onButton{
    background-color: #1b8a94;
    margin-right: 10px;
}
.onButton:hover{
    background-color: #177881;
}

.offButton{
    background-color: #5f6c6d;
}
.offButton:hover{
    background-color: #4a5354;
}

.connectButton{
    background-color: #4CAF50;
    margin-right: 10px;
}
.connectButton:hover{
    background-color: #1f8f2f;
}

.disconnectButton{
    background-color: #d13a30;
}
.disconnectButton:hover{
    background-color: #942722;
}

.gray-label {
    color: #bebebe;
    font-size: 1rem;
}
.reading {
    font-size: 1.8rem;
}
.my-image {
  width: 100px;
  height: 100px;
}
.notification {
  position: fixed;
  top: 0;
  right: 0;
  padding: 0px 5px;
  background-color: #f44336; /* Red */
  color: white;
  z-index: 1000; /* Ensure it sits on top */
  margin: 8px;
  border-radius: 5px;

}
.blue {
    color: blue;
    font-size: 30px;
}
.lightgray {
    color: lightgray;
    font-size: 30px;
}
.stream {
    width: 90%;
    height: 300px;
    margin-bottom: 10px;
}
.streamButton {
    background-color: #4CAF50; /* Green */
    border: none;
    color: white;
    padding: 10px 20px; /* Reduced padding */
    text-align: center;
    text-decoration: none;
    display: inline-block;
    font-size: 14px; /* Reduced font size */
    margin: 4px 2px;
    cursor: pointer;
    transition-duration: 0.4s;
}
.streamButton:hover {
    background-color: #45a049;
}
</style>