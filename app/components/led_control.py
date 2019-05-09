import paho.mqtt.client as mqtt

import math
import re
import time
import threading
import json

from app import app
from app.database.database import *
from app.components.file_management import READ_LOGFILE_MQTT, GET_CONFIG_MQTT_BROKER


""" #################### """
""" mqtt publish message """
""" #################### """

BROKER_ADDRESS = GET_CONFIG_MQTT_BROKER()

def MQTT_PUBLISH(MQTT_TOPIC, MQTT_MSG):


    def on_publish(client, userdata, mid):
        print ('Message Published...')

    client = mqtt.Client()
    client.on_publish = on_publish
    client.connect(BROKER_ADDRESS) 
    client.publish(MQTT_TOPIC,MQTT_MSG)
    client.disconnect()

    return ""


""" ############# """
""" led functions """
""" ############# """

def LED_START_SCENE(group_id, scene_id, brightness_global = 100):

    if GET_GLOBAL_SETTING_VALUE("zigbee2mqtt") == "True":

        try:
            group = GET_LED_GROUP_BY_ID(group_id)
            scene = GET_LED_SCENE_BY_ID(scene_id)

            # led 1
            channel = "SmartHome/zigbee2mqtt/" + group.led_name_1 + "/set"
            
            msg =  ('{"state": "ON", "brightness":' + str(scene.brightness_1*(brightness_global/100)) +
                    ',"color": { "r":' + str(scene.red_1) + ',"g":' + str(scene.green_1) + ',"b":' + str(scene.blue_1) + 
                    ',"transition": 3}}')

            MQTT_PUBLISH(channel, msg) 

            # led 2
            if group.active_led_2 == "on": 

                channel = "SmartHome/zigbee2mqtt/" + group.led_name_2 + "/set"

                if scene.active_setting_2 == "on":        
                    msg =  ('{"state": "ON", "brightness":' + str(scene.brightness_2*(brightness_global/100)) +
                            ',"color": { "r":' + str(scene.red_2) + ',"g":' + str(scene.green_2) + ',"b":' + str(scene.blue_2) + 
                            ',"transition": 3}}')
                else:
                    msg = '{"state": "OFF"}'

                MQTT_PUBLISH(channel, msg) 
            
            # led 3
            if group.active_led_3 == "on": 

                channel = "SmartHome/zigbee2mqtt/" + group.led_name_3 + "/set"

                if scene.active_setting_3 == "on":        
                    msg =  ('{"state": "ON", "brightness":' + str(scene.brightness_3*(brightness_global/100)) +
                            ',"color": { "r":' + str(scene.red_3) + ',"g":' + str(scene.green_3) + ',"b":' + str(scene.blue_3) + 
                            ',"transition": 3}}')
                else:
                    msg = '{"state": "OFF"}'

                MQTT_PUBLISH(channel, msg) 

            # led 4
            if group.active_led_4 == "on": 

                channel = "SmartHome/zigbee2mqtt/" + group.led_name_4 + "/set"

                if scene.active_setting_4 == "on":        
                    msg =  ('{"state": "ON", "brightness":' + str(scene.brightness_4*(brightness_global/100)) +
                            ',"color": { "r":' + str(scene.red_4) + ',"g":' + str(scene.green_4) + ',"b":' + str(scene.blue_4) + 
                            ',"transition": 3}}')
                else:
                    msg = '{"state": "OFF"}'

                MQTT_PUBLISH(channel, msg)             
                        
            # led 5
            if group.active_led_5 == "on": 

                channel = "SmartHome/zigbee2mqtt/" + group.led_name_5 + "/set"

                if scene.active_setting_5 == "on":        
                    msg =  ('{"state": "ON", "brightness":' + str(scene.brightness_5*(brightness_global/100)) +
                            ',"color": { "r":' + str(scene.red_5) + ',"g":' + str(scene.green_5) + ',"b":' + str(scene.blue_5) + 
                            ',"transition": 3}}')
                else:
                    msg = '{"state": "OFF"}'

                MQTT_PUBLISH(channel, msg) 
            
            # led 6
            if group.active_led_6 == "on": 

                channel = "SmartHome/zigbee2mqtt/" + group.led_name_6 + "/set"

                if scene.active_setting_6 == "on":        
                    msg =  ('{"state": "ON", "brightness":' + str(scene.brightness_6*(brightness_global/100)) +
                            ',"color": { "r":' + str(scene.red_6) + ',"g":' + str(scene.green_6) + ',"b":' + str(scene.blue_6) + 
                            ',"transition": 3}}')
                else:
                    msg = '{"state": "OFF"}'

                MQTT_PUBLISH(channel, msg) 

            # led 7
            if group.active_led_7 == "on": 

                channel = "SmartHome/zigbee2mqtt/" + group.led_name_7 + "/set"

                if scene.active_setting_7 == "on":        
                    msg =  ('{"state": "ON", "brightness":' + str(scene.brightness_7*(brightness_global/100)) +
                            ',"color": { "r":' + str(scene.red_7) + ',"g":' + str(scene.green_7) + ',"b":' + str(scene.blue_7) + 
                            ',"transition": 3}}')
                else:
                    msg = '{"state": "OFF"}'

                MQTT_PUBLISH(channel, msg)     

            # led 8
            if group.active_led_8 == "on": 

                channel = "SmartHome/zigbee2mqtt/" + group.led_name_8 + "/set"

                if scene.active_setting_8 == "on":        
                    msg =  ('{"state": "ON", "brightness":' + str(scene.brightness_8*(brightness_global/100)) +
                            ',"color": { "r":' + str(scene.red_8) + ',"g":' + str(scene.green_8) + ',"b":' + str(scene.blue_8) + 
                            ',"transition": 3}}')
                else:
                    msg = '{"state": "OFF"}'

                MQTT_PUBLISH(channel, msg) 
            
            # led 9
            if group.active_led_9 == "on": 

                channel = "SmartHome/zigbee2mqtt/" + group.led_name_9 + "/set"

                if scene.active_setting_9 == "on":        
                    msg =  ('{"state": "ON", "brightness":' + str(scene.brightness_9*(brightness_global/100)) +
                            ',"color": { "r":' + str(scene.red_9) + ',"g":' + str(scene.green_9) + ',"b":' + str(scene.blue_9) + 
                            ',"transition": 3}}')
                else:
                    msg = '{"state": "OFF"}'

                MQTT_PUBLISH(channel, msg) 
                
            time.sleep(1)
            
            # set current state
            scene_name = GET_LED_SCENE_BY_ID(scene_id).name
            
            SET_LED_GROUP_CURRENT_SETTING(group_id, scene_name)
            SET_LED_GROUP_CURRENT_BRIGHTNESS(group_id, brightness_global)
                
            return LED_CHECK_SETTING() 

        except Exception as e:
            WRITE_LOGFILE_SYSTEM("ERROR", "LED | start scene | " + str(e))
            return str(e)
            
    else:
        return ["Keine LED-Steuerung aktiviert"]  
                

def LED_SET_BRIGHTNESS(group_id, brightness_global = 100):
    
    if GET_GLOBAL_SETTING_VALUE("zigbee2mqtt") == "True":
        
        brightness = float(brightness_global) * 2.54
        brightness = int(brightness)

        try:
            group = GET_LED_GROUP_BY_ID(group_id)

            # led 1
            channel = "SmartHome/zigbee2mqtt/" + group.led_name_1 + "/set"     
            msg     = '{"state": "ON", "brightness":' + str(brightness) + '}'

            MQTT_PUBLISH(channel, msg) 

            # led 2
            if group.active_led_2 == "on": 

                channel = "SmartHome/zigbee2mqtt/" + group.led_name_2 + "/set"      
                msg     = '{"state": "ON", "brightness":' + str(brightness) + '}'

                MQTT_PUBLISH(channel, msg) 
            
            # led 3
            if group.active_led_3 == "on": 

                channel = "SmartHome/zigbee2mqtt/" + group.led_name_3 + "/set"      
                msg     = '{"state": "ON", "brightness":' + str(brightness) + '}'

                MQTT_PUBLISH(channel, msg) 

            # led 4
            if group.active_led_4 == "on": 

                channel = "SmartHome/zigbee2mqtt/" + group.led_name_4 + "/set"      
                msg     = '{"state": "ON", "brightness":' + str(brightness) + '}'

                MQTT_PUBLISH(channel, msg)          
                        
            # led 5
            if group.active_led_5 == "on": 

                channel = "SmartHome/zigbee2mqtt/" + group.led_name_5 + "/set"
                msg     = '{"state": "ON", "brightness":' + str(brightness) + '}'

                MQTT_PUBLISH(channel, msg)    
            
            # led 6
            if group.active_led_6 == "on": 

                channel = "SmartHome/zigbee2mqtt/" + group.led_name_6 + "/set"
                msg     = '{"state": "ON", "brightness":' + str(brightness) + '}'

                MQTT_PUBLISH(channel, msg)    

            # led 7
            if group.active_led_7 == "on": 

                channel = "SmartHome/zigbee2mqtt/" + group.led_name_7 + "/set"
                msg     = '{"state": "ON", "brightness":' + str(brightness) + '}'

                MQTT_PUBLISH(channel, msg)        

            # led 8
            if group.active_led_8 == "on": 

                channel = "SmartHome/zigbee2mqtt/" + group.led_name_8 + "/set"
                msg     = '{"state": "ON", "brightness":' + str(brightness) + '}'

                MQTT_PUBLISH(channel, msg)    
            
            # led 9
            if group.active_led_9 == "on": 

                channel = "SmartHome/zigbee2mqtt/" + group.led_name_9 + "/set"
                msg     = '{"state": "ON", "brightness":' + str(brightness) + '}'

                MQTT_PUBLISH(channel, msg)     
                
            time.sleep(1)
            
            # set current state
            SET_LED_GROUP_CURRENT_BRIGHTNESS(group_id, brightness_global)
                
            return LED_CHECK_SETTING() 


        except Exception as e:
            WRITE_LOGFILE_SYSTEM("ERROR", "LED | set brightness | " + str(e))
            return str(e)
 
    else:
        return ["Keine LED-Steuerung aktiviert"]  


def LED_TURN_OFF_GROUP(group_id):

    if GET_GLOBAL_SETTING_VALUE("zigbee2mqtt") == "True":

        try:
            group = GET_LED_GROUP_BY_ID(group_id)
            
            print(group.led_name_1)

            # led 1
            channel = "SmartHome/zigbee2mqtt/" + group.led_name_1 + "/set"
            msg = '{"state": "OFF"}'
            MQTT_PUBLISH(channel, msg) 

            # led 2
            if group.active_led_2 == "on": 
                channel = "SmartHome/zigbee2mqtt/" + group.led_name_2 + "/set"
                msg = '{"state": "OFF"}'
                MQTT_PUBLISH(channel, msg) 

            # led 3
            if group.active_led_3 == "on": 
                channel = "SmartHome/zigbee2mqtt/" + group.led_name_3 + "/set"
                msg = '{"state": "OFF"}'
                MQTT_PUBLISH(channel, msg) 

            # led 4
            if group.active_led_4 == "on": 
                channel = "SmartHome/zigbee2mqtt/" + group.led_name_4 + "/set"
                msg = '{"state": "OFF"}'
                MQTT_PUBLISH(channel, msg) 

            # led 5
            if group.active_led_5 == "on": 
                channel = "SmartHome/zigbee2mqtt/" + group.led_name_5 + "/set"
                msg = '{"state": "OFF"}'
                MQTT_PUBLISH(channel, msg) 

            # led 6
            if group.active_led_6 == "on": 
                channel = "SmartHome/zigbee2mqtt/" + group.led_name_6 + "/set"
                msg = '{"state": "OFF"}'
                MQTT_PUBLISH(channel, msg) 

            # led 7
            if group.active_led_7 == "on": 
                channel = "SmartHome/zigbee2mqtt/" + group.led_name_7 + "/set"
                msg = '{"state": "OFF"}'
                MQTT_PUBLISH(channel, msg)                 

            # led 8
            if group.active_led_8 == "on": 
                channel = "SmartHome/zigbee2mqtt/" + group.led_name_8 + "/set"
                msg = '{"state": "OFF"}'
                MQTT_PUBLISH(channel, msg) 
            
            # led 9
            if group.active_led_9 == "on": 
                channel = "SmartHome/zigbee2mqtt/" + group.led_name_9 + "/set"
                msg = '{"state": "OFF"}'
                MQTT_PUBLISH(channel, msg) 
            
            time.sleep(1)
            
            # set current state
            SET_LED_GROUP_CURRENT_SETTING(group_id, "OFF") 
            SET_LED_GROUP_CURRENT_BRIGHTNESS(group_id, 0)           
            
            return LED_CHECK_SETTING() 

        except Exception as e:
            WRITE_LOGFILE_SYSTEM("ERROR", "LED | turn_off | " + str(e))
            return str(e)
            
    else:
        return ["Keine LED-Steuerung aktiviert"]  
        


def LED_TURN_OFF_ALL():
    
    if GET_GLOBAL_SETTING_VALUE("zigbee2mqtt") == "True":   
        
        try: 
            leds = GET_ALL_MQTT_DEVICES("led")

            for led in leds:
                channel = "SmartHome/zigbee2mqtt/" + led.name + "/set"
                msg = '{"state": "OFF"}'
                MQTT_PUBLISH(channel, msg) 
                
            time.sleep(1)
            
            print("#############")
            
            # set current state
            for group in GET_ALL_ACTIVE_LED_GROUPS():   
                SET_LED_GROUP_CURRENT_SETTING(group.id, "OFF")
                SET_LED_GROUP_CURRENT_BRIGHTNESS(group.id, 0)
                
            return LED_CHECK_SETTING() 
            
        except Exception as e:
            WRITE_LOGFILE_SYSTEM("ERROR", "LED | turn_off | " + str(e))
            return str(e)

    else:
        return ["Keine LED-Steuerung aktiviert"]  


""" ################# """
""" program functions """
""" ################# """


def LED_START_PROGRAM_THREAD(group_id, program_id):

    try:
        LED_TURN_OFF_GROUP(group_id)
        
        # set current state
        program_name = GET_LED_PROGRAM_BY_ID(program_id).name  
        
        content = GET_LED_PROGRAM_BY_ID(program_id).content

        for line in content.splitlines():
            
            if "bri" in line: 
                led_id = line.split(":")[0]
                brightness = re.findall(r'\d+', line.split(":")[1])
                brightness = brightness[0]
                break
        
        SET_LED_GROUP_CURRENT_SETTING(group_id, program_name)
        SET_LED_GROUP_CURRENT_BRIGHTNESS(group_id, int(brightness))

        # start thread
        Thread = threading.Thread(target=LED_PROGRAM_THREAD, args=(group_id, program_id, ))
        Thread.start()  
        
        return "" 
     
    except Exception as e:
        WRITE_LOGFILE_SYSTEM("ERROR", "LED | start program | " + str(e))
        return str(e)
    

def LED_PROGRAM_THREAD(group_id, program_id):

    if GET_GLOBAL_SETTING_VALUE("zigbee2mqtt") == "True":
        
        try:
            content = GET_LED_PROGRAM_BY_ID(program_id).content

            # select each command line
            for line in content.splitlines():

                if "rgb" in line: 
                    led_id = line.split(":")[0]
                    rgb    = re.findall(r'\d+', line.split(":")[1])
                    red    = rgb[0]
                    green  = rgb[1]           
                    blue   = rgb[2]  
                    LED_PROGRAM_SET_RGB(group_id, led_id, red, green, blue)
                    
                if "bri" in line: 
                    led_id = line.split(":")[0]
                    brightness = re.findall(r'\d+', line.split(":")[1])
                    brightness = brightness[0]
                    LED_PROGRAM_SET_BRIGHTNESS(group_id, led_id, brightness)

                if "pause" in line: 
                    break_value = line.split(":")
                    break_value = int(break_value[1])
                    time.sleep(break_value)
                    
            time.sleep(1)
            
            return LED_CHECK_SETTING() 
     
        except Exception as e:
            WRITE_LOGFILE_SYSTEM("ERROR", "LED | start program | " + str(e))
            return str(e)
               
    else:
        return ["Keine LED-Steuerung aktiviert"]           


def LED_PROGRAM_SET_RGB(group_id, led_id, red, green, blue):

    group = GET_LED_GROUP_BY_ID(group_id)

    # led 1
    if led_id == "1":
        channel = "SmartHome/zigbee2mqtt/" + group.led_name_1 + "/set"
        msg     =  ('{"state": "ON","color": { "r":' + str(red) + 
                    ',"g":' + str(green) + ',"b":' + str(blue) + ',"transition": 3}}')
        MQTT_PUBLISH(channel, msg) 

    # led 2
    if led_id == "2":
        channel = "SmartHome/zigbee2mqtt/" + group.led_name_2 + "/set"
        msg     =  ('{"state": "ON","color": { "r":' + str(red) + 
                    ',"g":' + str(green) + ',"b":' + str(blue) + ',"transition": 3}}')
        MQTT_PUBLISH(channel, msg)    

    # led 3
    if led_id == "3":
        channel = "SmartHome/zigbee2mqtt/" + group.led_name_3 + "/set"
        msg     =  ('{"state": "ON","color": { "r":' + str(red) + 
                    ',"g":' + str(green) + ',"b":' + str(blue) + ',"transition": 3}}')
        MQTT_PUBLISH(channel, msg) 

    # led 4
    if led_id == "4":
        channel = "SmartHome/zigbee2mqtt/" + group.led_name_4 + "/set"
        msg     =  ('{"state": "ON","color": { "r":' + str(red) + 
                    ',"g":' + str(green) + ',"b":' + str(blue) + ',"transition": 3}}')
        MQTT_PUBLISH(channel, msg)    

    # led 5
    if led_id == "5":
        channel = "SmartHome/zigbee2mqtt/" + group.led_name_5 + "/set"
        msg     =  ('{"state": "ON","color": { "r":' + str(red) + 
                    ',"g":' + str(green) + ',"b":' + str(blue) + ',"transition": 3}}')
        MQTT_PUBLISH(channel, msg) 

    # led 6
    if led_id == "6":
        channel = "SmartHome/zigbee2mqtt/" + group.led_name_6 + "/set"
        msg     =  ('{"state": "ON","color": { "r":' + str(red) + 
                    ',"g":' + str(green) + ',"b":' + str(blue) + ',"transition": 3}}')
        MQTT_PUBLISH(channel, msg)    

    # led 7
    if led_id == "7":
        channel = "SmartHome/zigbee2mqtt/" + group.led_name_7 + "/set"
        msg     =  ('{"state": "ON","color": { "r":' + str(red) + 
                    ',"g":' + str(green) + ',"b":' + str(blue) + ',"transition": 3}}')
        MQTT_PUBLISH(channel, msg) 

    # led 8
    if led_id == "8":
        channel = "SmartHome/zigbee2mqtt/" + group.led_name_8 + "/set"
        msg     =  ('{"state": "ON","color": { "r":' + str(red) + 
                    ',"g":' + str(green) + ',"b":' + str(blue) + ',"transition": 3}}')
        MQTT_PUBLISH(channel, msg)    

    # led 9
    if led_id == "9":
        channel = "SmartHome/zigbee2mqtt/" + group.led_name_9 + "/set"
        msg     =  ('{"state": "ON","color": { "r":' + str(red) + 
                    ',"g":' + str(green) + ',"b":' + str(blue) + ',"transition": 3}}')
        MQTT_PUBLISH(channel, msg) 


def LED_PROGRAM_SET_BRIGHTNESS(group_id, led_id, brightness_global):

    # set current state
    SET_LED_GROUP_CURRENT_BRIGHTNESS(group_id, brightness_global)

    group = GET_LED_GROUP_BY_ID(group_id)
    brightness = float(brightness_global) * 2.54
    brightness = int(brightness)

    # led 1
    if led_id == "1":
        channel = "SmartHome/zigbee2mqtt/" + group.led_name_1 + "/set"
        msg     = '{"state": "ON", "brightness":' + str(brightness) + ',"transition": 3}}'
        MQTT_PUBLISH(channel, msg) 

    # led 2
    if led_id == "2":
        channel = "SmartHome/zigbee2mqtt/" + group.led_name_2 + "/set"
        msg     = '{"state": "ON", "brightness":' + str(brightness) + ',"transition": 3}}'
        MQTT_PUBLISH(channel, msg) 

    # led 3
    if led_id == "3":
        channel = "SmartHome/zigbee2mqtt/" + group.led_name_3 + "/set"
        msg     = '{"state": "ON", "brightness":' + str(brightness) + ',"transition": 3}}'
        MQTT_PUBLISH(channel, msg)        

    # led 4
    if led_id == "4":
        channel = "SmartHome/zigbee2mqtt/" + group.led_name_4 + "/set"
        msg     = '{"state": "ON", "brightness":' + str(brightness) + ',"transition": 3}}'
        MQTT_PUBLISH(channel, msg)  

    # led 5
    if led_id == "5":
        channel = "SmartHome/zigbee2mqtt/" + group.led_name_5 + "/set"
        msg     = '{"state": "ON", "brightness":' + str(brightness) + ',"transition": 3}}'
        MQTT_PUBLISH(channel, msg) 

    # led 6
    if led_id == "6":
        channel = "SmartHome/zigbee2mqtt/" + group.led_name_6 + "/set"
        msg     = '{"state": "ON", "brightness":' + str(brightness) + ',"transition": 3}}'
        MQTT_PUBLISH(channel, msg)  

    # led 7
    if led_id == "7":
        channel = "SmartHome/zigbee2mqtt/" + group.led_name_7 + "/set"
        msg     = '{"state": "ON", "brightness":' + str(brightness) + ',"transition": 3}}'
        MQTT_PUBLISH(channel, msg) 

    # led 8
    if led_id == "8":
        channel = "SmartHome/zigbee2mqtt/" + group.led_name_8 + "/set"
        msg     = '{"state": "ON", "brightness":' + str(brightness) + ',"transition": 3}}'
        MQTT_PUBLISH(channel, msg)  

    # led 9
    if led_id == "9":
        channel = "SmartHome/zigbee2mqtt/" + group.led_name_9 + "/set"
        msg     = '{"state": "ON", "brightness":' + str(brightness) + ',"transition": 3}}'
        MQTT_PUBLISH(channel, msg) 
   
        
""" ################## """
"""  check led setting """
""" ################## """
 
def LED_CHECK_SETTING():
            
    input_messages = READ_LOGFILE_MQTT("zigbee2mqtt", "SmartHome/zigbee2mqtt/bridge/log", 5)
            
    list_errors = []
 
    if input_messages != "Message nicht gefunden":
        for input_message in input_messages:
            input_message = str(input_message[2])
  
            data = json.loads(input_message)
            
            if data["type"] == "zigbee_publish_error":
                if (data["meta"]["entity"]["ID"]) not in list_errors:
                    list_errors.append(data["meta"]["entity"]["ID"])
                    list_errors.append(data["message"])
                    
    if list_errors != []:
        return list_errors
        
    else:
        return ""
        
        
