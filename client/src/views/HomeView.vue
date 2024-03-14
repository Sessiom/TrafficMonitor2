<template>
    <div class="content">
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

        <div class="card-grid">
            <div class="card">
                <h2>Sign 1</h2>
                <p class="reading"><span id="valueContainer2">{{ retrievedSouthValue }}</span></p>
                <img :src="require('@/assets/slow.png')" class="my-image"/>
                <i class="fas fa-car" style="font-size: 30px; color: lightgray;"></i>
                
                <p class="gray-label">Last reading: <span class="timestamp">{{ timestampContainers[0] }}</span></p>
            </div>

            <div class="card">
                <h2>Sign 2 </h2>
                <p class="reading"><span id="valueContainer1">{{ retrievedNorthValue }}</span></p>
                <img :src="require('@/assets/stop.png')" class="my-image"/>
                <i class="fas fa-car" style="font-size: 30px; color: lightgray;"></i>
                <p class="gray-label">Last reading: <span class="timestamp">{{ timestampContainers[1] }}</span></p>
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
      deviceName: 'ESP32',
      bleService: '6c744422-08a1-40c7-807a-576b64b52437',
      characteristics: [ 
      '2bd7866c-14ca-4191-a09f-c4985352cc96',      // LED characteristic
      'de420cdd-4085-4066-8ee7-a6c5e28316d5',      // Sensor characteristic
      'dc51766b-fe18-4d8f-bb31-d49e82e59e18',      // second characteristic
      'c28e246d-5632-44d7-8fdb-124f4243eb10',      // third characteristic
      '65037f44-f9f5-48a4-8205-e9d3dc574316',      // fourth characteristic
      '55a12381-bb3c-4731-9cde-99fcbc13fca2',      // fifth characteristic
      'd9001af2-630c-4a44-ad33-2520d5fc93ff',      // carWaitingLeft characteristic
      '0d044a6c-fdf5-485f-b0f0-55c8d9f3854a'       // carWaitingRight characteristic
      ],
      bleServer: null,
      bleServiceFound: null,
      sensorCharacteristicFound: null,
      latestValueSent: '',
      retrievedValue: 'NaN',
      secondValue: 'NaN',
      thirdValue: '0',
      fourthValue: '0',
      fifthValue: '0',
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
            // Now you can read or write the values of the characteristics as needed
            // For example, to read the values:
            const sensorCharacteristic = characteristics[1];
            const secondCharacteristic = characteristics[2];
            const thirdCharacteristic = characteristics[3];
            const fourthCharacteristic = characteristics[4];
            const fifthCharacteristic = characteristics[5];

            sensorCharacteristic.addEventListener('characteristicvaluechanged', this.handleCharacteristicValueChanged);
            secondCharacteristic.addEventListener('characteristicvaluechanged', this.handleCharacteristicValueChanged);
            thirdCharacteristic.addEventListener('characteristicvaluechanged', this.handleCharacteristicValueChanged);
            fourthCharacteristic.addEventListener('characteristicvaluechanged', this.handleCharacteristicValueChanged);
            fifthCharacteristic.addEventListener('characteristicvaluechanged', this.handleCharacteristicValueChanged);

            sensorCharacteristic.startNotifications();
            secondCharacteristic.startNotifications();
            thirdCharacteristic.startNotifications();
            fourthCharacteristic.startNotifications();
            fifthCharacteristic.startNotifications();

            console.log("Notifications started for Sensor Characteristic");
            console.log("Notifications started for Second Characteristic");
            console.log("Notifications started for Third Characteristic");
            console.log("Notifications started for Fourth Characteristic");
            console.log("Notifications started for Fifth Characteristic");
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
            window.alert("Bluetooth is not connected. Cannot write to characteristic. \n Connect to BLE first!")
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
</style>