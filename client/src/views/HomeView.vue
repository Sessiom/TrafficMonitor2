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
                <h2>Red Red Override</h2>
                <button id="onButton" class="onButton">ON</button>
                <button id="offButton" class="offButton">OFF</button>
                <p class="gray-label">Last value sent: <span id="valueSent">{{ latestValueSent }}</span></p>
            </div>
        </div>

        <div class="card-grid">
            <div class="card">
                <h2>Sign 1</h2>
                <p class="reading"><span id="valueContainer2">{{ retrievedSouthValue }}</span></p>
                <p class="gray-label">Last reading: <span class="timestamp">{{ timestampContainers[0] }}</span></p>
            </div>

            <div class="card">
                <h2>Sign 2 </h2>
                <p class="reading"><span id="valueContainer1">{{ retrievedNorthValue }}</span></p>
                <p class="gray-label">Last reading: <span class="timestamp">{{ timestampContainers[1] }}</span></p>
            </div>

        </div>

        <div class="card-grid">
            <div class="card">
                <h2>Cars In Lane</h2>
                <p class="reading"><span id="valueContainer3">{{ retrievedCarCountValue }}</span></p>
                <p class="gray-label">Last reading: <span class="timestamp">{{ timestampContainers[2] }}</span></p>
            </div>
        </div>

        <div class="card-grid">
            <div class="card">
                <h2>Car Counts</h2>
                <p class="reading"><span>Sign 1: </span><span id="valueContainer4">{{ retrievedSign1CarCountValue }}</span></p>
                <p class="reading"><span>Sign 2: </span><span id="valueContainer5">{{ retrievedSign2CarCountValue }}</span></p>
                <p class="reading"><span>Total: </span><span> {{ total }}</span></p>
                <p class="gray-label">Last reading: <span class="timestamp">{{ timestampContainers[3] }}</span></p>
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
      bleService: '19b10000-e8f2-537e-4f6c-d104768a1214',
      SouthCharacteristic: '19b10001-e8f2-537e-4f6c-d104768a1214',
      RedRedCharacteristic: '19b10002-e8f2-537e-4f6c-d104768a1214',
      NorthCharacteristic: '19b10003-e8f2-537e-4f6c-d104768a1214',
      CarCountCharacteristic: '19b10004-e8f2-537e-4f6c-d104768a1214',
      Sign1CarCountCharacteristic: '19b10005-e8f2-537e-4f6c-d104768a1214',
      Sign2CarCountCharacteristic: '19b10006-e8f2-537e-4f6c-d104768a1214',
      bleServer: null,
      bleServiceFound: null,
      SouthCharacteristicFound: null,
      NorthCharacteristicFound: null,
      CarCountCharacteristicFound: null,
      Sign1CarCountCharacteristicFound: null,
      Sign2CarCountCharacteristicFound: null,
      sign1: 0,
      sign2: 0,
      total: 0,
      isUpdating: false,
      retrievedSouthValue: 'NaN',
      retrievedNorthValue: 'NaN',
      retrievedCarCountValue: 'NaN',
      retrievedSign1CarCountValue: 'NaN',
      retrievedSign2CarCountValue: 'NaN',
      latestValueSent: '',
      bleState: 'Disconnected',
      timestampContainers: ['', '', '', '']
    };
  },
  computed: {
    calculatedTotal() {
      let sign1 = parseInt(this.retrievedSign1CarCountValue, 10); 
      let sign2 = parseInt(this.retrievedSign2CarCountValue, 10);
      return sign1 + sign2;
    }
  },
  watch: {
    calculatedTotal(newTotal) {
        this.total = newTotal;
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
            this.bleState = 'Connected to device ' + device.name;
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
            return service.getCharacteristic(this.SouthCharacteristic);
        })
        .then(characteristic => {
            console.log("SouthCharacteristic discovered:", characteristic.uuid);
            this.SouthCharacteristicFound = characteristic;
            characteristic.addEventListener('characteristicvaluechanged', this.handleCharacteristicChange1);
            characteristic.startNotifications();
            console.log("Notifications Started.");
            return characteristic.readValue();
        })
        .then(value => {
            console.log("Read South value: ", value);
            const decodedValue = new TextDecoder().decode(value);
            console.log("Decoded value: ", decodedValue);
            this.retrievedSouthValue = decodedValue;
            return this.bleServiceFound.getCharacteristic(this.NorthCharacteristic);
        })
        .then(characteristic => {
            console.log("NorthCharacteristic discovered:", characteristic.uuid);
            this.NorthCharacteristicFound = characteristic;
            characteristic.addEventListener('characteristicvaluechanged', this.handleCharacteristicChange2);
            characteristic.startNotifications();
            console.log("Notifications Started.");
            return characteristic.readValue();
        })
        .then(value => {
            console.log("Read North value: ", value);
            const decodedValue = new TextDecoder().decode(value);
            console.log("Decoded value: ", decodedValue);
            this.retrievedNorthValue = decodedValue;
            return this.bleServiceFound.getCharacteristic(this.CarCountCharacteristic);
        })
        .then(characteristic => {
            console.log("CarCountCharacteristic discovered:", characteristic.uuid);
            this.CarCountCharacteristicFound = characteristic;
            characteristic.addEventListener('characteristicvaluechanged', this.handleCharacteristicChange3);
            characteristic.startNotifications();
            console.log("Notifications Started.");
            return characteristic.readValue();
        })
        .then(value => {
            console.log("Read CarCount value: ", value);
            const decodedValue = new TextDecoder().decode(value);
            console.log("Decoded value: ", decodedValue);
            this.retrievedCarCountValue = decodedValue;
            return this.bleServiceFound.getCharacteristic(this.Sign1CarCountCharacteristicCharacteristic);
        })
        .then(characteristic => {
            console.log("Sign1CarCountCharacteristic discovered:", characteristic.uuid);
            this.Sign1CarCountCharacteristic = characteristic;
            characteristic.addEventListener('characteristicvaluechanged', this.handleCharacteristicChange4);
            characteristic.startNotifications();
            console.log("Notifications Started.");
            return characteristic.readValue();
        })
        .then(value => {
            console.log("Read Sign1CarCount value: ", value);
            const decodedValue = new TextDecoder().decode(value);
            console.log("Decoded value: ", decodedValue);
            this.retrievedSign1CarCountValue = decodedValue;
            return this.bleServiceFound.getCharacteristic(this.Sign2CarCountCharacteristic);
        })
        .then(characteristic => {
            console.log("Sign2CarCountCharacteristic discovered:", characteristic.uuid);
            this.Sign2CarCountCharacteristic = characteristic;
            characteristic.addEventListener('characteristicvaluechanged', this.handleCharacteristicChange5);
            characteristic.startNotifications();
            console.log("Notifications Started.");
            return characteristic.readValue();
        })
        .catch(error => {
        console.log('Error: ', error);
        })
    },
    onDisconnected(event) {
        console.log('Device Disconnected:', event.target.device.name);
        this.bleState = 'Device Disconnected';
        this.connectToDevice();
    },
    handleCharacteristicChange1(event) {
        if(this.isUpdating) {
            this.retrievedSouthValue = "STOP";
            return;
        }
        else{
            const newValueReceived = new TextDecoder().decode(event.target.value);
            console.log("South Characteristic value changed: ", newValueReceived);
            if (newValueReceived === "1") {
            this.retrievedSouthValue = "SLOW";
            } else {
            this.retrievedSouthValue = "STOP";
            }
            this.timestampContainers[0] = this.getDateTime();
        }
    },
    handleCharacteristicChange2(event) {
        if(this.isUpdating) {
            this.retrievedNorthValue = "STOP";
            return;
        }
        else{
            const newValueReceived = new TextDecoder().decode(event.target.value);
            console.log("North Characteristic value changed: ", newValueReceived);
            if (newValueReceived === "1") {
                this.retrievedNorthValue = "SLOW";
            } else {
                this.retrievedNorthValue = "STOP";
            }
            this.timestampContainers[1] = this.getDateTime();
        }
    },
    handleCharacteristicChange3(event) {
        if(this.isUpdating) {
            this.retrievedCarCountValue = "0";
            return;
        }
        else{
        const newValueReceived = new TextDecoder().decode(event.target.value);
        console.log("Car Count Characteristic value changed: ", newValueReceived);
        this.retrievedCarCountValue = newValueReceived;
        this.timestampContainers[2] = this.getDateTime();
        }
    },
    handleCharacteristicChange4(event) {
        const newValueReceived = new TextDecoder().decode(event.target.value);
        console.log("Sign1 Car Count Characteristic value changed: ", newValueReceived);
        this.retrievedSign1CarCountValue = newValueReceived; 
        this.sign1 = parseInt(this.retrievedSign1CarCountValue, 10);
    },
    handleCharacteristicChange5(event) {
        const newValueReceived = new TextDecoder().decode(event.target.value);
        console.log("Sign2 Car Count Characteristic value changed: ", newValueReceived);
        this.retrievedSign2CarCountValue = newValueReceived;
        this.sign2 = parseInt(this.retrievedSign2CarCountValue, 10);
        this.timestampContainers[3] = this.getDateTime();

    },
    onButton() {
      this.writeOnCharacteristic(1);
    },
    offButton() {
      this.writeOnCharacteristic(0);
    },
    writeOnCharacteristic(value) {
        if (this.bleServer && this.bleServer.connected) {
            if(value === 1){
                this.isUpdating = true;
            }
            else{
                this.isUpdating = false;
            }
            this.bleServiceFound.getCharacteristic(this.RedRedCharacteristic)
            .then(characteristic => {
                console.log("Found the RedRed characteristic: ", characteristic.uuid);
                const data = new Uint8Array([value]);
                return characteristic.writeValue(data);
            })
            .then(() => {
                this.latestValueSent = value;
                console.log("Value written to RedRedcharacteristic:", value);
            })
            .catch(error => {
                console.error("Error writing to the RedRed characteristic: ", error);
            });
        } else {
            console.error ("Bluetooth is not connected. Cannot write to characteristic.")
            window.alert("Bluetooth is not connected. Cannot write to characteristic. \n Connect to BLE first!")
        }
    },
    disconnectDevice() {
        console.log("Disconnect Device.");
        if (this.bleServer && this.bleServer.connected) {
            Promise.all([
            this.SouthCharacteristicFound?.stopNotifications().then(() => console.log("SouthCharacteristic notifications stopped")),
            this.NorthCharacteristicFound?.stopNotifications().then(() => console.log("NorthCharacteristic notifications stopped")),
            this.CarCountCharacteristicFound?.stopNotifications().then(() => console.log("CarCountCharacteristic notifications stopped")),
            this.Sign1CarCountCharacteristic?.stopNotifications().then(() => console.log("Sign1CarCountCharacteristic notifications stopped")),
            this.Sign2CarCountCharacteristic?.stopNotifications().then(() => console.log("Sign2CarCountCharacteristic notifications stopped"))
            ])
            .then(() => this.bleServer.disconnect())
            .then(() => {
            console.log("Device Disconnected");
            this.bleState = "Device Disconnected";
            if(this.total > 0){
                this.createPost();                  // On Disconnect, create a post if total is greater than 0
            }})
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
        toast.info('Working...');
        await PostService.insertPost(this.sign1, this.sign2, this.total);  //calculated in computed property
        const posts = await PostService.getPosts();
        this.posts = posts.sort((a, b) => new Date(b.createdAt) - new Date(a.createdAt));
        toast.clear();
        toast.success('New post added.');
      } catch (error) {
        toast.error('Failed to add new post.');
      }
      this.sign1 = 0;
      this.sign2 = 0;
      this.total = 0;
    },
  },
  mounted() {
    // Add event listeners here
  },
  beforeUnmounted() {
    this.disconnectDevice();
  }
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
</style>