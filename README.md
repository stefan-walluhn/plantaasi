## create a development environment 

### create environment for flashing

create python virtual environment
`python3 -m venv venv`

install required python software
`./venv/bin/pip install -r requirements.txt`

### flash esp32 with micropython

download latest micropython from micropython.org
`wget https://micropython.org/resources/firmware/esp32-20220117-v1.18.bin`

erase esp32
`./venv/bin/esptool.py --chip esp32 --port /dev/ttyUSB0 erase_flash`

flash the downloaded firmware firmware
`./venv/bin/esptool.py --chip esp32 --port /dev/ttyUSB0 --baud 460800 write_flash -z 0x1000 esp32-20220117-v1.18.bin`

### create configuration file

copy the config example
`cp config.json.example config.json`

edit the configuration for your environment

### Transfer plantaasi to the microcontroller

`./venv/bin/ampy --port /dev/ttyUSB0 put plantaasi`

`./venv/bin/ampy --port /dev/ttyUSB0 put main.py`

`./venv/bin/ampy --port /dev/ttyUSB0 put config.json`


### install required library on esp32

connect to the micropython 
`screen /dev/ttyUSB0 115200 8N1`

connect to your wifi
```
import network

wlan = network.WLAN(network.STA_IF)
wlan.active(True)
if not wlan.isconnected():
    wlan.connect("ESSID", "PASSWORD")

    while not wlan.isconnected():
        time.sleep(1)
```

install urequests library
`import upip`
`upip.install('urequests')`
