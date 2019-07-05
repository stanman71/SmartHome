import threading
import time
import json
import heapq

from app import app
from app.database.database import *
from app.components.file_management import WRITE_LOGFILE_SYSTEM
from app.components.mqtt import MQTT_CHECK_SETTING
from app.components.shared_resources import process_management_queue



""" ############ """
""" pump control """
""" ############ """

def START_PUMP(plant_id):
    
    time.sleep(5)
    
    plant    = GET_PLANT_BY_ID(plant_id)
    ieeeAddr = plant.mqtt_device.ieeeAddr 
    
    channel  = "SmartHome/mqtt/" + ieeeAddr + "/set"
    msg      = '{"pump_state": "PUMP_ON", "pump_time":' + str(plant.pumptime) + '}'
    
    heapq.heappush(process_management_queue, (50, ("watering", channel, msg)))
    
    time.sleep(5)
    
    # check pump started first try
    if MQTT_CHECK_SETTING(ieeeAddr, "pump_state", "PUMP_ON", 10):
        SET_MQTT_DEVICE_PREVIOUS_SETTING(ieeeAddr, '"pump_state"="ON"|"pump_time":' + str(plant.pumptime))
        WRITE_LOGFILE_SYSTEM("SUCCESS", "Watering | Plant - " + plant.name + " | Pump started")  
        return True

    time.sleep(5)

    # check pump started second try 
    if MQTT_CHECK_SETTING(ieeeAddr, "pump_state", "PUMP_ON", 10):
        SET_MQTT_DEVICE_PREVIOUS_SETTING(ieeeAddr, '"pump_state"="ON"|"pump_time":' + str(plant.pumptime))
        WRITE_LOGFILE_SYSTEM("SUCCESS", "Watering | Plant - " + plant.name + " | Pump started")  
        return True
        
    WRITE_LOGFILE_SYSTEM("WARNING", "Watering | Plant - " + plant.name + " | Pump starting not confimed") 
    return False

        
        
""" ######### """
""" threading """
""" ######### """

def START_WATERING_THREAD(group):

    Thread = threading.Thread(target=WATERING_THREAD, args=(group, ))
    Thread.start()   


def WATERING_THREAD(group):
    global pump_incoming_list    
  
    pump_running = 0
    warnings     = False       
    
    # search plant
    for plant in GET_ALL_PLANTS():
        
        if plant.group == int(group) or group == "all" or group == "ALL":
            
            watering = False        
        
            # check watertank sensor
            if plant.control_sensor_watertank == "checked":
                
                sensor_values      = plant.mqtt_device.last_values
                sensor_values_json = json.loads(sensor_values)              
                current_watertank  = sensor_values_json["sensor_watertank"] 
                
                if current_watertank == 0:
                    WRITE_LOGFILE_SYSTEM("WARNING", "Watering | Plant - " + plant.name + " | Watertank Low") 
                    warnings = True    
         
     
            # check moisture sensor
            if plant.control_sensor_moisture == "checked":          
                
                moisture_level     = plant.moisture            
                sensor_values      = plant.mqtt_device.last_values
                sensor_values_json = json.loads(sensor_values) 
                current_moisture   = sensor_values_json["sensor_moisture"] 
                
                # 300 moisture low
                # 700 moisture high
                
                if moisture_level == "much" and current_moisture < 600:
                    watering = True
                if moisture_level == "normal" and current_moisture < 450:
                    watering = True                
                if moisture_level == "less" and current_moisture < 300:
                    watering = True     
                        
            else:
                watering = True
                    
                    
            # start watering
            if watering == True:
                
                WRITE_LOGFILE_SYSTEM("EVENT", "Watering | Plant - " + plant.name + " | Starting") 
                
                if START_PUMP(plant.id) != True:  
                    warnings = True
                      
                pump_running = pump_running + 1

                    
    # check watering process
    while pump_running != 0 or seconds < 60:
        
        time.sleep(10)
    
        # check pump stopped ?
        if MQTT_CHECK_SETTING(plant.mqtt_device.ieeeAddr , "pump_state", "OFF", 15):  
            WRITE_LOGFILE_SYSTEM("SUCCESS", "Watering | Plant - " + plant.name + " | Pump stopped")                              
            pump_running = False

        seconds = seconds + 10
                      
                             
    # pump stopping not confirmed
    if pump_running > 0:
        
        WRITE_LOGFILE_SYSTEM("WARNING", "Watering | Plant - " + plant.name + " | Pump stopping not confimed") 
        warnings     = True


    SET_MQTT_DEVICE_PREVIOUS_SETTING(plant.mqtt_device.ieeeAddr, '"pump_state"="OFF"')
        
    if warnings == True:
        WRITE_LOGFILE_SYSTEM("WARNING", "Watering | Plant - " + plant.name + " | Finished with Warning")               
    else:
        WRITE_LOGFILE_SYSTEM("SUCCESS", "Watering | Plant - " + plant.name + " | Finished")    

                                          
