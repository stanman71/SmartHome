from flask import render_template, redirect, url_for, request, send_from_directory
from flask_login import login_required, current_user
from functools import wraps
import os
import datetime
import json
import sys

from app import app
from app.components.led_control import *
from app.database.database import *
from app.components.file_management import *
from app.components.email import SEND_EMAIL
from app.components.mqtt_functions import *
from app.components.checks import *


# create role "superuser"
def superuser_required(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if current_user.role == "superuser":
            return f(*args, **kwargs)
        else:
            return redirect(url_for('login'))
    return wrap


""" ############# """
""" mqtt settings """
""" ############# """

@app.route('/dashboard/settings/mqtt', methods=['GET', 'POST'])
@login_required
@superuser_required
def dashboard_settings_mqtt():   
    error_message = ""
    error_message_mqtt = ""
    error_message_table = ""
    mqtt_device_name = ""   
    check_value_mqtt   = ["", ""]

    if GET_ERROR_LIST() is not "":
        error_message_table = GET_ERROR_LIST()
        SET_ERROR_LIST("")

    if request.method == "POST":     
        # change mqtt settings   
        if request.form.get("set_setting_mqtt") is not None:
            setting_mqtt = str(request.form.get("radio_mqtt"))
            SET_GLOBAL_SETTING_VALUE("mqtt", setting_mqtt)

    # change radio check  
    mqtt_setting = GET_GLOBAL_SETTING_VALUE("mqtt")    
    if mqtt_setting == "True":
        check_value_mqtt[0] = "checked = 'on'"
        check_value_mqtt[1] = ""
    else:
        check_value_mqtt[0] = ""
        check_value_mqtt[1] = "checked = 'on'"

    if mqtt_setting == "True":

        # check mqtt
        try:
            MQTT_CHECK()
        except Exception as e:
            error_message_mqtt = "Fehler in MQTT: " + str(e)
            WRITE_LOGFILE_SYSTEM("ERROR", "MQTT | " + str(e)) 

        # change settings
        if request.form.get("change_settings") != None:    
            for i in range (1,26):
                if request.form.get("set_name_" + str(i)) != "" and request.form.get("set_name_" + str(i)) != None:
                                
                    # rename devices                   
                    new_name = request.form.get("set_name_" + str(i))
                    old_name = GET_MQTT_DEVICE_BY_ID(i).name

                    if new_name != old_name:          
                        if not GET_MQTT_DEVICE_BY_NAME(new_name):  
                            ieeeAddr = GET_MQTT_DEVICE_BY_ID(i).ieeeAddr                  
                            SET_MQTT_DEVICE_NAME(ieeeAddr, new_name)                         
                        else: 
                            error_message_table = "Name bereits vergeben >>> " + new_name

        # update device list
        if request.form.get("mqtt_update_devices") != None:
            error_message_table = MQTT_UPDATE_DEVICES("mqtt")
            
        # reset logfile
        if request.form.get("reset_logfile") != None: 
            print("OK")
            RESET_LOGFILE("log_mqtt")   
            

    mqtt_device_list = GET_ALL_MQTT_DEVICES("mqtt")
    
    timestamp = str(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")) 

    return render_template('dashboard_settings_mqtt.html',                    
                            error_message=error_message,
                            error_message_mqtt=error_message_mqtt,
                            error_message_table=error_message_table,
                            mqtt_device_name=mqtt_device_name,
                            mqtt_setting=mqtt_setting,
                            check_value_mqtt=check_value_mqtt,
                            mqtt_device_list=mqtt_device_list,
                            active01="active",
                            timestamp=timestamp,
                            )
     
# remove mqtt device
@app.route('/dashboard/settings/mqtt/delete/<int:id>')
@login_required
@superuser_required
def remove_mqtt_device(id):
    DELETE_MQTT_DEVICE(id)
    return redirect(url_for('dashboard_settings_mqtt'))
     
     
# download mqtt logfile
@app.route('/dashboard/settings/mqtt/download/<path:filepath>')
@login_required
@superuser_required
def download_mqtt_logfile(filepath): 
    try:
        path = GET_PATH() + "/logs/"     
        WRITE_LOGFILE_SYSTEM("EVENT", "File | /logs/" + filepath + " | downloaded")
        return send_from_directory(path, filepath)
    except Exception as e:
        WRITE_LOGFILE_SYSTEM("ERROR", "File | /logs/" + filepath + " | " + str(e))
             

""" #################### """
""" zigbee2mqtt settings """
""" #################### """

@app.route('/dashboard/settings/zigbee2mqtt', methods=['GET', 'POST'])
@login_required
@superuser_required
def dashboard_settings_zigbee2mqtt():
    error_message = ""
    error_message_zigbee2mqtt = ""
    error_message_table = ""
    check_value_zigbee2mqtt = ["", ""]
    check_value_pairing = ["", ""]
    zigbee_topology_show = False

    if request.method == "POST":     
        # change mqtt settings   
        if request.form.get("set_setting_zigbee2mqtt") is not None:
            setting_zigbee2mqtt = str(request.form.get("radio_zigbee2mqtt"))
            SET_GLOBAL_SETTING_VALUE("zigbee2mqtt", setting_zigbee2mqtt)

    # change radio check  
    zigbee2mqtt_setting = GET_GLOBAL_SETTING_VALUE("zigbee2mqtt")    
    if zigbee2mqtt_setting == "True":
        check_value_zigbee2mqtt[0] = "checked = 'on'"
        check_value_zigbee2mqtt[1] = ""
    else:
        check_value_zigbee2mqtt[0] = ""
        check_value_zigbee2mqtt[1] = "checked = 'on'"


    if zigbee2mqtt_setting == "True":

        if GET_ERROR_LIST() is not "":
            error_message_table = GET_ERROR_LIST()
            SET_ERROR_LIST("")
        
        error_message_zigbee2mqtt = MQTT_PUBLISH("SmartHome/zigbee2mqtt/bridge/config/", "")
        
        if request.method == 'POST':

            # change name
            if request.form.get("change_settings") != None:
                
                for i in range (1,26):

                    if (request.form.get("set_name_" + str(i)) != "" and request.form.get("set_name_" + str(i)) != None):
                            
                        new_name = request.form.get("set_name_" + str(i))
                        old_name = GET_MQTT_DEVICE_BY_ID(i).name 
                        
                        if new_name != old_name:
                        
                            # name already exist
                            if not GET_MQTT_DEVICE_BY_NAME(new_name):

                                # no connection to mqtt
                                if MQTT_PUBLISH("SmartHome/zigbee2mqtt/bridge/config/rename", 
                                                '{"old": "' + old_name + '", "new": "' + new_name + '"}') != "Keine Verbindung zu MQTT":

                                    time.sleep(3)

                                    # error in zigbee2mqtt
                                    if MQTT_CHECK_NAME_CHANGED():       
                                        ieeeAddr = GET_MQTT_DEVICE_BY_ID(i).ieeeAddr                  
                                        SET_MQTT_DEVICE_NAME(ieeeAddr, new_name)  

                                    else:
                                        error_message_table = "Name konnte in ZigBee2MQTT nicht verändert werden"
                                        MQTT_UPDATE_DEVICES("zigbee2mqtt")

                                else:
                                    error_message_table = "Ohne eine Verbindung zu MQTT können die Namen der Geräte nicht verändert werden !"
                                
                            else:
                                error_message_table = "Name bereits vergeben >>> " + new_name

            # update device list
            if request.form.get("update_zigbee2mqtt_devices") is not None:
                error_message_table = MQTT_UPDATE_DEVICES("zigbee2mqtt")

            # request zigbee topology
            if request.form.get("request_zigbee_topology") is not None: 
                MQTT_PUBLISH("SmartHome/zigbee2mqtt/bridge/networkmap", "graphviz")
                zigbee_topology_show = True
                time.sleep(1)

            # change pairing setting
            if request.form.get("set_pairing") is not None: 
                setting_pairing = str(request.form.get("radio_pairing"))
                SET_ZIGBEE2MQTT_PAIRING(setting_pairing)

            # reset logfile
            if request.form.get("reset_logfile") is not None: 
                RESET_LOGFILE("log_zigbee2mqtt")
     
        # set pairing checkbox  
        pairing_setting = GET_ZIGBEE2MQTT_PAIRING()    
        if pairing_setting == "True":
            check_value_pairing[0] = "checked = 'on'"
            check_value_pairing[1] = ""        
            MQTT_PUBLISH("SmartHome/zigbee2mqtt/bridge/config/permit_join", "true")  
        else:
            check_value_pairing[0] = ""
            check_value_pairing[1] = "checked = 'on'"        
            MQTT_PUBLISH("SmartHome/zigbee2mqtt/bridge/config/permit_join", "false")

        if READ_LOGFILE_MQTT("zigbee2mqtt", "",5) != "Message nicht gefunden":
            error_message_zigbee2mqtt = READ_LOGFILE_MQTT("zigbee2mqtt", "",5) 
            WRITE_LOGFILE_SYSTEM("ERROR", "ZigBee2MQTT | No connection")

    zigbee2mqtt_device_list = GET_ALL_MQTT_DEVICES("zigbee2mqtt")

    timestamp = str(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))

    return render_template('dashboard_settings_zigbee2mqtt.html',
                            error_message=error_message,
                            error_message_zigbee2mqtt=error_message_zigbee2mqtt,
                            error_message_table=error_message_table,
                            check_value_zigbee2mqtt=check_value_zigbee2mqtt,  
                            check_value_pairing=check_value_pairing,
                            zigbee2mqtt_device_list=zigbee2mqtt_device_list, 
                            zigbee2mqtt_setting=zigbee2mqtt_setting, 
                            zigbee_topology_show=zigbee_topology_show,                 
                            active02="active",
                            timestamp=timestamp,
                            )


# remove zigbee2mqtt device
@app.route('/dashboard/settings/zigbee2mqtt/delete/<int:id>')
@login_required
@superuser_required
def remove_zigbee2mqtt_device(id):
    MQTT_PUBLISH("SmartHome/zigbee2mqtt/bridge/config/remove", GET_MQTT_DEVICE_BY_ID(id).name) 
    DELETE_MQTT_DEVICE(id)
    return redirect(url_for('dashboard_settings_zigbee2mqtt'))


# download zigbee2mqtt logfile
@app.route('/dashboard/settings/zigbee2mqtt/download/<path:filepath>')
@login_required
@superuser_required
def download_zigbee2mqtt_logfile(filepath): 
    try:
        path = GET_PATH() + "/logs/"     
        WRITE_LOGFILE_SYSTEM("EVENT", "File | /logs/" + filepath + " | downloaded")
        return send_from_directory(path, filepath)
    except Exception as e:
        WRITE_LOGFILE_SYSTEM("ERROR", "File | /logs/" + filepath + " | " + str(e))             


""" ############### """
"""  speechcontrol  """
""" ############### """

@app.route('/dashboard/settings/speechcontrol', methods=['GET', 'POST'])
@login_required
@superuser_required
def dashboard_settings_speechcontrol():
    error_message = ""
    error_message_snowboy = ""
    error_message_table = ""
    error_message_snowboy_tasks = ""
    error_message_fileupload = ""
    error_message_hotword = ""
    error_message_speech_recognition_provider_tasks = ""
    error_message_speech_recognition_provider_settings = ""
    sensitivity = ""
    delay = ""
    microphone = ""
    check_value_speechcontrol = ["", "", ""]
    snowboy_name = ""
    snowboy_task = ""   
    speech_recognition_provider_task = ""
    speech_recognition_provider_keywords = ""
    speech_recognition_provider_parameters = ""
    

    if request.method == "POST":     
        # change speech_control settings   
        if request.form.get("radio_speechcontrol") is not None:
            setting_speechcontrol = str(request.form.get("radio_speechcontrol"))
            SET_GLOBAL_SETTING_VALUE("speechcontrol", setting_speechcontrol) 

    # change radio check    
    if GET_GLOBAL_SETTING_VALUE("speechcontrol") == "snowboy":
        check_value_speechcontrol[0] = "checked = 'on'"
        check_value_speechcontrol[1] = ""
        check_value_speechcontrol[2] = ""
    elif GET_GLOBAL_SETTING_VALUE("speechcontrol") == "speech_recognition_provider":
        check_value_speechcontrol[0] = ""
        check_value_speechcontrol[1] = "checked = 'on'"
        check_value_speechcontrol[2] = ""
    else:
        check_value_speechcontrol[0] = ""
        check_value_speechcontrol[1] = ""
        check_value_speechcontrol[2] = "checked = 'on'"

    ##########################
    # general snowboy settings
    ##########################

    if GET_GLOBAL_SETTING_VALUE("speechcontrol") == "snowboy" or GET_GLOBAL_SETTING_VALUE("speechcontrol") == "speech_recognition_provider":

        # check snowboy
        def START_SNOWBOY():
            from app.speechcontrol.snowboy.snowboy import SNOWBOY_START
            SNOWBOY_START("snowboy")
          
        try:
            START_SNOWBOY()
        except Exception as e:  
            if "signal only works in main thread" not in str(e):      
                error_message_snowboy = "Fehler in SnowBoy: " + str(e)
                WRITE_LOGFILE_SYSTEM("ERROR", "Snowboy | " + str(e)) 
                
        if request.method == 'POST':

            # change snowboy settings
            if request.form.get("change_snowboy_settings") is not None: 
                
                # check sensitivity
                sensitivity = request.form.get("set_sensitivity")
                if sensitivity != "":     
                    sensitivity = request.form.get("set_sensitivity") 
                else:
                    sensitivity = GET_SNOWBOY_SETTINGS().sensitivity
                    
                # check delay
                delay = request.form.get("set_delay")     
                if delay != "":     
                    delay = request.form.get("set_delay") 
                else:
                    delay = GET_SNOWBOY_SETTINGS().delay  

                # set microphone
                microphone = request.form.get("set_microphone")                                            
             
                SET_SNOWBOY_SETTINGS(sensitivity, delay, microphone)  

            #########
            # snowboy
            #########

            # add new snowboy task
            if request.form.get("add_snowboy_task") is not None:

                if request.form.get("set_snowboy_name") == "":
                    error_message = "Kein Name angegeben"
                    snowboy_task = request.form.get("set_snowboy_task")
                elif request.form.get("set_snowboy_task") == "":
                    error_message = "Keine Aufgabe angegeben"  
                    snowboy_name = request.form.get("set_snowboy_name")  
                else:         
                    snowboy_name  = request.form.get("set_snowboy_name")
                    snowboy_task  = request.form.get("set_snowboy_task")
                    error_message = ADD_SNOWBOY_TASK(snowboy_name, snowboy_task)

                    snowboy_name = ""
                    snowboy_task = "" 

            # change snowboy tasks
            if request.form.get("change_snowboy_tasks") != None: 
                for i in range (1,26):

                    if request.form.get("set_snowboy_name_" + str(i)) != None:  
                        
                        # check snowboy name
                        if (request.form.get("set_snowboy_name_" + str(i)) != "" and 
                            GET_SNOWBOY_TASK_BY_NAME(request.form.get("set_snowboy_name_" + str(i))) == None):
                            snowboy_name = request.form.get("set_snowboy_name_" + str(i)) 
                            
                        elif request.form.get("set_snowboy_name_" + str(i)) == GET_SNOWBOY_TASK_BY_ID(i).name:
                            snowboy_name = GET_SNOWBOY_TASK_BY_ID(i).name                        
                            
                        else:
                            snowboy_name = GET_SNOWBOY_TASK_BY_ID(i).name 
                            error_message_table = "Ungültige Eingabe (leeres Feld / Name schon vergeben"                          
                        
                        # check task
                        if request.form.get("set_snowboy_task_" + str(i)) != "":
                            snowboy_task = request.form.get("set_snowboy_task_" + str(i)) 
                        
                        else:
                            snowboy_task = GET_SNOWBOY_TASK_BY_ID(i).task 
                            error_message_table = "Ungültige Eingabe (leeres Feld / Name schon vergeben"   
                                           
                        SET_SNOWBOY_TASK(i, snowboy_name, snowboy_task)

            #############################
            # speech recognition provider
            #############################

            # add new speech_recognition_provider task
            if request.form.get("add_speech_recognition_provider_task") is not None:

                if request.form.get("set_speech_recognition_provider_task") == "":
                    error_message = "Keine Aufgabe angegeben"
                    speech_recognition_provider_keywords   = request.form.get("set_speech_recognition_provider_keywords")
                    speech_recognition_provider_parameters = request.form.get("set_speech_recognition_provider_parameters")
                else:         
                    speech_recognition_provider_task       = request.form.get("set_speech_recognition_provider_task")
                    speech_recognition_provider_keywords   = request.form.get("set_speech_recognition_provider_keywords")
                    speech_recognition_provider_parameters = request.form.get("set_speech_recognition_provider_parameters")
                    
                    error_message = ADD_SPEECH_RECOGNITION_PROVIDER_TASK(speech_recognition_provider_task, speech_recognition_provider_keywords, speech_recognition_provider_parameters)
                   
                    speech_recognition_provider_task = ""
                    speech_recognition_provider_keywords = ""
                    speech_recognition_provider_parameters = ""

            # change speech_recognition_provider tasks
            if request.form.get("change_speech_recognition_provider_tasks") != None: 
                for i in range (1,26):

                    if request.form.get("set_speech_recognition_provider_task_" + str(i)) != None:  
                        
                        # check task
                        if request.form.get("set_speech_recognition_provider_task_" + str(i)) != "":
                            speech_recognition_provider_task = request.form.get("set_speech_recognition_provider_task_" + str(i)) 
                        
                        else:
                            speech_recognition_provider_task = GET_SPEECH_RECOGNITION_PROVIDER_TASK_BY_ID(i).task 
                            error_message_table = "Ungültige Eingabe (leeres Feld / Aufgabe schon vorhanden)"   
                                                                  
                        # check keywords
                        if request.form.get("set_speech_recognition_provider_keywords_" + str(i)) != "":
                            speech_recognition_provider_keywords = request.form.get("set_speech_recognition_provider_keywords_" + str(i)) 
                        
                        else:
                            speech_recognition_provider_keywords = GET_SPEECH_RECOGNITION_PROVIDER_TASK_BY_ID(i).keywords 
                            error_message_table = "Ungültige Eingabe (leeres Feld / Aufgabe schon vorhanden)"    
                            
                        speech_recognition_provider_parameters = request.form.get("set_speech_recognition_provider_parameters_" + str(i)) 
                    
                                           
                        SET_SPEECH_RECOGNITION_PROVIDER_TASK(i, speech_recognition_provider_task, speech_recognition_provider_keywords, speech_recognition_provider_parameters)

            # change speech_recognition_provider settings
            if request.form.get("set_speech_recognition_provider_settings") != None: 
                
                snowboy_hotword                      = request.form.get("set_snowboy_hotword")        
                speech_recognition_provider          = request.form.get("set_speech_recognition_provider")
                speech_recognition_provider_username = request.form.get("set_speech_recognition_provider_username")
                speech_recognition_provider_key      = request.form.get("set_speech_recognition_provider_key")

                SET_SPEECH_RECOGNITION_PROVIDER_SETTINGS(snowboy_hotword, speech_recognition_provider, 
                                                  speech_recognition_provider_username, speech_recognition_provider_key)


            #########################################
            # snowboy and speech recognition provider
            #########################################
                    
            if request.form.get("file_upload") is not None:
                # file upload
                if 'file' not in request.files:
                    error_message_fileupload = "Keine Datei angegeben"
                else:
                    file = request.files['file']
                    error_message_fileupload = UPLOAD_HOTWORD_FILE(file)


    # snowboy settings
    speechcontrol_setting = GET_GLOBAL_SETTING_VALUE("speechcontrol")
    sensitivity           = GET_SNOWBOY_SETTINGS().sensitivity
    delay                 = GET_SNOWBOY_SETTINGS().delay
    microphone            = GET_SNOWBOY_SETTINGS().microphone

    dropdown_list_microphone_options = ["ReSpeaker 2-Mics Pi HAT", "ReSpeaker Mic 4 Array v2.0", "Other"]   

    # snowboy only
    snowboy_task_list           = GET_ALL_SNOWBOY_TASKS()
    hotword_file_list           = GET_ALL_HOTWORD_FILES()
    error_message_snowboy_tasks = CHECK_TASKS(GET_ALL_SNOWBOY_TASKS(), "snowboy")
    error_message_hotword       = CHECK_HOTWORD_FILE_EXIST(GET_ALL_SNOWBOY_TASKS())

    # speech_recognition_provider only
    snowboy_hotword                      = GET_SPEECH_RECOGNITION_PROVIDER_SETTINGS().snowboy_hotword
    speech_recognition_provider          = GET_SPEECH_RECOGNITION_PROVIDER_SETTINGS().speech_recognition_provider
    speech_recognition_provider_username = GET_SPEECH_RECOGNITION_PROVIDER_SETTINGS().speech_recognition_provider_username
    speech_recognition_provider_key      = GET_SPEECH_RECOGNITION_PROVIDER_SETTINGS().speech_recognition_provider_key

    speech_recognition_provider_task_list = GET_ALL_SPEECH_RECOGNITION_PROVIDER_TASKS()

    dropdown_list_speech_recognition_provider = ["Google Cloud Speech", "Google Speech Recognition",
                                                 "Houndify", "IBM Speech", "Microsoft Azure Speech", 
                                                 "Microsoft Bing Voice Recognition", "Wit.ai"]
    
    error_message_speech_recognition_provider_tasks = ""
    error_message_speech_recognition_provider_settings = CHECK_SPEECH_RECOGNITION_PROVIDER_SETTINGS(GET_SPEECH_RECOGNITION_PROVIDER_SETTINGS())

    return render_template('dashboard_settings_speechcontrol.html',
                            error_message=error_message,   
                            error_message_snowboy=error_message_snowboy,   
                            error_message_table=error_message_table,  
                            error_message_snowboy_tasks=error_message_snowboy_tasks,        
                            error_message_fileupload=error_message_fileupload,
                            error_message_hotword=error_message_hotword,
                            error_message_speech_recognition_provider_tasks=error_message_speech_recognition_provider_tasks,
                            error_message_speech_recognition_provider_settings=error_message_speech_recognition_provider_settings,
                            
                            speechcontrol_setting=speechcontrol_setting,
                            check_value_speechcontrol=check_value_speechcontrol,
                            snowboy_task_list=snowboy_task_list,
                            sensitivity=sensitivity,
                            delay=delay,
                            microphone=microphone,
                            dropdown_list_microphone_options=dropdown_list_microphone_options,

                            snowboy_name=snowboy_name,
                            snowboy_task=snowboy_task,
                            hotword_file_list=hotword_file_list,                            
                            snowboy_hotword=snowboy_hotword,

                            dropdown_list_speech_recognition_provider=dropdown_list_speech_recognition_provider,
                            speech_recognition_provider_task_list=speech_recognition_provider_task_list,
                            speech_recognition_provider=speech_recognition_provider,
                            speech_recognition_provider_username=speech_recognition_provider_username,
                            speech_recognition_provider_key=speech_recognition_provider_key,
                            speech_recognition_provider_task=speech_recognition_provider_task,
                            speech_recognition_provider_keywords=speech_recognition_provider_keywords,
                            speech_recognition_provider_parameters=speech_recognition_provider_parameters,

                            active03="active",
                            )


# delete snowboy task
@app.route('/dashboard/settings/speechcontrol/snowboy/delete/task/<int:id>')
@login_required
@superuser_required
def delete_snowboy_task(id):
    DELETE_SNOWBOY_TASK(id)
    return redirect(url_for('dashboard_settings_speechcontrol'))

# delete speech_recognition_provider task
@app.route('/dashboard/settings/speechcontrol/speech_recognition_provider/delete/task/<int:id>')
@login_required
@superuser_required
def delete_speech_recognition_provider_task(id):
    DELETE_SPEECH_RECOGNITION_PROVIDER_TASK(id)
    return redirect(url_for('dashboard_settings_speechcontrol'))

# download hotword file
@app.route('/dashboard/settings/speechcontrol/snowboy/download/hotword/<path:filepath>')
@login_required
@superuser_required
def download_hotword_file(filepath):
    if filepath is None:
        print("Ungültiger Pfad angegeben")     
    try:
        path = GET_PATH() + "/app/snowboy/resources/"     
        WRITE_LOGFILE_SYSTEM("EVENT", "File | /app/snowboy/resources/" + filepath + " | downloaded")
        return send_from_directory(path, filepath)
        
    except Exception as e:
        WRITE_LOGFILE_SYSTEM("ERROR", "File | /app/snowboy/resources/" + filepath + " | " + str(e)) 


# delete snowboy hotwords
@app.route('/dashboard/settings/snowboy/delete/hotword/<string:filename>')
@login_required
@superuser_required
def delete_snowboy_hotword(filename):
    DELETE_HOTWORD_FILE(filename)
    return redirect(url_for('dashboard_settings_speechcontrol'))


""" ############# """
""" user settings """
""" ############# """

# dashboard user management
@app.route('/dashboard/settings/user', methods=['GET', 'POST'])
@login_required
@superuser_required
def dashboard_settings_user():
    error_message = ""
    error_message_form = ""

    if request.method == "POST":     
        # change user settings
        if request.form.get("change_user_settings") != None:
            for i in range (1,51): 
                
                if request.form.get("set_username_" + str(i)) != None:

                    # check name
                    if (request.form.get("set_username_" + str(i)) != "" and 
                        GET_USER_BY_NAME(request.form.get("set_username_" + str(i))) == None):
                        username = request.form.get("set_username_" + str(i)) 
                        
                    elif request.form.get("set_username_" + str(i)) == GET_USER_BY_ID(i).username:
                        username = GET_USER_BY_ID(i).username                        
                        
                    else:
                        username = GET_USER_BY_ID(i).username 
                        error_message_form = "Ungültige Eingabe (leeres Feld / Name schon vergeben"                          
                    
                    # check email
                    if (request.form.get("set_email_" + str(i)) != "" and 
                        GET_EMAIL(request.form.get("set_email_" + str(i))) == None):
                        email = request.form.get("set_email_" + str(i)) 
                    
                    elif request.form.get("set_email_" + str(i)) == GET_USER_BY_ID(i).email:
                        email = GET_USER_BY_ID(i).email                        
                    
                    else:
                        email = GET_USER_BY_ID(i).email 
                        error_message_form = "Ungültige Eingabe (leeres Feld / Name schon vergeben"   

                    # change user role
                    role = request.form.get("set_role_" + str(i))

                    # change email notification
                    if request.form.get("checkbox_info_" + str(i)):
                        email_notification_info = "checked"
                    else:
                        email_notification_info = ""
                    if request.form.get("checkbox_error_" + str(i)):
                        email_notification_error = "checked"
                    else:
                        email_notification_error = ""
                    if request.form.get("checkbox_camera_" + str(i)):
                        email_notification_camera = "checked"
                    else:
                        email_notification_camera = ""
           
                    SET_USER_SETTINGS(i, username, email, role, email_notification_info, email_notification_error, email_notification_camera)


    user_list = GET_ALL_USERS()
    dropdown_list_roles = ["guest", "user", "superuser"]

    return render_template('dashboard_settings_user.html',
                            error_message=error_message,
                            error_message_form=error_message_form,
                            user_list=user_list,  
                            dropdown_list_roles=dropdown_list_roles,             
                            active04="active",
                            )


# delete user
@app.route('/dashboard/settings/user/delete/<int:id>')
@login_required
@superuser_required
def delete_user(id):
    DELETE_USER(id)
    return redirect(url_for('dashboard_settings_user'))


""" ############# """
""" email settings """
""" ############# """

# dashboard email settings
@app.route('/dashboard/settings/email', methods=['GET', 'POST'])
@login_required
@superuser_required
def dashboard_settings_email():
    error_message = ""
    error_message_test = ""
    message_test = ""

    if request.method == "POST":     
        # update email settings
        if request.form.get("change_email_settings") is not None:      
            set_mail_server_address = request.form.get("set_mail_server_address")
            set_mail_server_port    = request.form.get("set_mail_server_port")
            set_mail_encoding       = request.form.get("set_mail_encoding")
            set_mail_username       = request.form.get("set_mail_username")               
            set_mail_password       = request.form.get("set_mail_password")

            error_message = SET_EMAIL_SETTINGS(set_mail_server_address, 
                                                    set_mail_server_port, 
                                                    set_mail_encoding, 
                                                    set_mail_username, 
                                                    set_mail_password)

        # test email settings
        if request.form.get("test_email_config") is not None:
            error_message_test = SEND_EMAIL(GET_EMAIL_ADDRESS("test"), "TEST", "TEST")

    email_config = GET_EMAIL_CONFIG()[0]
    mail_encoding_list = ["TLS", "SSL"]
    
    # eMail-Muster
    # SEND_EMAIL(GET_EMAIL_ADDRESS("info"), "TEST", "Das ist eine eMail mit Anhang")

    return render_template('dashboard_settings_email.html',
                            error_message=error_message,
                            error_message_test=error_message_test,
                            email_config=email_config,
                            mail_encoding_list=mail_encoding_list,                          
                            active05="active",
                            )


""" ############### """
""" system settings """
""" ############### """

@app.route('/dashboard/settings/system', methods=['GET', 'POST'])
@login_required
@superuser_required
def dashboard_settings_system():
    error_message = ""

    def GET_CPU_TEMPERATURE():
        res = os.popen('vcgencmd measure_temp').readline()
        return(res.replace("temp=","").replace("'C\n"," C"))

    if request.method == "POST":     
        # restart raspi 
        if request.form.get("restart") is not None:
            os.system("sudo shutdown -r now")
            sys.exit()
        # shutdown raspi 
        if request.form.get("shutdown") is not None:
            os.system("sudo shutdown -h now")
            sys.exit()
        # save database   
        if request.form.get("database_save") is not None:
            SAVE_DATABASE() 
 
    file_list = GET_BACKUP_FILES()
    cpu_temperature = GET_CPU_TEMPERATURE()

    return render_template('dashboard_settings_system.html',
                            error_message=error_message,
                            file_list=file_list,
                            cpu_temperature=cpu_temperature,                                                     
                            active06="active",
                            )


# restore database backup
@app.route('/dashboard/settings/system/restore/backup_database/<string:filename>')
@login_required
@superuser_required
def restore_database_backup(filename):
    RESTORE_DATABASE(filename)
    return redirect(url_for('dashboard_settings_system'))


# delete database backup
@app.route('/dashboard/settings/system/delete/backup_database/<string:filename>')
@login_required
@superuser_required
def delete_database_backup(filename):
    DELETE_DATABASE_BACKUP(filename)
    return redirect(url_for('dashboard_settings_system'))


""" ########### """
""" system logs """
""" ########### """

@app.route('/dashboard/settings/system_log', methods=['GET', 'POST'])
@login_required
@superuser_required
def dashboard_settings_system_log():
    error_message = ""

    if request.method == 'POST':
        if request.form.get("reset_logfile") is not None: 
            RESET_LOGFILE("log_system")   
            
    if GET_LOGFILE_SYSTEM(30) is not None:
        data_log_system = GET_LOGFILE_SYSTEM(30)
    else:
        data_log_system = ""

    timestamp = str(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")) 

    return render_template('dashboard_settings_system_log.html',
                            error_message=error_message,
                            timestamp=timestamp,
                            data_log_system=data_log_system,                                                       
                            active07="active",
                            )


# download system logfile
@app.route('/dashboard/settings/system_log/download/<path:filepath>')
@login_required
@superuser_required
def download_system_logfile(filepath): 
    try:
        path = GET_PATH() + "/logs/"    
        WRITE_LOGFILE_SYSTEM("EVENT", "File | /logs/" + filepath + " | downloaded")
        return send_from_directory(path, filepath)
    except Exception as e:
        WRITE_LOGFILE_SYSTEM("ERROR", "File | /logs/" + filepath + " | " + str(e))
