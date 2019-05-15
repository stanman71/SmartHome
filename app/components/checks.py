from app import app
from app.database.database import *
from app.components.mqtt import *


""" ################### """
"""      check mqtt     """
""" ################### """
 
def MQTT_CHECK():
   MQTT_PUBLISH("SmartHome/mqtt/test", "") 


def MQTT_CHECK_NAME_CHANGED():
            
   input_messages = READ_LOGFILE_MQTT("zigbee2mqtt", "SmartHome/zigbee2mqtt/bridge/log", 5)

   if input_messages != "Message nicht gefunden":
      for input_message in input_messages:
         input_message = str(input_message[2])
  
         data = json.loads(input_message)
            
         if data["type"] == "device_renamed":
            return True
                    
   else:
      return False


""" ############### """
"""  check settings """
""" ############### """


def CHECK_LED_GROUP_SETTINGS(settings):
   list_errors = []

   for element in settings:
      if element.led_id_1 == None or element.led_id_1 == "None":
          list_errors.append(element.name + " >>> fehlende Einstellung >>> LED 1")        
      if element.active_led_2 == "on" and (element.led_id_2 == None or element.led_id_2 == "None"):
          list_errors.append(element.name + " >>> fehlende Einstellung >>> LED 2") 
      if element.active_led_3 == "on" and (element.led_id_3 == None or element.led_id_3 == "None"):
          list_errors.append(element.name + " >>> fehlende Einstellung >>> LED 3") 
      if element.active_led_4 == "on" and (element.led_id_4 == None or element.led_id_4 == "None"):
          list_errors.append(element.name + " >>> fehlende Einstellung >>> LED 4") 
      if element.active_led_5 == "on" and (element.led_id_5 == None or element.led_id_5 == "None"):
          list_errors.append(element.name + " >>> fehlende Einstellung >>> LED 5") 
      if element.active_led_6 == "on" and (element.led_id_6 == None or element.led_id_6 == "None"):
          list_errors.append(element.name + " >>> fehlende Einstellung >>> LED 6") 
      if element.active_led_7 == "on" and (element.led_id_7 == None or element.led_id_7 == "None"):
          list_errors.append(element.name + " >>> fehlende Einstellung >>> LED 7") 
      if element.active_led_8 == "on" and (element.led_id_8 == None or element.led_id_8 == "None"):
          list_errors.append(element.name + " >>> fehlende Einstellung >>> LED 8") 
      if element.active_led_9 == "on" and (element.led_id_9 == None or element.led_id_9 == "None"):
          list_errors.append(element.name + " >>> fehlende Einstellung >>> LED 9")                     

   if list_errors == []:
      return ""
   else:
      return list_errors



def CHECK_PLANTS_SETTINGS():
   list_errors = []

   plants  = GET_ALL_PLANTS()
   entries = GET_ALL_PLANTS()

   # pump missing ?
   for entry in entries:
        if entry.pump_key == "None" or entry.pump_key == None or entry.pump_key == "":
            list_errors.append(entry.name + " >>> keine Pumpe zugeordnet")

   # pumptime missing ?
   for entry in entries:
        if entry.pumptime == "None" or entry.pumptime == None or entry.pumptime == "":
            list_errors.append(entry.name + " >>> keine Pumpedauer eingestellt")

   # check pumps multiple times ?
   for plant in plants:
      for entry in entries:

         if entry.id != plant.id:
            if ((entry.mqtt_device_id == plant.mqtt_device_id and entry.pump_key == plant.pump_key) and  
                (entry.pump_key != None and entry.pump_key != "None" and entry.pump_key != "")):
               list_errors.append(entry.name + " >>> Pumpe mehrmals zugeordnet")

   # sensor missing ?
   for entry in entries:
        if ((entry.sensor_key == "None" or entry.sensor_key == None or entry.sensor_key == "") and 
             entry.control_sensor == "checked"):

            list_errors.append(entry.name + " >>> keinen Sensor zugeordnet")

   # check sensors multiple times ?
   for plant in plants:
      for entry in entries:

         if entry.id != plant.id:
            if ((entry.mqtt_device_id == plant.mqtt_device_id and entry.sensor_key == plant.sensor_key) and  
                (entry.sensor_key != None and entry.sensor_key != "None" and entry.sensor_key != "")):
               list_errors.append(entry.name + " >>> Sensor mehrmals zugeordnet")

   if list_errors == []:
      return ""
   else:
      return list_errors



def CHECK_SENSORDATA_JOBS_SETTINGS():
   list_errors = []

   entries = GET_ALL_SENSORDATA_JOBS()

   # sensor missing ?
   for entry in entries:
        if entry.sensor_key == "None" or entry.sensor_key == None or entry.sensor_key == "":
            list_errors.append(entry.name + " >>> keinen Sensor zugeordnet")

   if list_errors == []:
      return ""
   else:
      return list_errors


""" ######################### """
"""  check scheduler settings """
""" ######################### """

def CHECK_SCHEDULER_TIME_SETTINGS(scheduler_tasks): 
   list_time_errors_general = []  
   error_message_time_settings = ""

   for task in scheduler_tasks:

      if task.option_time == "checked":

         list_time_errors_device = []

         try:
            ### check day
            if "," in task.day:
                  day = task.day.split(",")
                  for element in day:
                     if element.lower() not in ["mo", "tu", "we", "th", "fr", "sa", "su"]:
                        list_time_errors_general.append(task.name + " >>> falsche Zeitangabe >>> Tag") 
                        list_time_errors_device.append(task.name + " >>> falsche Zeitangabe >>> Tag") 
                        break                                 
            else:
                  if task.day.lower() not in ["mo", "tu", "we", "th", "fr", "sa", "su", "*"] and task.day != "*":
                     list_time_errors_general.append(task.name + " >>> falsche Zeitangabe >>> Tag") 
                     list_time_errors_device.append(task.name + " >>> falsche Zeitangabe >>> Tag") 
         except:
            list_time_errors_general.append(task.name + " >>> falsche Zeitangabe >>> Tag")
            list_time_errors_device.append(task.name + " >>> falsche Zeitangabe >>> Tag") 

         try:
            ### check hour
            if "," in task.hour:
                  hour = task.hour.split(",")
                  for element in hour:
                     try:                                   
                        if not (0 <= int(element) <= 24):
                              list_time_errors_general.append(task.name + " >>> falsche Zeitangabe >>> Stunde")
                              list_time_errors_device.append(task.name + " >>> falsche Zeitangabe >>> Stunde") 
                              break   
                     except:
                        list_time_errors_general.append(task.name + " >>> falsche Zeitangabe >>> Stunde")
                        list_time_errors_device.append(task.name + " >>> falsche Zeitangabe >>> Stunde") 
                        break   
            else:
                  try:
                     if not (0 <= int(task.hour) <= 24) and task.hour != "*":
                              list_time_errors_general.append(task.name + " >>> falsche Zeitangabe >>> Stunde") 
                              list_time_errors_device.append(task.name + " >>> falsche Zeitangabe >>> Stunde")
                  except:
                     if task.hour != "*":
                        list_time_errors_general.append(task.name + " >>> falsche Zeitangabe >>> Stunde") 
                        list_time_errors_device.append(task.name + " >>> falsche Zeitangabe >>> Stunde")   

         except:
            list_time_errors_general.append(task.name + " >>> falsche Zeitangabe >>> Stunde")
            list_time_errors_device.append(task.name + " >>> falsche Zeitangabe >>> Stunde")


         try:
            ### check minute
            if "," in task.minute:
                  minute = task.minute.split(",")
                  for element in minute:
                     try:                                   
                        if not (0 <= int(element) <= 60):
                              list_time_errors_general.append(task.name + " >>> falsche Zeitangabe >>> Minute") 
                              list_time_errors_device.append(task.name + " >>> falsche Zeitangabe >>> Minute") 
                              break   
                     except:
                        list_time_errors_general.append(task.name + " >>> falsche Zeitangabe >>> Minute") 
                        list_time_errors_device.append(task.name + " >>> falsche Zeitangabe >>> Minute") 
                        break   
            else:
                  try:
                     if not (0 <= int(task.minute) <= 60) and task.minute != "*":
                              list_time_errors_general.append(task.name + " >>> falsche Zeitangabe >>> Minute")
                              list_time_errors_device.append(task.name + " >>> falsche Zeitangabe >>> Minute")  
                  except:
                     if task.minute != "*":
                        list_time_errors_general.append(task.name + " >>> falsche Zeitangabe >>> Minute") 
                        list_time_errors_device.append(task.name + " >>> falsche Zeitangabe >>> Minute") 
      
         except:
            list_time_errors_general.append(task.name + " >>> falsche Zeitangabe >>> Minute") 
            list_time_errors_device.append(task.name + " >>> falsche Zeitangabe >>> Minute") 

         # add errors for each device to database  

         if list_time_errors_device != []:

            list_time_errors_device = str(list_time_errors_device)
            list_time_errors_device = list_time_errors_device.replace("[", "")
            list_time_errors_device = list_time_errors_device.replace("]", "")
            SET_SCHEDULER_SETTING_TIME_ERRORS(task.id, list_time_errors_device)


   if list_time_errors_general != []:
      error_message_time_settings = list_time_errors_general

   return error_message_time_settings


def CHECK_SCHEDULER_TIMER_SETTINGS(scheduler_tasks):
   list_timer_errors_general = []  
   error_message_timer_settings = ""

   for task in scheduler_tasks:

      if task.option_timer == "checked":

         list_timer_errors_device = []

         try:
            ### check minutes
            if not task.timer_minutes.isdigit():
               list_timer_errors_general.append(task.name + " >>> Ungültige Timerangabe >>> Minuten")
               list_timer_errors_device.append(task.name + " >>> Ungültige Timerangabe >>> Minuten")

            elif int(task.timer_minutes) > 99:
               list_timer_errors_general.append(task.name + " >>> Wert über 99 Minuten")
               list_timer_errors_device.append(task.name + " >>> Wert über 99 Minuten")

            else:
               pass

         except:
            list_timer_errors_general.append(task.name + " >>> Ungültige Timerangabe >>> Minuten")
            list_timer_errors_device.append(task.name + " >>> Ungültige Timerangabe >>> Minuten")

         try:
            ### check seconds
            if not task.timer_seconds.isdigit():
               list_timer_errors_general.append(task.name + " >>> Ungültige Timerangabe >>> Sekunden")
               list_timer_errors_device.append(task.name + " >>> Ungültige Timerangabe >>> Sekunden")

            elif int(task.timer_seconds) > 59:
               list_timer_errors_general.append(task.name + " >>> Wert über 59 Sekunden")
               list_timer_errors_device.append(task.name + " >>> Wert über 59 Sekunden")

            else:
               pass

         except:
            list_timer_errors_general.append(task.name + " >>> Ungültige Timerangabe >>> Sekunden")
            list_timer_errors_device.append(task.name + " >>> Ungültige Timerangabe >>> Sekunden")

         try:
            ### check endtask
            list_task_errors = CHECK_TASK_OPERATION(task.timer_endtask, task.name, "timer")

            if list_task_errors != []:

               # merge errors to device list
               list_timer_errors_device = list_timer_errors_device + list_task_errors

               # merge errors to general list
               list_timer_errors_general = list_timer_errors_general + list_task_errors

         except:
            pass

         # add errors for each device to database

         if list_timer_errors_device != []:

            list_timer_errors_device = str(list_timer_errors_device)
            list_timer_errors_device = list_timer_errors_device.replace("[", "")
            list_timer_errors_device = list_timer_errors_device.replace("]", "")
            SET_SCHEDULER_SETTING_TIMER_ERRORS(task.id, list_timer_errors_device)


   if list_timer_errors_general == []:
      error_message_timer_settings = ""
   else:
      error_message_timer_settings = list_timer_errors_general

   return error_message_timer_settings



def CHECK_SCHEDULER_SENSOR_SETTINGS(scheduler_tasks): 
   list_sensor_errors_general = []  
   error_message_sensor_settings = ""

   for task in scheduler_tasks:

      if task.option_sensors == "checked":

         list_sensor_errors_device = []

         # check mqtt devices
         
         if task.mqtt_device_id_1 == "None" or task.mqtt_device_id_1 == "" or task.mqtt_device_id_1 == None:
            list_sensor_errors_general.append(task.name + " >>> fehlende Einstellung >>> MQTT-Gerät 1") 
            list_sensor_errors_device.append(task.name + " >>> fehlende Einstellung >>> MQTT-Gerät 1")

         if task.mqtt_device_id_2 == "None" or task.mqtt_device_id_2 == "" or task.mqtt_device_id_2 == None:
            if task.operator_main_1 != "None" and task.operator_main_1 != None:
               list_sensor_errors_general.append(task.name + " >>> fehlende Einstellung >>> MQTT-Gerät 2") 
               list_sensor_errors_device.append(task.name + " >>> fehlende Einstellung >>> MQTT-Gerät 2")

         if task.mqtt_device_id_3 == "None" or task.mqtt_device_id_3 == "" or task.mqtt_device_id_3 == None:
            if task.operator_main_1 != "None" and task.operator_main_1 != None:
               if task.operator_main_2 != "None" and task.operator_main_2 != None:
                  list_sensor_errors_general.append(task.name + " >>> fehlende Einstellung >>> MQTT-Gerät 3")  
                  list_sensor_errors_device.append(task.name + " >>> fehlende Einstellung >>> MQTT-Gerät 3")           

         # check sensors
         
         if task.sensor_key_1 == "None" or task.sensor_key_1 == None:
            list_sensor_errors_general.append(task.name + " >>> fehlende Einstellung >>> Sensor 1") 
            list_sensor_errors_device.append(task.name + " >>> fehlende Einstellung >>> Sensor 1")
            
         if task.operator_main_1 != "None" and task.operator_main_1 != None:
            if task.sensor_key_2 == "None" or task.sensor_key_2 == None:
               list_sensor_errors_general.append(task.name + " >>> fehlende Einstellung >>> Sensor 2")  
               list_sensor_errors_device.append(task.name + " >>> fehlende Einstellung >>> Sensor 2") 
               
         if task.operator_main_2 != "None" and task.operator_main_2 != None:
            if task.sensor_key_3 == "None" or task.sensor_key_3 == None:
               list_sensor_errors_general.append(task.name + " >>> fehlende Einstellung >>> Sensor 3") 
               list_sensor_errors_device.append(task.name + " >>> fehlende Einstellung >>> Sensor 3")

         # check operators
         
         if task.operator_main_1 != "<" and task.operator_main_1 != ">" and task.operator_main_1 != "=":
            if task.operator_1 == "" or task.operator_1 == "None" or task.operator_1 == None: 
               list_sensor_errors_general.append(task.name + " >>> fehlende Einstellung >>> Operator 1")
               list_sensor_errors_device.append(task.name + " >>> fehlende Einstellung >>> Operator 1") 
         
         if task.operator_main_1 == "and" or task.operator_main_1 == "or":
            if task.operator_2 == "None" or task.operator_2 == "" or task.operator_2 == None: 
               list_sensor_errors_general.append(task.name + " >>> fehlende Einstellung >>> Operator 2") 
               list_sensor_errors_device.append(task.name + " >>> fehlende Einstellung >>> Operator 2")  

         if task.operator_main_2 == "and" or task.operator_main_2 == "or":
            if task.operator_3 == "None" or task.operator_3 == "" or task.operator_3 == None: 
               list_sensor_errors_general.append(task.name + " >>> fehlende Einstellung >>> Operator 3")
               list_sensor_errors_device.append(task.name + " >>> fehlende Einstellung >>> Operator 3")  

         # check values
         
         if task.operator_main_1 != "<" and task.operator_main_1 != ">" and task.operator_main_1 != "=":
            if task.value_1 == "" or task.value_1 == "None" or task.value_1 == None: 
               list_sensor_errors_general.append(task.name + " >>> fehlende Einstellung >>> Vergleichswert 1") 
               list_sensor_errors_device.append(task.name + " >>> fehlende Einstellung >>> Vergleichswert 1")      
            elif (task.operator_1 == "<" or task.operator_1 == ">") and not task.value_1.isdigit():
               list_sensor_errors_general.append(task.name + 
               " >>> ungültiger Eintrag >>> Vergleichswert 1 >>> nur Zahlen können mit dem gewählten Operator verwendet werden")
               list_sensor_errors_device.append(task.name + 
               " >>> ungültiger Eintrag >>> Vergleichswert 1 >>> nur Zahlen können mit dem gewählten Operator verwendet werden") 

         if task.operator_main_1 == "and" or task.operator_main_1 == "or":
            if task.value_2 == "" or task.value_2 == "None" or task.value_2 == None:
               list_sensor_errors_general.append(task.name + " >>> fehlende Einstellung >>> Vergleichswert 2")
               list_sensor_errors_device.append(task.name + " >>> fehlende Einstellung >>> Vergleichswert 2")
            elif (task.operator_2 == "<" or task.operator_2 == ">") and not task.value_2.isdigit():
               list_sensor_errors_general.append(task.name + 
               " >>> ungültiger Eintrag >>> Vergleichswert 2 >>> nur Zahlen können mit dem gewählten Operator verwendet werden")   
               list_sensor_errors_device.append(task.name + 
               " >>> ungültiger Eintrag >>> Vergleichswert 2 >>> nur Zahlen können mit dem gewählten Operator verwendet werden")                  

         if task.operator_main_2 == "and" or task.operator_main_2 == "or":
            if task.value_3 == "" or task.value_3 == "None" or task.value_3 == None:
               list_sensor_errors_general.append(task.name + " >>> fehlende Einstellung >>> Vergleichswert 3")
               list_sensor_errors_device.append(task.name + " >>> fehlende Einstellung >>> Vergleichswert 3")
            elif (task.operator_3 == "<" or task.operator_3 == ">") and not task.value_3.isdigit():
               list_sensor_errors_general.append(task.name + 
               " >>> ungültiger Eintrag >>> Vergleichswert 3 >>> nur Zahlen können mit dem gewählten Operator verwendet werden")     
               list_sensor_errors_device.append(task.name + 
               " >>> ungültiger Eintrag >>> Vergleichswert 3 >>> nur Zahlen können mit dem gewählten Operator verwendet werden")    

         # add errors for each device to database

         if list_sensor_errors_device != []:

            list_sensor_errors_device = str(list_sensor_errors_device)
            list_sensor_errors_device = list_sensor_errors_device.replace("[", "")
            list_sensor_errors_device = list_sensor_errors_device.replace("]", "")
            SET_SCHEDULER_SETTING_SENSOR_ERRORS(task.id, list_sensor_errors_device)


   if list_sensor_errors_general == []:
      error_message_sensor_settings = ""
   else:
      error_message_sensor_settings = list_sensor_errors_general

   return error_message_sensor_settings


def CHECK_SCHEDULER_EXPANDED_SETTINGS(scheduler_tasks):
   list_expanded_errors_general = []  
   error_message_expanded_settings = ""

   for task in scheduler_tasks:

      if task.option_expanded == "checked":

         list_expanded_errors_device = []

         if task.expanded_home == "checked" or task.expanded_away == "checked":

            # search for wrong chars
            if task.expanded_ip_adresses != "None":
               for element in task.expanded_ip_adresses:
                  if not element.isdigit() and element != "." and element != ",":
                     list_expanded_errors_device.append(task.name + " >>> Ungültige IP-Adressen")
                     break

               # merge errors to general list
               list_expanded_errors_general = list_expanded_errors_general + list_expanded_errors_device         


         # add errors for each device to database
         if list_expanded_errors_device != []:
            list_expanded_errors_device = str(list_expanded_errors_device)
            list_expanded_errors_device = list_expanded_errors_device.replace("[", "")
            list_expanded_errors_device = list_expanded_errors_device.replace("]", "")
            SET_SCHEDULER_SETTING_EXPANDED_ERRORS(task.id, list_expanded_errors_device)


   if list_expanded_errors_general == []:
      error_message_expanded_settings = ""
   else:
      error_message_expanded_settings = list_expanded_errors_general

   return error_message_expanded_settings



""" ################### """
"""  speech recognition """
""" ################### """

def CHECK_SPEECH_RECOGNITION_PROVIDER_SETTINGS(settings):
   list_errors = []

   if settings.snowboy_hotword == "":
      list_errors.append("Kein Snowboy Hotword angegeben") 
   if settings.speech_recognition_provider == "":
      list_errors.append("Keinen Provider angegeben")     
   if settings.speech_recognition_provider_key == "":
      list_errors.append("Keinen Key angegeben")
      
   # check hotword files exist
   hotword_file = GET_SPEECH_RECOGNITION_PROVIDER_SETTINGS().snowboy_hotword
   
   if hotword_file not in GET_ALL_HOTWORD_FILES():
      list_errors.append("Snowboy Hotword " + hotword_file + " nicht vorhanden")


   if list_errors == []:
      return ""
   else:
      return list_errors   


def CHECK_SPEECH_RECOGNITION_PROVIDER_KEYWORDS(tasks):
   list_errors = []

   # get list with all keywords
   list_all_keywords = []
   
   for task in tasks:
      list_keywords = task.keywords.split(",")
      
      for keyword in list_keywords:
         keyword = keyword.replace(" ", "")
         list_all_keywords.append(keyword)
   
   # search for double keywords
   for task in tasks:
      
      if task.keywords != "":
         keywords = task.keywords.split(",")
         
         for keyword in keywords:
            keyword = keyword.replace(" ", "")
            num = list_all_keywords.count(keyword)
         
            if num > 1:
               list_errors.append(task.task + " >>> Schlüsselwort doppelt verwendet >>> " + keyword) 
         
   if list_errors == []:
      return ""
   else:
      return list_errors


""" ################### """
"""     check tasks     """
""" ################### """

def CHECK_TASKS(tasks, task_type):
   list_task_errors_general = []

   for element in tasks:

      list_task_errors = CHECK_TASK_OPERATION(element.task, element.name, task_type)

      if list_task_errors != []:

         # merge errors to general list
         list_task_errors_general = list_task_errors_general + list_task_errors

         # save errors for each scheduler task 
         if task_type == "scheduler":    
            list_task_errors = str(list_task_errors)
            list_task_errors = list_task_errors.replace("[", "")
            list_task_errors = list_task_errors.replace("]", "")
            SET_SCHEDULER_SETTING_TASK_ERRORS(element.id, list_task_errors)         


   if list_task_errors_general == []:
      return ""
   else:
      return list_task_errors_general



def CHECK_TASK_OPERATION(task, name, task_type):
   list_task_errors = []

   try:

      # check snowboy_active
      if task == "snowboy_active" and task_type == "snowboy":
         return list_task_errors

      # check start_scene
      if "scene" in task:
         if ":" in task:
            task = task.split(":") 

            # check group setting 
            try:
               group_exist = False

               input_group_name = task[1]
               input_group_name = input_group_name.lower()

               # get exist group names and lower the letters
               all_exist_groups = GET_ALL_LED_GROUPS()
               
               for exist_group in all_exist_groups:
                  
                  exist_group_name       = exist_group.name
                  exist_group_name_lower = exist_group_name.lower()
                  
                  # compare the formated names
                  if input_group_name == exist_group_name_lower: 
                     group_exist = True
                     
               if group_exist == True:
                  pass
               else:
                  list_task_errors.append(name + " >>> LED Gruppe nicht vorhanden >>> " + task[1])

            except:
               list_task_errors.append(name + " >>> fehlende Einstellung >>> LED Gruppe")

            # check scene setting    
            try:
               scene_exist = False

               input_scene_name = task[2]
               input_scene_name = input_scene_name.lower()

               # get exist scene names and lower the letters
               all_exist_scenes = GET_ALL_LED_SCENES()
               
               for exist_scene in all_exist_scenes:
                  
                  exist_scene_name       = exist_scene.name
                  exist_scene_name_lower = exist_scene_name.lower()
                  
                  # compare the formated names
                  if input_scene_name == exist_scene_name_lower: 
                     scene_exist = True
                     
               if scene_exist == True:
                  pass
                  
               else:
                  list_task_errors.append(name + " >>> LED Szene nicht vorhanden >>> " + task[2])

            except:
               list_task_errors.append(name + " >>> fehlende Einstellung >>> LED Szene")

            # check global brightness    
            try:
               if task[3].isdigit():
                  if 1 <= int(task[3]) <= 100:
                     return list_task_errors

                  else:
                     list_task_errors.append(name + " >>> ungültiger Wertebereich >>> Globale Helligkeit") 
                     return list_task_errors    

               else:
                  list_task_errors.append(name + " >>> ungültige Einstellung >>> Globale Helligkeit")
                  return list_task_errors

            except:
               return list_task_errors

         else:
            list_task_errors.append(name + " >>> Ungültige Formatierung")
            return list_task_errors

      # check start_program
      if "program" in task:
         if ":" in task:
            task = task.split(":") 

            # check group setting
            try:
               if GET_LED_GROUP_BY_NAME(task[1]):
                  pass
                  
               else:
                  list_task_errors.append(name + " >>> LED Gruppe nicht vorhanden >>> " + task[1])   
                                    
            except:
               list_task_errors.append(name + " >>> fehlende Einstellung >>> LED Gruppe")      

            # check program setting    
            try:
               if GET_LED_PROGRAM_BY_NAME(task[2]):
                  return list_task_errors
                  
               else:
                  list_task_errors.append(name + " >>> LED Programm nicht vorhanden >>> " + task[2])
                  return list_task_errors
                  
            except:
               list_task_errors.append(name + " >>> fehlende Einstellung >>> LED Programm")    
               return list_task_errors

         else:
            list_task_errors.append(name + " >>> Ungültige Formatierung")
            return list_task_errors

      # check led_off
      if "led_off" in task:
         if ":" in task:
            task = task.split(":")

            # check group setting
            if task[1] == "group":

               # get input group names and lower the letters
               try:
                     list_groups = task[2].split(",")
               except:
                     list_groups = [task[2]]

               for input_group_name in list_groups:
                     
                  input_group_name = input_group_name.replace(" ", "")
                  input_group_name = input_group_name.lower()

                  # get exist group names and lower the letters
                  try:
                     all_exist_group = GET_ALL_LED_GROUPS()
                     
                     group_exist = False
                     
                     for exist_group in all_exist_group:
                        
                        exist_group_name = exist_group.name
                        exist_group_name = exist_group_name.lower()
                        
                        # compare the formated names
                        if input_group_name == exist_group_name: 
                           group_exist = True
                        
                     if group_exist == True:
                        pass
                        
                     else:
                        list_task_errors.append(name + " >>> LED Gruppe nicht vorhanden >>> " + input_group_name)  
                     
                  except:
                     list_task_errors.append(name + " >>> fehlende Einstellung >>> LED Gruppe")
                     return list_task_errors

               return list_task_errors

            # check turn off all leds
            try:
               if task[1] == "all": 
                  return list_task_errors
                  
            except:
               pass
            
            list_task_errors.append(name + " >>> Ungültige Eingabe >>> 'all' oder 'group'")
            return list_task_errors  

         else:
            list_task_errors.append(name + " >>> Ungültige Formatierung")
            return list_task_errors

      # check watering_plants
      if task == "watering_plants" and task_type == "scheduler":
         return list_task_errors

      # check save_database         
      if task == "save_database" and task_type == "scheduler":
         return list_task_errors

      # check mqtt_update_devices
      if task == "mqtt_update_devices" and task_type == "scheduler":
         return list_task_errors

      # check request_sensordata
      if "request_sensordata" in task and task_type == "scheduler":
         if ":" in task:
            task = task.split(":")

            # check job-id setting
            try:          
               if GET_SENSORDATA_JOB_BY_ID(int(task[1])):
                  return list_task_errors

               else:
                  list_task_errors.append(name + " >>> Job-ID nicht vorhanden >>> " + task[1])
                  return list_task_errors   

            except:
               list_task_errors.append(name + " >>> fehlende Einstellung >>> Job-ID") 
               return list_task_errors

         else:
            list_task_errors.append(name + " >>> Ungültige Formatierung")
            return list_task_errors

      # nothing found
      list_task_errors.append(name + " >>> Ungültige Aufgabe") 
      return list_task_errors
   
   except:
      list_task_errors.append("MISSING NAME >>> Ungültige Aufgabe") 
      return list_task_errors

