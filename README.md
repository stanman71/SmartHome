##  Miranda

This project creates a smarthome environment.

!!! WORK IN PROGRESS !!!


### Features

- flask server 
- control Philips Hue LEDs
- voice control 
- provide a simple script system to create light shows
- read sensors
- share data with ESP8266 moduls by using MQTT
- taskmanagement to automate processes
- watering plants
- SQL-lite database 
- user management and user rights
- smartphone view

</br>
------------
</br>

### Miranda

#### 1. Installation 

- activate ssh

       >>> sudo raspi-config
       >>> Interfacing Options > SSH > Yes

- update raspian

       >>> sudo apt-get update && sudo apt-get upgrade

- upgrade pip

       >>> pip install --upgrade pip

- open hostname file and insert new name

       >>> sudo nano /etc/hostname
           miranda
          
- create the new folder "/home/pi/miranda" and copy all Miranda files into it

       >>> mkdir miranda

       FileZilla

       Protocol:   SFTP
       Server:     Raspberry PI IP-Address
       Port:       ---
       Connection: normal
       user:       pi
       password:   raspberry

- install BLAS and LAPACK

       >>> sudo apt-get install libblas-dev liblapack-dev libatlas-base-dev gfortran

- install graphviz

       >>> sudo apt-get install graphviz libgraphviz-dev pkg-config
       >>> sudo apt-get install python-pip python-virtualenv

- install all nessessary python modules

       >>> sudo pip3 install -r /home/pi/miranda/requirements.txt --upgrade

- install openCV

       >>> sudo apt install python3-opencv
           (https://raspberrypi.stackexchange.com/questions/100253/how-can-i-install-opencv-on-raspberry-pi-4-raspbian-buster)

- replace wrong spotipy file
 
       >>> sudo cp /home/pi/miranda/support/spotipy/client.py /usr/local/lib/python3.7/dist-packages/spotipy/client.py

- change folder permissions

       >>> sudo chmod -v -R 070 /home/pi/miranda

- default_login

       >>> admin
       >>> qwer1234

</br>

#### 2. Autostart

- create an autostart-file

       >>> sudo nano /etc/systemd/system/miranda.service

           [Unit]
           Description=Miranda
           After=network.target

           [Service]
           ExecStart=/home/pi/miranda/run.py
           WorkingDirectory=/home/pi
           Restart=always

           [Install]
           WantedBy=multi-user.target

- enable autostart

       >>> sudo systemctl enable miranda.service

- start / stop service

       >>> sudo systemctl start miranda
       >>> sudo systemctl stop miranda

- show status / log

       >>> systemctl status miranda.service
       >>> journalctl -u miranda

</br>

#### 3. Manually Control 

- deactivate the miranda service

       >>> sudo systemctl stop miranda

- start the program 

       >>> sudo python3 /home/pi/miranda/run.py

- stop the program 

       >>> sudo killall python3


</br>
------------
</br>

### Optional: Mosquitto (MQTT)

https://mosquitto.org/
</br>
https://forum-raspberrypi.de/forum/thread/31959-mosquitto-autostart/
</br>
https://github.com/eclipse/mosquitto
</br>
https://medium.com/@eranda/setting-up-authentication-on-mosquitto-mqtt-broker-de5df2e29afc
</br>
https://www.auxnet.de/verschluesseltes-mqtt-vom-und-zum-mosquitto-server/
</br>

#### 1. Installation

       >>> sudo apt-get install mosquitto mosquitto-clients -y

</br>

#### 2. Test Mosquitto

- subscribe a channel

       >>> mosquitto_sub -d -h localhost -p 1883 -t "test_channel"

- send a message

       >>> mosquitto_pub -d -h localhost -p 1883 -t "test_channel" -m "Hello World"

</br>

#### 3. Autostart

- create an autostart-file

       >>> sudo nano /etc/systemd/system/mosquitto.service

           [Unit]
           Description=MQTT Broker
           After=network.target

           [Service]
           ExecStart=/usr/sbin/mosquitto -c /etc/mosquitto/mosquitto.conf
           Restart=always

           [Install]
           WantedBy=multi-user.target

- enable autostart

       >>> sudo systemctl enable mosquitto.service

- start / stop service

       >>> sudo systemctl start mosquitto
       >>> sudo systemctl stop mosquitto

- show status / log

       >>> systemctl status mosquitto.service
       >>> journalctl -u mosquitto
       >>> sudo cat /var/log/mosquitto/mosquitto.log

</br>

#### 4. Authentification

- stop mosquitto

       >>> sudo systemctl stop mosquitto

- create a new user and password

       >>> sudo mosquitto_passwd -c /etc/mosquitto/passwd <user_name>

- change file permissions

       >>> sudo chmod -v -R 060 /etc/mosquitto/passwd

- edit mosquitto config and add these two lines

       >>> sudo nano /etc/mosquitto/mosquitto.conf

           password_file /etc/mosquitto/passwd
           allow_anonymous false

- restart mosquitto

       >>> sudo systemctl restart mosquitto

- verify the authentication

       >>> mosquitto_sub -h localhost -p 1883 -t "test_channel" -u <user_name> -P <password>
       >>> mosquitto_pub -h localhost -p 1883 -t "test_channel" -u <user_name> -P <password> -m "Hello World"

</br>
------------
</br>

### Optional: ZigBee2MQTT

https://gadget-freakz.com/diy-zigbee-gateway/
</br>
https://www.zigbee2mqtt.io/
</br>
https://github.com/Koenkk/zigbee2mqtt
</br>

#### 1. Installation

- install Node.js

       >>> sudo curl -sL https://deb.nodesource.com/setup_10.x | sudo -E bash -
       >>> sudo apt-get install -y nodejs git make g++ gcc

- verify that the correct nodejs and npm (automatically installed with nodejs)

       >>> node --version  # Should output v10.X
       >>> npm  --version  # Should output 6.X

- clone zigbee2mqtt repository

       >>> sudo unzip /home/pi/miranda/support/files/zigbee2mqtt_1.6.0.zip -d /opt/zigbee2mqtt
       >>> sudo chown -R pi:pi /opt/zigbee2mqtt

- install zigbee2mqtt 

       >>> cd /opt/zigbee2mqtt
       >>> npm install
	   
	   Note that the npm install produces some warning which can be ignored


##### ERROR: npm not founded

- install the newest version of Node.js 

       >>> https://www.zigbee2mqtt.io/getting_started/running_zigbee2mqtt.html

</br>

#### 2. Configuration

- change file permissions

       >>> sudo chmod -v -R 070 /opt/zigbee2mqtt/data/configuration.yaml

- generate a network key

       >>> dd if=/dev/urandom bs=1 count=16 2>/dev/null | od -A n -t x1 | awk '{printf "["} {for(i = 1; i< NF; i++) {printf "0x%s, ", $i}} {printf "0x%s]\n", $NF}'

- edit zigbee2mqtt config

       >>> sudo nano /opt/zigbee2mqtt/data/configuration.yaml

           # MQTT settings
           mqtt:
           # MQTT base topic for zigbee2mqtt MQTT messages
           base_topic: miranda/zigbee2mqtt
           # MQTT server URL
           server: 'mqtt://localhost'
           # MQTT server authentication, uncomment if required:
           user: <my_user>
           password: <my_password>
           
           advanced:
             network_key: <network_key>

</br>

#### 3. Bridge Software

- start command

       >>> cd /opt/zigbee2mqtt
       >>> npm start

- stop command

       >>> sudo systemctl stop zigbee2mqtt

- view the log of zigbee2mqtt

       >>> sudo journalctl -u zigbee2mqtt.service -f

- backup configuration

       >>> cp -R data data-backup

</br>

#### 4. Pairing

- bridge software must be running to pairing new devices automatically
- zigbee2mqtt setting: {permit_join: true}

</br>

#### 5. Autostart

- create an autostart-file

       >>> sudo nano /etc/systemd/system/zigbee2mqtt.service

           [Unit]
           Description=zigbee2mqtt
           After=network.target

           [Service]
           ExecStart=/usr/bin/npm start
           WorkingDirectory=/opt/zigbee2mqtt
           StandardOutput=inherit
           StandardError=inherit
           Restart=always

           [Install]
           WantedBy=multi-user.target

- enable autostart

       >>> sudo systemctl enable zigbee2mqtt.service

- start / stop service

       >>> sudo systemctl start zigbee2mqtt
       >>> sudo systemctl stop zigbee2mqtt

- show status / log

       >>> systemctl status zigbee2mqtt.service
       >>> journalctl -u zigbee2mqtt

</br>
------------
</br>

### Optional: Zigbee2MQTT Hardware

https://www.zigbee2mqtt.io/getting_started/flashing_the_cc2531.html
</br>
https://www.zigbee2mqtt.io/information/connecting_cc2530.html
</br>
https://github.com/Koenkk/Z-Stack-firmware
</br>
https://github.com/Koenkk/zigbee2mqtt/issues/1437
</br>
https://github.com/Koenkk/zigbee2mqtt/issues/489
</br>
</br>

#### 1. Flashing

- uploading the new coordinator firmware
- instructions and files

       >>> /home/pi/miranda/devices/MS1PA1/z-stack_firmware.zip
       >>> /home/pi/miranda/devices/MS1PA1/zigbee_firmware.zip

</br>

#### 2. CC2531 USB-Stick

- no configuration nessessary, use the default settings

</br>

#### 3. CC2530

- Connect the CC2530 to the Raspberry

       >>> CC2530 -> Raspberry
	   
           VCC -> 3,3V (Pin1)
           GND -> GND  (Pin6)
           P02 -> TXD  (Pin8 / BCM 14)
           P03 -> RXD  (Pin10 / BCM 15)

</br>

- add following at the end of the config file

       >>> sudo nano /boot/config.txt 
	   
	   enable_uart=1
	   dtoverlay=pi3-disable-bt

- disable the modem system service 

       >>> sudo systemctl disable hciuart

- remove any of those entries in the cmdline file, if present

       >>> sudo nano /boot/cmdline.txt

           console=serial0,115200 console=ttyAMA0,11520

- add the lines in zigbee2mqtt config

       >>> sudo nano data/configuration.yaml
	   
	   serial:
		 port: /dev/ttyAMA0
	   advanced:
		 baudrate: 115200
		 rtscts: false

- reboot your raspberry	

   
</br>
------------
</br>

### Optional: Snowboy

https://github.com/Kitt-AI/snowboy
</br>
https://github.com/wanleg/snowboyPi 
</br>
https://snowboy.kitt.ai
</br>
http://docs.kitt.ai/snowboy/
</br>
https://pimylifeup.com/raspberry-pi-snowboy/
</br>
</br>

#### 1. Installation

- install dependencies

       >>> sudo apt -y install python-pyaudio python3-pyaudio sox python3-pip python-pip libatlas-base-dev

</br>

##### ERROR: Command 'arm-linux-gnueabihf-gcc' failed with exit status 1

- install portaudio first (https://github.com/jgarff/rpi_ws281x/issues/294)

       >>> sudo apt-get install portaudio19-dev

</br>

#### 2. Sound settings

- create ".asoundrc" in your home folder with correct hw settings (see example file in https://github.com/wanleg/snowboyPi or /support/Snowboy)

       >>> sudo nano /home/pi/.asoundrc

           pcm.!default {
             type asym
              playback.pcm {
                type plug
                slave.pcm "hw:0,0"
              }
              capture.pcm {
                type plug
                slave.pcm "hw:1,0"
              }
           }

- find out hw cards (e.g "card 0, device 0" is "hw:0,0")

       >>> aplay -l
       >>> arecord -l

</br>

#### 3. Test Sound settings

- audio out

       >>> speaker-test -c 2

- record a 3 second clip 

       >>> arecord -d 3 test.wav

- verify

       >>> aplay test.wav

</br>

#### 4. Replace alsa.conf

       >>> sudo cp /home/pi/miranda/support/snowboy/alsa.conf /usr/share/alsa/alsa.conf

           https://www.raspberrypi.org/forums/viewtopic.php?t=136974

</br>

#### 5. Snowboy in Miranda

- activate snowboy in system/speechcontrol
- restart Miranda

</br>

##### ERROR: ImportError: dynamic module does not define module export function (PyInit__snowboydetect)
##### ERROR: No module named '_snowboydetect'

- create snowboydetect again (https://github.com/Kitt-AI/snowboy)

- install swig 

       https://github.com/Yadoms/yadoms/wiki/Build-on-RaspberryPI
       http://weegreenblobbie.com/?p=263

       >>> sudo apt-get install libpcre3-dev
       >>> wget http://prdownloads.sourceforge.net/swig/swig-3.0.12.tar.gz
       >>> tar xf swig-3.0.12.tar.gz
       >>> cd swig-3.0.12
       >>> ./configure --prefix=/usr
       >>> make -j 4
       >>> sudo make install
 
- check installed swig version

       >>> swig -version

- extract snowboy git archiv

       >>> unzip /home/pi/miranda/support/files/snowboy_1.3.0.zip -d /home/pi/snowboy

- create new detection files

       >>> cd /home/pi/snowboy/swig/Python3 
       >>> make

- replace "_snowboydetect.so" and "snowboydetect.py" in "/home/pi/miranda/app/speechcontrol/snowboy"

- delete the folder "/home/pi/snowboy"

</br>

##### ERROR: ALSA lib confmisc.c:1281:(snd_func_refer) Unable to find definition 'cards.bcm2835_alsa.pcm.front.0:CARD=0'

- if you got many ALBA errors like above and snowboy doesn't work reinstall raspian

</br>

#### 6. Create new Snowboy hotwords

- log into https://snowboy.kitt.ai
- create a new hotword (try to find hotwords as different as possible)
- copy the downloaded file into the folder ~/resources/ on your raspberry pi
- add the new hotword and action in your system settings


</br>
------------
</br>

### Optional: piCorePlayer & LMS (Logitech Media Server)

https://www.picoreplayer.org/
</br>
https://www.basecube.de/2018/03/17/download/
</br>
</br>

#### 1. General Settings piCorePlayer

- change settings option to beta (options are at the bottom corner on the main site)

</br>

- wifi settings

       >>> activate wlan
       >>> insert wlan connetion data (ssid + password)

- main page

       >>> resize filesystem to 200mb
       >>> set a static ip-address

</br>

#### 2. Settings piCorePlayer - Player

- squeezelite settings

       >>> set output device (e.g. HifiBerry DAC+)

- tweaks

       >>> activate squeezelite autostart


</br>

#### 3. Settings piCorePlayer - LMS 

- LMS

       >>> install LMS
       >>> start LMS


</br>

#### 4. LMS 

- LMS IP-address:

       >>> same as piCorePlayer, defaultport = 9000

- Logitech Account

       >>> not necessary, just skip it

- settings

       >>> plugins >>> install Spotty

- config spotty

       >>> add premium account 
       >>> activate player at spotify connect
       >>> activate option "Überwache die Verbindung der Spotty Connect Helferanwendung"
       >>> the new player is now selectable in spotify

- synchronize player

       >>> set the player-groups on the main page in the upper-right corner 
           (Squeezelite must be installed on the clients)
       >>> synchronized groups appears as selectable devices in spotify


</br>

#### 5. Squeezelite - Client

##### Raspian

https://forums.slimdevices.com/showthread.php?110523-squeezelite-shows-up-in-lms-settings-but-not-in-players
</br>
http://www.winko-erades.nl/installing-squeezelite-player-on-a-raspberry-pi-running-jessie/
</br>
</br>

- installation

       >>> sudo apt-get install squeezelite
       
- change Hostname

       >>> sudo nano /etc/hostname

- get sound device informations

       >>> aplay -L

- squeezelite config

       >>> sudo nano /etc/default/squeezelite

	   SL_SOUNDCARD="hw:CARD=sndrpihifiberry,DEV=0"
	   SB_EXTRA_ARGS="-a 180"

- volume setting

       >>> alsamixer

           press "F6" and setect sound-device
           use arrow keys and change "Digital" to 30%     

    
##### Windows 10

- installation

       >>> microsoft store >>> Squeezelite-X

</br>
------------
</br>

### Optional: Raspotify (Spotify Connect for Python)

https://github.com/dtcooper/raspotify
</br>
</br>

- installation

       >>> curl -sL https://dtcooper.github.io/raspotify/install.sh | sh
       
- get audio device informations

       >>> aplay -l

- raspotify config

       >>> sudo nano /etc/default/raspotify

	   DEVICE_NAME="raspotify" 
	   BITRATE="320"
	   OPTIONS="--username <USERNAME> --password <PASSWORD> --device hw:0,1"

- restart raspotify 

       >>> sudo systemctl restart raspotify

- volume setting

       >>> alsamixer

           press "F6" and setect sound-device
           use arrow keys and change "Digital" to 30%  
     

