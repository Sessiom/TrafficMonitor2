<script>
// @ is an alias to /src

</script>

<template>
    <div class="content">
        <div class="card-grid">
            <div class="card">
                <p>
                    <button id="connectBleButton" class="connectButton"> Connect </button>
                    <button id="disconnectBleButton" class="disconnectButton"> Disconnect </button>
                </p>
                <p class="gray-label">Device state: <strong><span id="bleState" style="color:#d13a30;">Disconnected</span></strong></p>
            </div>
        </div>

        <div class="card-grid">
            <div class="card">
                <h2>Red Red Override</h2>
                <button id="onButton" class="onButton">ON</button>
                <button id="offButton" class="offButton">OFF</button>
                <p class="gray-label">Last value sent: <span id="valueSent"></span></p>
            </div>
        </div>

        <div class="card-grid">
            <div class="card">
                <h2>Sign 1</h2>
                <p class="reading"><span id="valueContainer2">NaN</span></p>
                <p class="gray-label">Last reading: <span class="timestamp"></span></p>
            </div>

            <div class="card">
                <h2>Sign 2 </h2>
                <p class="reading"><span id="valueContainer1">NaN</span></p>
                <p class="gray-label">Last reading: <span class="timestamp"></span></p>
            </div>

        </div>

        <div class="card-grid">
            <div class="card">
                <h2>Cars In Lane</h2>
                <p class="reading"><span id="valueContainer3">NaN</span></p>
                <p class="gray-label">Last reading: <span class="timestamp"></span></p>
            </div>
        </div>

    </div>
    <div class="footer">
        <p></p>
        <p></p>
    </div>
</template>

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