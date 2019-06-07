from app import app

from app.speechcontrol.snowboy import snowboydetect
from app.speechcontrol.snowboy import snowboydecoder
from app.speechcontrol.speech_recognition_provider import SPEECH_RECOGNITION_PROVIDER
from app.database.database import *
from app.components.file_management import *
from app.speechcontrol.microphone_led_control import MICROPHONE_LED_CONTROL

import sys
import signal

interrupted = False

def signal_handler(signal, frame):
   global interrupted
   interrupted = True

def interrupt_callback():
   global interrupted
   return interrupted


def SNOWBOY_START():

   signal.signal(signal.SIGINT, signal_handler)

   sensitivity_value = GET_SNOWBOY_SETTINGS().sensitivity / 100
    
   hotword_file = GET_SPEECH_RECOGNITION_PROVIDER_SETTINGS().snowboy_hotword
   
   # check hotword files exist
   if hotword_file in GET_ALL_HOTWORD_FILES():
   
      # voice models here:
      models = GET_SPEECH_RECOGNITION_PROVIDER_HOTWORD(GET_SPEECH_RECOGNITION_PROVIDER_SETTINGS().snowboy_hotword)
      
      sensitivity_value = GET_SNOWBOY_SETTINGS().sensitivity / 100

      # modify sensitivity for better detection / accuracy
      detector = snowboydecoder.HotwordDetector(models, sensitivity=sensitivity_value)  
      
      def detect_callback():
         detector.terminate()
         MICROPHONE_LED_CONTROL(GET_SNOWBOY_SETTINGS().microphone, "on")
         SPEECH_RECOGNITION_PROVIDER(GET_SNOWBOY_SETTINGS().timeout)
         MICROPHONE_LED_CONTROL(GET_SNOWBOY_SETTINGS().microphone, "off")

         detector.start(detected_callback=detect_callback, interrupt_check=interrupt_callback, sleep_time=0.03)

      WRITE_LOGFILE_SYSTEM("EVENT", "Speech Control | started") 

      # main loop
      detector.start(detected_callback=detect_callback,
                     interrupt_check=interrupt_callback,
                     sleep_time=0.03)

      detector.terminate()

   else:
      WRITE_LOGFILE_SYSTEM("ERROR", "Speech Control | Snowboy Hotword - " + hotword_file + " | not founded")

