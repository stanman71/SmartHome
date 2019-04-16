from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from werkzeug.security import generate_password_hash
import re
import time
import datetime

from app import app
from app.components.file_management import WRITE_LOGFILE_SYSTEM

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database/smarthome.sqlite3'
db = SQLAlchemy(app)


""" ###################### """
""" ###################### """
""" define table structure """
""" ###################### """
""" ###################### """

class eMail(db.Model):
    __tablename__ = 'email'
    id                  = db.Column(db.Integer, primary_key=True, autoincrement = True)
    mail_server_address = db.Column(db.String(50))
    mail_server_port    = db.Column(db.Integer)
    mail_encoding       = db.Column(db.String(50))
    mail_username       = db.Column(db.String(50))
    mail_password       = db.Column(db.String(50)) 

class Error_List(db.Model):
    __tablename__ = 'error_list'
    id           = db.Column(db.Integer, primary_key=True, autoincrement = True)
    content      = db.Column(db.String(100))

class LED_Programs(db.Model):
    __tablename__ = 'led_programs'
    id      = db.Column(db.Integer, primary_key=True, autoincrement = True)
    name    = db.Column(db.String(50), unique = True)
    content = db.Column(db.Text)

class LED_Scenes(db.Model):
    __tablename__ = 'led_scenes'
    id            = db.Column(db.Integer, primary_key=True, autoincrement = True)
    name          = db.Column(db.String(50), unique = True)
    led_id_1      = db.Column(db.Integer)
    led_name_1    = db.Column(db.String(50))
    red_1         = db.Column(db.Integer, server_default=("0"))
    green_1       = db.Column(db.Integer, server_default=("0"))
    blue_1        = db.Column(db.Integer, server_default=("0"))
    brightness_1  = db.Column(db.Integer, server_default=("254"))
    active_led_2  = db.Column(db.String(50))
    led_id_2      = db.Column(db.Integer)
    led_name_2    = db.Column(db.String(50))
    red_2         = db.Column(db.Integer, server_default=("0"))
    green_2       = db.Column(db.Integer, server_default=("0"))
    blue_2        = db.Column(db.Integer, server_default=("0"))
    brightness_2  = db.Column(db.Integer, server_default=("254"))
    active_led_3  = db.Column(db.String(50))
    led_id_3      = db.Column(db.Integer)
    led_name_3    = db.Column(db.String(50))
    red_3         = db.Column(db.Integer, server_default=("0"))
    green_3       = db.Column(db.Integer, server_default=("0"))
    blue_3        = db.Column(db.Integer, server_default=("0"))
    brightness_3  = db.Column(db.Integer, server_default=("254"))
    active_led_4  = db.Column(db.String(50))
    led_id_4      = db.Column(db.Integer)
    led_name_4    = db.Column(db.String(50))
    red_4         = db.Column(db.Integer, server_default=("0"))
    green_4       = db.Column(db.Integer, server_default=("0"))
    blue_4        = db.Column(db.Integer, server_default=("0"))
    brightness_4  = db.Column(db.Integer, server_default=("254"))
    active_led_5  = db.Column(db.String(50))
    led_id_5      = db.Column(db.Integer)
    led_name_5    = db.Column(db.String(50))
    red_5         = db.Column(db.Integer, server_default=("0"))
    green_5       = db.Column(db.Integer, server_default=("0"))
    blue_5        = db.Column(db.Integer, server_default=("0"))
    brightness_5  = db.Column(db.Integer, server_default=("254"))        
    active_led_6  = db.Column(db.String(50))
    led_id_6      = db.Column(db.Integer)
    led_name_6    = db.Column(db.String(50))
    red_6         = db.Column(db.Integer, server_default=("0"))
    green_6       = db.Column(db.Integer, server_default=("0"))
    blue_6        = db.Column(db.Integer, server_default=("0"))
    brightness_6  = db.Column(db.Integer, server_default=("254"))
    active_led_7  = db.Column(db.String(50))
    led_id_7      = db.Column(db.Integer)
    led_name_7    = db.Column(db.String(50))
    red_7         = db.Column(db.Integer, server_default=("0"))
    green_7       = db.Column(db.Integer, server_default=("0"))
    blue_7        = db.Column(db.Integer, server_default=("0"))
    brightness_7  = db.Column(db.Integer, server_default=("254"))
    active_led_8  = db.Column(db.String(50))
    led_id_8      = db.Column(db.Integer)
    led_name_8    = db.Column(db.String(50))
    red_8         = db.Column(db.Integer, server_default=("0"))
    green_8       = db.Column(db.Integer, server_default=("0"))
    blue_8        = db.Column(db.Integer, server_default=("0"))
    brightness_8  = db.Column(db.Integer, server_default=("254"))
    active_led_9  = db.Column(db.String(50))
    led_id_9      = db.Column(db.Integer)
    led_name_9    = db.Column(db.String(50))
    red_9         = db.Column(db.Integer, server_default=("0"))
    green_9       = db.Column(db.Integer, server_default=("0"))
    blue_9        = db.Column(db.Integer, server_default=("0"))
    brightness_9  = db.Column(db.Integer, server_default=("254"))   

class MQTT_Devices(db.Model):
    __tablename__ = 'mqtt_devices'
    id           = db.Column(db.Integer, primary_key=True, autoincrement = True)
    name         = db.Column(db.String(50), unique=True)
    gateway      = db.Column(db.String(50)) 
    ieeeAddr     = db.Column(db.String(50))  
    model        = db.Column(db.String(50))
    inputs       = db.Column(db.String(200))
    outputs      = db.Column(db.String(200))
    last_contact = db.Column(db.String(50))

class Plants(db.Model):
    __tablename__  = 'plants'
    id             = db.Column(db.Integer, primary_key=True, autoincrement = True)   
    name           = db.Column(db.String(50), unique=True)
    mqtt_device_id = db.Column(db.Integer, db.ForeignKey('mqtt_devices.id'))   
    watervolume    = db.Column(db.Integer)
    mqtt_device    = db.relationship('MQTT_Devices')  
    pump_key       = db.Column(db.String(50))
    sensor_key     = db.Column(db.String(50))
    control_sensor = db.Column(db.String(50))     

class Sensordata_Jobs(db.Model):
    __tablename__  = 'sensordata_jobs'
    id               = db.Column(db.Integer, primary_key=True, autoincrement = True)
    name             = db.Column(db.String(50), unique=True)
    filename         = db.Column(db.String(50))
    mqtt_device_id   = db.Column(db.Integer, db.ForeignKey('mqtt_devices.id'))   
    mqtt_device      = db.relationship('MQTT_Devices')  
    sensor_key       = db.Column(db.String(50)) 
    always_active    = db.Column(db.String(50))

class Settings(db.Model):
    __tablename__ = 'settings'
    id            = db.Column(db.Integer, primary_key=True, autoincrement = True)
    setting_name  = db.Column(db.String(50), unique=True)
    setting_value = db.Column(db.String(50))   

class Snowboy(db.Model):
    __tablename__ = 'snowboy'
    id          = db.Column(db.Integer, primary_key=True, autoincrement = True)
    sensitivity = db.Column(db.Integer)

class Snowboy_Tasks(db.Model):
    __tablename__ = 'snowboy_tasks'
    id   = db.Column(db.Integer, primary_key=True, autoincrement = True)
    name = db.Column(db.String(50), unique = True)
    task = db.Column(db.String(100))

class Taskmanagement_Time(db.Model):
    __tablename__ = 'taskmanagement_time'
    id     = db.Column(db.Integer, primary_key=True, autoincrement = True)
    name   = db.Column(db.String(50), unique=True)
    day    = db.Column(db.String(50))
    hour   = db.Column(db.String(50))
    minute = db.Column(db.String(50))
    task   = db.Column(db.String(100))
    repeat = db.Column(db.String(50))

class Taskmanagement_Sensor(db.Model):
    __tablename__ = 'taskmanagement_sensor'
    id                   = db.Column(db.Integer, primary_key=True, autoincrement = True)
    name                 = db.Column(db.String(50), unique=True)
    task                 = db.Column(db.String(100))          
    mqtt_device_id_1     = db.Column(db.Integer)  
    mqtt_device_name_1   = db.Column(db.String(50)) 
    mqtt_device_inputs_1 = db.Column(db.String(100)) 
    sensor_key_1         = db.Column(db.String(50))    
    value_1              = db.Column(db.String(100), server_default=(""))
    operator_1           = db.Column(db.String(50))
    operator_main_1      = db.Column(db.String(50))     
    mqtt_device_id_2     = db.Column(db.Integer) 
    mqtt_device_name_2   = db.Column(db.String(50))        
    mqtt_device_inputs_2 = db.Column(db.String(100)) 
    sensor_key_2         = db.Column(db.String(50))    
    value_2              = db.Column(db.String(100), server_default=(""))
    operator_2           = db.Column(db.String(50))   
    operator_main_2      = db.Column(db.String(50))     
    mqtt_device_id_3     = db.Column(db.Integer) 
    mqtt_device_name_3   = db.Column(db.String(50))        
    mqtt_device_inputs_3 = db.Column(db.String(100)) 
    sensor_key_3         = db.Column(db.String(50))    
    value_3              = db.Column(db.String(100), server_default=(""))
    operator_3           = db.Column(db.String(50))   

class User(UserMixin, db.Model):
    __tablename__ = 'user'
    id                        = db.Column(db.Integer, primary_key=True, autoincrement = True)
    username                  = db.Column(db.String(50), unique=True)
    email                     = db.Column(db.String(50), unique=True)
    password                  = db.Column(db.String(100))
    role                      = db.Column(db.String(20), server_default=("guest")) 
    email_notification_info   = db.Column(db.String(20), server_default=(""))
    email_notification_error  = db.Column(db.String(20), server_default=(""))
    email_notification_camera = db.Column(db.String(20), server_default=(""))

class ZigBee(db.Model):
    __tablename__ = 'zigbee'
    id      = db.Column(db.Integer, primary_key=True, autoincrement = True)
    pairing = db.Column(db.String(50))


""" ################################ """
""" ################################ """
""" create tables and default values """
""" ################################ """
""" ################################ """


# create all database tables
db.create_all()


# create default email
if eMail.query.filter_by().first() is None:
    email = eMail(
        id = 1,
    )
    db.session.add(email)
    db.session.commit()


# create error list
if Error_List.query.filter_by().first() is None:      
    error = Error_List(
        id = 1,
        content = "",
    )        
    db.session.add(error)
    db.session.commit()


# create default settings
if Settings.query.filter_by().first() is None:
    setting = Settings(
        setting_name  = "mqtt",
        setting_value = "False",
    )
    db.session.add(setting)    
    db.session.commit()
    
    setting = Settings(
        setting_name  = "zigbee",
        setting_value = "False",
    )
    db.session.add(setting)    
    db.session.commit()

    setting = Settings(
        setting_name  = "snowboy",
        setting_value = "False",
    )
    db.session.add(setting)    
    db.session.commit()


# create default snowboy
if Snowboy.query.filter_by().first() is None:
    snowboy = Snowboy(
        sensitivity  = "45",
    )
    db.session.add(snowboy)
    db.session.commit()


# create default user
if User.query.filter_by(username='default').first() is None:
    user = User(
        username='default',
        email='member@example.com',
        password=generate_password_hash('qwer1234', method='sha256'),
        role='superuser'
    )
    db.session.add(user)
    db.session.commit()


# create default zigbee
if ZigBee.query.filter_by().first() is None:
    zigbee = ZigBee(
        pairing = "False",
    )
    db.session.add(zigbee)
    db.session.commit()


""" ################## """
""" ################## """
"""        eMail       """
""" ################## """
""" ################## """


def GET_EMAIL_CONFIG():   
    return eMail.query.all()


def GET_EMAIL_ADDRESS(address_type): 
    if address_type == "test":
        mail_list = []
        mail_list.append(eMail.query.filter_by().first().mail_username)
        return mail_list

    if address_type == "info":
        mail_list = []
        users = User.query.all()
        for user in users:
            if user.email_notification_info == "checked":
                mail_list.append(user.email)
        return mail_list

    if address_type == "error":
        mail_list = []
        users = User.query.all()
        for user in users:
            if user.email_notification_error == "checked":
                mail_list.append(user.email)
        return mail_list

    if address_type == "camera":
        mail_list = []
        users = User.query.all()
        for user in users:
            if user.email_notification_camera == "checked":
                mail_list.append(user.email)
        return mail_list


def SET_EMAIL_SETTINGS(mail_server_address, mail_server_port, mail_encoding, mail_username, mail_password): 
    email = eMail.query.filter_by().first()
    email.mail_server_address = mail_server_address
    email.mail_server_port    = mail_server_port
    email.mail_encoding       = mail_encoding
    email.mail_username       = mail_username
    email.mail_password       = mail_password
    db.session.commit()
    
    WRITE_LOGFILE_SYSTEM("EVENT", "Database >>> eMail Server Settings >>> changed")
    return ""


""" ################## """
""" ################## """
"""     error list     """
""" ################## """
""" ################## """


def SET_ERROR_LIST(content):
    entry = Error_List.query.filter_by(id=1).first()
    entry.content = content
    db.session.commit()  


def GET_ERROR_LIST():
    entry = Error_List.query.filter_by(id=1).first()
    return entry.content


""" ################### """
""" ################### """
"""    led programs     """
""" ################### """
""" ################### """


def GET_ALL_LED_PROGRAMS():
    return LED_Programs.query.all()   


def GET_LED_PROGRAM_BY_NAME(name):
    return LED_Programs.query.filter_by(name=name).first()


def GET_LED_PROGRAM_BY_ID(id):
    return LED_Programs.query.filter_by(id=id).first()


def ADD_LED_PROGRAM(name):
    # name exist ?
    check_entry = LED_Programs.query.filter_by(name=name).first()
    if check_entry is None:
        # find a unused id
        for i in range(1,25):
            if LED_Programs.query.filter_by(id=i).first():
                pass
            else:
                # add the new program
                program = LED_Programs(
                        id = i,
                        name = name,
                        content = "",
                    )
                db.session.add(program)
                db.session.commit()

                WRITE_LOGFILE_SYSTEM("EVENT", "Database >>> LED Program >>> " + name + " >>> added")  

                return ""
    else:
        return "Name bereits vergeben"


def SET_LED_PROGRAM_NAME(id, name):
    check_entry = LED_Programs.query.filter_by(name=name).first()
    if check_entry is None:
        entry = LED_Programs.query.filter_by(id=id).first()
        entry.name = name
        db.session.commit()    


def UPDATE_LED_PROGRAM(id, content):
    entry = LED_Programs.query.filter_by(id=id).update(dict(content=content))
    db.session.commit()


def DELETE_LED_PROGRAM(name):
    name = LED_Programs.query.filter_by(name=name).name
    WRITE_LOGFILE_SYSTEM("EVENT", "Database >>> LED Program >>> " + name + " >>> deleted")  

    LED_Programs.query.filter_by(name=name).delete()
    db.session.commit() 


""" ################### """
""" ################### """
"""    led scenes     """
""" ################### """
""" ################### """


def GET_ALL_LED_SCENES():
    return LED_Scenes.query.all()   


def GET_LED_SCENE_BY_ID(id):
    return LED_Scenes.query.filter_by(id=id).first()


def GET_LED_SCENE_BY_NAME(name):
    return LED_Scenes.query.filter_by(name=name).first()


def ADD_LED_SCENE(name):
    # name exist ?
    check_entry = LED_Scenes.query.filter_by(name=name).first()
    if check_entry is None:
        if name == "":
            return "Kein Name angegeben"
        else:
            # find a unused id
            for i in range(1,25):
                if LED_Scenes.query.filter_by(id=i).first():
                    pass
                else:
                    # add the new program
                    scene = LED_Scenes(
                            id = i,
                            name = name,
                        )
                    db.session.add(scene)
                    db.session.commit()

                    WRITE_LOGFILE_SYSTEM("EVENT", "Database >>> LED Scene >>> " + name + " >>> added")  

                    return ""
    else:
        return "Name bereits vergeben"


def SET_LED_SCENE(id, name, led_id_1, led_name_1, red_1, green_1, blue_1, brightness_1,
                            led_id_2, led_name_2, red_2, green_2, blue_2, brightness_2):

    entry = LED_Scenes.query.filter_by(id=id).first()
    entry.name  = name

    entry.led_id_1 = led_id_1
    entry.led_name_1 = led_name_1
    entry.red_1 = red_1
    entry.green_1 = green_1   
    entry.blue_1 = blue_1
    entry.brightness_1 = brightness_1
    entry.led_id_2 = led_id_2
    entry.led_name_2 = led_name_2
    entry.red_2 = red_2
    entry.green_2 = green_2   
    entry.blue_2 = blue_2
    entry.brightness_2 = brightness_2

    db.session.commit()   


def LED_SCENE_LED_EXIST(id):
    led_list = []

    entry = LED_Scenes.query.filter_by(id=id).first()

    led_list.append(entry.led_id_1)
    led_list.append(entry.led_id_2)
    led_list.append(entry.led_id_3)
    led_list.append(entry.led_id_4)
    led_list.append(entry.led_id_5)
    led_list.append(entry.led_id_6)
    led_list.append(entry.led_id_7)
    led_list.append(entry.led_id_8)
    led_list.append(entry.led_id_9)

    return led_list


def ADD_LED_SCENE_LED(id):
    entry = LED_Scenes.query.filter_by(id=id).first()

    if entry.active_led_2 != "on":
        entry.active_led_2 = "on"
        db.session.commit()
        return

    if entry.active_led_3 != "on":
        entry.active_led_3 = "on"
        db.session.commit()
        return

    if entry.active_led_4 != "on":
        entry.active_led_4 = "on"
        db.session.commit()
        return

    if entry.active_led_5 != "on":
        entry.active_led_5 = "on"
        db.session.commit()
        return

    if entry.active_led_6 != "on":
        entry.active_led_6 = "on"
        db.session.commit()
        return

    if entry.active_led_7 != "on":
        entry.active_led_7 = "on"
        db.session.commit()
        return

    if entry.active_led_8 != "on":
        entry.active_led_8 = "on"
        db.session.commit()
        return       

    if entry.active_led_9 != "on":
        entry.active_led_9 = "on"
        db.session.commit()
        return  


def REMOVE_LED_SCENE_LED(id, led_id):
    entry = LED_Scenes.query.filter_by(id=id).first()

    if led_id == 2:
        entry.active_led_2 = "None"
        db.session.commit()
        return

    if led_id == 3:
        entry.active_led_3 = "None"
        db.session.commit()
        return

    if led_id == 4:
        entry.active_led_4 = "None"
        db.session.commit()
        return

    if led_id == 5:
        entry.active_led_5 = "None"
        db.session.commit()
        return            

    if led_id == 6:
        entry.active_led_6 = "None"
        db.session.commit()
        return

    if led_id == 7:
        entry.active_led_7 = "None"
        db.session.commit()
        return

    if led_id == 7:
        entry.active_led_7 = "None"
        db.session.commit()
        return

    if led_id == 8:
        entry.active_led_8 = "None"
        db.session.commit()
        return            

    if led_id == 9:
        entry.active_led_9 = "None"
        db.session.commit()
        return


def DELETE_LED_SCENE(id):

    try:
        name = GET_LED_SCENE_BY_ID(id).name
        WRITE_LOGFILE_SYSTEM("EVENT", "Database >>> LED Scene >>> " + name + " >>> deleted")   
    except:
        pass
    
    LED_Scenes.query.filter_by(id=id).delete()
    db.session.commit() 


""" ################### """
""" ################### """
"""        mqtt         """
""" ################### """
""" ################### """


def GET_MQTT_DEVICE(id):
    return MQTT_Devices.query.filter_by(id=id).first()


def GET_ALL_MQTT_DEVICES(selector):
    device_list = []
    devices = MQTT_Devices.query.all()
    
    if selector == "mqtt" or selector == "zigbee":
        for device in devices:
            if device.gateway == selector:
                device_list.append(device)
                
    if selector == "sensor":
        for device in devices:
            if device.inputs:
                device_list.append(device)  
                
    if selector == "watering":
        for device in devices:
            if device.inputs and device.outputs:
                device_list.append(device)    

    if selector == "led":
        for device in devices:
            if device.model == "9290012573A":
                device_list.append(device)                                 
                
    return device_list
        

def GET_MQTT_DEVICE_NAME(id):
    return MQTT_Devices.query.filter_by(id=id).first().name


def GET_MQTT_DEVICE_INPUTS_BY_ID(id):
    return MQTT_Devices.query.filter_by(id=id).first().inputs   


def ADD_MQTT_DEVICE(name, gateway, ieeeAddr, model = "", inputs = "", outputs = "", last_contact = ""):
    # path exist ?
    check_entry = MQTT_Devices.query.filter_by(ieeeAddr=ieeeAddr).first()
    if check_entry is None:       
        # find a unused id
        for i in range(1,50):
            if MQTT_Devices.query.filter_by(id=i).first():
                pass
            else:
                # add the new device            
                device = MQTT_Devices(
                        id           = i,
                        name         = name,
                        gateway      = gateway,                       
                        ieeeAddr     = ieeeAddr,
                        model        = model,
                        inputs       = inputs,
                        outputs      = outputs,
                        last_contact = last_contact,
                        )
                db.session.add(device)
                db.session.commit()
                
                WRITE_LOGFILE_SYSTEM("EVENT", "Database >>> MQTT Device >>> " + name + " >>> added >>>  Gateway: " + 
                                     gateway + " /// ieeeAddr: " + ieeeAddr + " /// Model: " + model + 
                                     " /// Inputs: " + inputs + " /// Outputs: " + outputs)

                SET_MQTT_DEVICE_LAST_CONTACT(ieeeAddr)                                  
                
    else:
        SET_MQTT_DEVICE_LAST_CONTACT(ieeeAddr)  


def SET_MQTT_DEVICE_LAST_CONTACT(ieeeAddr):
    timestamp = str(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")) 
    entry = MQTT_Devices.query.filter_by(ieeeAddr=ieeeAddr).first()
    entry.last_contact = timestamp
    db.session.commit()       


def SET_MQTT_DEVICE_MQTT(id, name):
    entry = MQTT_Devices.query.filter_by(id=id).first()

    # values changed ?
    if (entry.name != name):

        WRITE_LOGFILE_SYSTEM("EVENT", "Database >>> MQTT Device >>> " + entry.name + " >>> changed >>> Name: " +
                            name + " /// Gateway: " + entry.gateway + " /// ieeeAddr: " + entry.ieeeAddr + 
                            " /// Model: " + entry.model + " /// Inputs: " + str(entry.inputs) + " /// Outputs: " + 
                            entry.outputs)

        entry.name = name
        db.session.commit()    


def SET_MQTT_DEVICE_ZigBee(id, name, inputs):
    entry = MQTT_Devices.query.filter_by(id=id).first()

    # values changed ?
    if (entry.name != name or entry.inputs != inputs):
        
        entry.inputs = inputs
        
        WRITE_LOGFILE_SYSTEM("EVENT", "Database >>> MQTT Device >>> " + entry.name + " >>> changed >>> Name: " +
                            name + " /// Gateway: " + entry.gateway + " /// ieeeAddr: " + entry.ieeeAddr + 
                            " /// Model: " + entry.model + " /// Inputs: " + inputs)

        entry.name = name
        db.session.commit()    


def DELETE_MQTT_DEVICE(id):
    if Plants.query.filter_by(mqtt_device_id=id).first():
        entry = GET_MQTT_DEVICE(id)
        SET_ERROR_LIST(entry.name + " wird in Bewässerung verwendet")
    elif Sensordata_Jobs.query.filter_by(mqtt_device_id=id).first():
        entry = GET_MQTT_DEVICE(id)
        SET_ERROR_LIST(entry.name + " wird in Sensordaten verwendet")      
    else:
        entry = GET_MQTT_DEVICE(id)
        WRITE_LOGFILE_SYSTEM("EVENT", "Database >>> MQTT Device >>> " + entry.name + " >>> deleted")
 
        MQTT_Devices.query.filter_by(id=id).delete()
        db.session.commit() 
        return "MQTT-Device gelöscht"


""" ################### """
""" ################### """
"""       plants        """
""" ################### """
""" ################### """


def GET_PLANT_BY_ID(plant_id):
    return Plants.query.filter_by(id=plant_id).first()


def GET_PLANT_BY_NAME(name):
    plants = Plants.query.all()

    for plant in plants:
        if plant.name == name:
            return plant


def GET_ALL_PLANTS():
    return Plants.query.all()


def CHECK_PLANTS():
    string_errors = ""
    entries = Plants.query.all()
    for entry in entries:
        if ((entry.sensor_key == "None" or entry.sensor_key == None) or
            (entry.pump_key == "None" or entry.pump_key == None)):
            
            string_errors = string_errors + str(entry.name) + " "
     
    if string_errors != "":
        return ("Einstellungen unvollständig ( Pflanzen-Name: " + string_errors + ")")
    else:
        return ""


def ADD_PLANT(name, mqtt_device_id, watervolume, control_sensor, log = ""):
    # name exist ?
    check_entry = Plants.query.filter_by(name=name).first()
    if check_entry is None:
        # find a unused id
        for i in range(1,25):
            if Plants.query.filter_by(id=i).first():
                pass
            else:
                # add the new plant
                plant = Plants(
                        id             = i,
                        name           = name,
                        mqtt_device_id = mqtt_device_id,
                        watervolume    = watervolume, 
                        control_sensor = control_sensor,                    
                    )
                db.session.add(plant)
                db.session.commit()
                
                if log == "":
                    WRITE_LOGFILE_SYSTEM("EVENT", "Database >>> Plant >>> " + name + " >>> added")               
                
                return ""

    else:
        return "Name bereits vergeben"


def SET_PLANT_SETTINGS(plant_id, name, sensor_key, pump_key, watervolume, control_sensor):        
    entry = Plants.query.filter_by(id=plant_id).first()
    old_name = entry.name

    # values changed ?
    if (entry.name != name or entry.sensor_key != sensor_key or entry.pump_key != pump_key or 
        entry.watervolume != int(watervolume) or entry.control_sensor != control_sensor):

        entry.name = name
        entry.sensor_key = sensor_key
        entry.pump_key = pump_key
        entry.watervolume = watervolume
        entry.control_sensor = control_sensor
        
        db.session.commit()  

        WRITE_LOGFILE_SYSTEM("EVENT", "Database >>> Plant >>> " + old_name + " >>> changed >>> Name: " + entry.name + 
                             " /// MQTT-Device: " + entry.mqtt_device.name + " /// Sensor: " + entry.sensor_key + 
                             " /// Pump: " + entry.pump_key + " /// Watervolume: " + str(watervolume) + " /// Control-Sensor: " +
                             entry.control_sensor)                


def DELETE_PLANT(plant_id, log = ""):
    entry = GET_PLANT_BY_ID(plant_id)

    if log == "":
        WRITE_LOGFILE_SYSTEM("EVENT", "Database >>> Plant >>> " + entry.name + " >>> deleted")   
    
    Plants.query.filter_by(id=plant_id).delete()
    db.session.commit()


""" ################### """
""" ################### """
"""     sensordata      """
""" ################### """
""" ################### """


def GET_SENSORDATA_JOB_BY_ID(id):
    return Sensordata_Jobs.query.filter_by(id=id).first()


def GET_SENSORDATA_JOB_BY_NAME(name):
    return Sensordata_Jobs.query.filter_by(name=name).first()


def GET_ALL_SENSORDATA_JOBS():
    return Sensordata_Jobs.query.all()


def CHECK_SENSORDATA_JOBS():
    string_errors = ""
    entries = Sensordata_Jobs.query.all()
    for entry in entries:
        if entry.sensor_key == "None" or entry.sensor_key == None:
            string_errors = string_errors + str(entry.id) + " "
            
    if string_errors != "":
        return ("Einstellungen unvollständig ( Job-ID: " + string_errors + ")")
    else:
        return ""


def ADD_SENSORDATA_JOB(name, filename, mqtt_device_id, always_active, log = ""):
    # name exist ?
    check_entry = Sensordata_Jobs.query.filter_by(name=name).first()
    if check_entry is None:        
        # find a unused id
        for i in range(1,25):
            if Sensordata_Jobs.query.filter_by(id=i).first():
                pass
            else:
                # add the new job
                sensordata_job = Sensordata_Jobs(
                        id             = i,
                        name           = name,
                        filename       = filename,
                        mqtt_device_id = mqtt_device_id, 
                        always_active  = always_active,                
                    )
                db.session.add(sensordata_job)
                db.session.commit()

                if log == "":
                    WRITE_LOGFILE_SYSTEM("EVENT", "Database >>> Sensordata Job >>> " + name + " >>> added")                    
             
                return ""
    else:
        return "Name bereits vergeben"


def SET_SENSORDATA_JOB(id, name, filename, mqtt_device_id, sensor_key, always_active):        
    entry = Sensordata_Jobs.query.filter_by(id=id).first()
    old_name = entry.name

    # values changed?
    if (entry.name != name or entry.filename != filename or entry.mqtt_device_id != mqtt_device_id or 
        entry.sensor_key != sensor_key or entry.always_active != always_active):

        entry.name = name
        entry.filename = filename
        entry.mqtt_device_id = mqtt_device_id
        entry.sensor_key = sensor_key
        entry.always_active = always_active
        db.session.commit()    

        WRITE_LOGFILE_SYSTEM("EVENT", "Database >>> Sensordata Job >>> " + entry.name + " >>> changed >>> Name: " + 
                             entry.name + " /// Filename: " +  entry.filename + " /// MQTT-Device: " + entry.mqtt_device.name + 
                              " /// Sensor: " + entry.sensor_key + " /// Always_Active: " + entry.always_active)    


def DELETE_SENSORDATA_JOB(id, log = ""):
    entry = GET_SENSORDATA_JOB_BY_ID(id)

    print(log)

    if log == "":
        WRITE_LOGFILE_SYSTEM("EVENT", "Database >>> Sensordata Job >>> " + entry.name + " >>> deleted")
 
    Sensordata_Jobs.query.filter_by(id=id).delete()
    db.session.commit()


""" ################### """
""" ################### """
"""      settings       """
""" ################### """
""" ################### """


def GET_SETTING_VALUE(name):
    entry = Settings.query.filter_by(setting_name=name).first()
    return entry.setting_value


def SET_SETTING_VALUE(name, value):
    entry = Settings.query.filter_by(setting_name=name).first()
    entry.setting_value = value
    db.session.commit()    


def GET_HUE_BRIDGE_IP():
    entry = HUE_Bridge.query.filter_by().first()
    return (entry.ip)  


def SET_HUE_BRIDGE_IP(IP):
    entry = HUE_Bridge.query.filter_by().first()
    entry.ip = IP
    db.session.commit() 


def REMOVE_LED(id):
    if Scene_01.query.filter_by(led_id=id).first():
        return "LED in Szene 1 verwendet"
    if Scene_02.query.filter_by(led_id=id).first():
        return "LED in Szene 2 verwendet"
    if Scene_03.query.filter_by(led_id=id).first():
        return "LED in Szene 3 verwendet"
    if Scene_04.query.filter_by(led_id=id).first():
        return "LED in Szene 4 verwendet" 
    if Scene_05.query.filter_by(led_id=id).first():
        return "LED in Szene 5 verwendet"
    if Scene_06.query.filter_by(led_id=id).first():
        return "LED in Szene 6 verwendet"
    if Scene_07.query.filter_by(led_id=id).first():
        return "LED in Szene 7 verwendet"
    if Scene_08.query.filter_by(led_id=id).first():
        return "LED in Szene 8 verwendet"
    if Scene_09.query.filter_by(led_id=id).first():
        return "LED in Szene 9 verwendet"
    if Scene_10.query.filter_by(led_id=id).first():
        return "LED in Szene 10 verwendet"
    if Scene_99.query.filter_by(led_id=id).first():
        return "LED in Szene 99 verwendet"

    LED.query.filter_by(id=id).delete()
    db.session.commit()    

    return "LED erfolgreich gelöscht"


""" ################### """
""" ################### """
"""      snowboy        """
""" ################### """
""" ################### """


def GET_SNOWBOY_SENSITIVITY():
    entry = Snowboy.query.filter_by().first()
    return (entry.sensitivity)  


def SET_SNOWBOY_SENSITIVITY(value):
    entry = Snowboy.query.filter_by().first()
    entry.sensitivity = value
    db.session.commit() 


def GET_SNOWBOY_TASK_BY_NAME(name):
    return Snowboy_Tasks.query.filter_by(name=name).first()


def GET_SNOWBOY_TASK_BY_ID(id):
    return Snowboy_Tasks.query.filter_by(id=id).first()


def GET_ALL_SNOWBOY_TASKS():
    return Snowboy_Tasks.query.all()


def ADD_SNOWBOY_TASK(name, task):
    # name exist ?
    check_entry = Snowboy_Tasks.query.filter_by(name=name).first()
    if check_entry is None:
        # find a unused id
        for i in range(1,25):
            if Snowboy_Tasks.query.filter_by(id=i).first():
                pass
            else:
                # add the new task
                task = Snowboy_Tasks(
                        id     = i,
                        name   = name,
                        task   = task,
                    )
                db.session.add(task)
                db.session.commit()
  
                WRITE_LOGFILE_SYSTEM("EVENT", "Database >>> Snowboy Task >>> " + name + " >>> added") 
  
                return ""
    else:
        return "Name bereits vergeben"


def SET_SNOWBOY_TASK(id, name, task):
    entry = Snowboy_Tasks.query.filter_by(id=id).first()
    old_name = entry.name
    
    # values changed ?
    if (entry.name != name or entry.task != task):
        
        entry.name = name
        entry.task = task
        db.session.commit()
        
        WRITE_LOGFILE_SYSTEM("EVENT", "Database >>> Snowboy Task >>> " + old_name + " >>> changed >>> Name: " +
                             entry.name + " /// Task: " + entry.task) 


def DELETE_SNOWBOY_TASK(task_id):
    entry = GET_SNOWBOY_TASK_ID(task_id)
    WRITE_LOGFILE_SYSTEM("EVENT", "Database >>> Snowboy Task >>> " + entry.name + " >>> deleted")    
    
    
    Snowboy_Tasks.query.filter_by(id=task_id).delete()
    db.session.commit()


""" ################## """
""" ################## """
"""   taskmanagement   """
""" ################## """
""" ################## """


def GET_TASKMANAGEMENT_TIME_TASK_BY_NAME(name):
    return Taskmanagement_Time.query.filter_by(name=name).first()


def GET_TASKMANAGEMENT_TIME_TASK_BY_ID(id):
    return Taskmanagement_Time.query.filter_by(id=id).first()


def GET_ALL_TASKMANAGEMENT_TIME_TASKS():
    return Taskmanagement_Time.query.all()


def ADD_TASKMANAGEMENT_TIME_TASK(name, task, day, hour, minute, repeat):
    # name exist ?
    check_entry = Taskmanagement_Time.query.filter_by(name=name).first()
    if check_entry is None:
        # find a unused id
        for i in range(1,25):
            if Taskmanagement_Time.query.filter_by(id=i).first():
                pass
            else:
                # add the new task
                new_task = Taskmanagement_Time(
                        id     = i,
                        name   = name,
                        task   = task,
                        day    = day,
                        hour   = hour,
                        minute = minute,
                        repeat = repeat,
                    )
                db.session.add(new_task)
                db.session.commit()
                
                WRITE_LOGFILE_SYSTEM("EVENT", "Database >>> Taskmanagement (Time) >>> " + name + " >>> added >>> Task: " + 
                                     task + " /// Day: " + day + " /// Hour: " + str(hour) + " /// Minute: " + str(minute) + 
                                     " /// Repeat: " +  repeat)                
                
                return ""
    else:
        return "Name bereits vergeben"


def SET_TASKMANAGEMENT_TIME_TASK(id, name, task, day, hour, minute, repeat):       
    entry = Taskmanagement_Time.query.filter_by(id=id).first()
    old_name = entry.name

    # values changed ?
    if (entry.name != name or entry.task != task or entry.day != day or entry.hour != hour 
        or entry.minute != minute or entry.repeat != repeat):

        entry.name = name
        entry.task = task
        entry.day = day
        entry.hour = hour
        entry.minute = minute
        entry.repeat = repeat
        db.session.commit()    

        WRITE_LOGFILE_SYSTEM("EVENT", "Database >>> Taskmanagement (Time) >>> " + old_name + " >>> changed >>> Name: " + 
                             entry.name + " /// Task: " + entry.task + " /// Day: " + entry.day + " /// Hour: " + 
                             entry.hour + " /// Minute: " + entry.minute + " /// Repeat: " +  entry.repeat)


def DELETE_TASKMANAGEMENT_TIME_TASK(task_id):
    entry = GET_TASKMANAGEMENT_TIME_TASK_BY_ID(task_id)
    WRITE_LOGFILE_SYSTEM("EVENT", "Database >>> Taskmanagement (Time) >>> " + entry.name + " >>> deleted")    
    
    Taskmanagement_Time.query.filter_by(id=task_id).delete()
    db.session.commit()


def GET_TASKMANAGEMENT_SENSOR_TASK_BY_NAME(name):
    return Taskmanagement_Sensor.query.filter_by(name=name).first()


def GET_TASKMANAGEMENT_SENSOR_TASK_BY_ID(id):
    return Taskmanagement_Sensor.query.filter_by(id=id).first()
    

def GET_ALL_TASKMANAGEMENT_SENSOR_TASKS():
    return Taskmanagement_Sensor.query.all()


def ADD_TASKMANAGEMENT_SENSOR_TASK(name, task, log = ""):
    check_entry = Taskmanagement_Sensor.query.filter_by(name=name).first()
    if check_entry is None:
        # find a unused id
        for i in range(1,25):
            if Taskmanagement_Sensor.query.filter_by(id=i).first():
                pass
            else:
                # add the new task
                new_task = Taskmanagement_Sensor(
                        id             = i,
                        name           = name,
                        task           = task,                        
                    )
                db.session.add(new_task)
                db.session.commit()
                
                if log == "":
                    WRITE_LOGFILE_SYSTEM("EVENT", "Database >>> Taskmanagement (Sensor) >>> " + name + " >>> added")               
                
                return ""
    else:
        return "Name bereits vergeben"


def ADD_TASKMANAGEMENT_SENSOR_TASK_OPTION(id):
    entry = Taskmanagement_Sensor.query.filter_by(id=id).first()
    operator_main_1 = entry.operator_main_1 
    operator_main_2 = entry.operator_main_2 

    if operator_main_1 == "None" or operator_main_1 == None:
        entry.operator_main_1 = "and"
        entry.operator_main_2 = "None"

    if operator_main_1 != "None" and operator_main_1 != None:
        entry.operator_main_2 = "and"

    db.session.commit()


def REMOVE_TASKMANAGEMENT_SENSOR_TASK_OPTION(id):
    entry = Taskmanagement_Sensor.query.filter_by(id=id).first()
    operator_main_1 = entry.operator_main_1 
    operator_main_2 = entry.operator_main_2 

    if operator_main_2 != "None":
        entry.operator_main_2 = "None"

    if operator_main_2 == "None" or operator_main_2 == None:
        entry.operator_main_1 = "None"

    db.session.commit()


def SET_TASKMANAGEMENT_SENSOR_TASK(id, name, task, mqtt_device_id_1, mqtt_device_name_1, mqtt_device_inputs_1,  
                                                   sensor_key_1, operator_1, value_1, operator_main_1,
                                                   mqtt_device_id_2, mqtt_device_name_2, mqtt_device_inputs_2, 
                                                   sensor_key_2, operator_2, value_2, operator_main_2,
                                                   mqtt_device_id_3, mqtt_device_name_3, mqtt_device_inputs_3, 
                                                   sensor_key_3, operator_3, value_3):        
                                                                                        
    entry = Taskmanagement_Sensor.query.filter_by(id=id).first()
    old_name = entry.name

    # values changed ?
    if (entry.name != name or entry.task != task or str(entry.mqtt_device_id_1) != mqtt_device_id_1 or
        entry.sensor_key_1 != sensor_key_1 or entry.operator_1 != operator_1 or entry.value_1 != value_1 or 
        str(entry.mqtt_device_id_2) != mqtt_device_id_2 or entry.sensor_key_2 != sensor_key_2 or 
        entry.operator_2 != operator_2 or entry.value_2 != value_2 or entry.operator_main_1 != operator_main_1 or
        str(entry.mqtt_device_id_3) != mqtt_device_id_3 or entry.sensor_key_3 != sensor_key_3 or 
        entry.operator_3 != operator_3 or entry.value_3 != value_3 or entry.operator_main_2 != operator_main_2):

        entry.name = name        
        entry.task = task
        entry.mqtt_device_id_1 = mqtt_device_id_1
        entry.mqtt_device_name_1 = mqtt_device_name_1
        entry.mqtt_device_inputs_1 = mqtt_device_inputs_1
        entry.sensor_key_1 = sensor_key_1
        entry.operator_1 = operator_1
        entry.value_1 = value_1
        entry.operator_main_1=operator_main_1
        entry.mqtt_device_id_2 = mqtt_device_id_2
        entry.mqtt_device_name_2 = mqtt_device_name_2
        entry.mqtt_device_inputs_2 = mqtt_device_inputs_2
        entry.sensor_key_2 = sensor_key_2
        entry.operator_2 = operator_2
        entry.value_2 = value_2        
        entry.operator_main_2=operator_main_2
        entry.mqtt_device_id_3 = mqtt_device_id_3
        entry.mqtt_device_name_3 = mqtt_device_name_3
        entry.mqtt_device_inputs_3 = mqtt_device_inputs_3
        entry.sensor_key_3 = sensor_key_3
        entry.operator_3 = operator_3
        entry.value_3 = value_3               
        db.session.commit()    

        if operator_main_1 == "not":
            WRITE_LOGFILE_SYSTEM("EVENT", "Database >>> Taskmanagement (Sensor) >>> " + old_name + 
                                  " >>> changed >>> Name: " + name + " /// Task: " + task + 
                                  " /// MQTT-Device_1: " + mqtt_device_name_1 + " /// Sensor_1: " + sensor_key_1 + 
                                  " /// Operator_1: " + str(operator_1) + " /// Value_1: " +  str(value_1)) 
                                 
        if operator_main_2 == "not":
            WRITE_LOGFILE_SYSTEM("EVENT", "Database >>> Taskmanagement (Sensor) >>> " + old_name + 
                                 " >>> changed >>> Name: " + name + " /// Task: " + task + 
                                 " /// MQTT-Device_1: " + mqtt_device_name_1 + " /// Sensor_1: " + sensor_key_1 + 
                                 " /// Operator_1: " + str(operator_1) + " /// Value_1: " +  str(value_1) + 
                                 " /// MQTT-Device_2: " + mqtt_device_name_2 + " /// Sensor_2: " + sensor_key_2 + 
                                 " /// Operator_2: " + str(operator_2) + " /// Value_2: " +  str(value_2))
                                   
        else:
            WRITE_LOGFILE_SYSTEM("EVENT", "Database >>> Taskmanagement (Sensor) >>> " + old_name + 
                                 " >>> changed >>> Name: " + name + " /// Task: " + task + 
                                 " /// MQTT-Device_1: " + mqtt_device_name_1 + " /// Sensor_1: " + sensor_key_1 + 
                                 " /// Operator_1: " + str(operator_1) + " /// Value_1: " +  str(value_1) + 
                                 " /// MQTT-Device_2: " + mqtt_device_name_2 + " /// Sensor_2: " + sensor_key_2 + 
                                 " /// Operator_2: " + str(operator_2) + " /// Value_2: " +  str(value_2) +
                                 " /// MQTT-Device_3: " + mqtt_device_name_3 + " /// Sensor_3: " + sensor_key_3 + 
                                 " /// Operator_3: " + str(operator_3) + " /// Value_3: " +  str(value_3))


def DELETE_TASKMANAGEMENT_SENSOR_TASK(task_id, log = ""):
    entry = GET_TASKMANAGEMENT_SENSOR_TASK_BY_ID(task_id)

    if log == "":
        WRITE_LOGFILE_SYSTEM("EVENT", "Database >>> Taskmanagement (Sensor) >>> " + entry.name + " >>> deleted")    
    
    Taskmanagement_Sensor.query.filter_by(id=task_id).delete()
    db.session.commit()


""" ################### """
""" ################### """
"""   user management   """
""" ################### """
""" ################### """


def GET_USER_BY_ID(user_id):
    return User.query.get(int(user_id))


def GET_USER_BY_NAME(user_name):
    return User.query.filter_by(username=user_name).first()


def GET_EMAIL(email):
    return User.query.filter_by(email=email).first()


def GET_ALL_USERS():
    return User.query.all()


def ADD_USER(user_name, email, password):
    new_user = User(username=user_name, email=email, password=password)
    db.session.add(new_user)
    db.session.commit()

    WRITE_LOGFILE_SYSTEM("EVENT", "Database >>> User >>> " + user_name + " >>> added") 


def SET_USER_SETTINGS(id, username, email, role, email_notification_info, email_notification_error, email_notification_camera):
    entry = User.query.filter_by(id=id).first()
    old_username = entry.username

    # values changed ?
    if (entry.username != username or entry.email != email or entry.role != role or
        entry.email_notification_info   != email_notification_info or
        entry.email_notification_error  != email_notification_error or
        entry.email_notification_camera != email_notification_camera):

        entry.username = username
        entry.email = email
        entry.role = role
        entry.email_notification_info   = email_notification_info
        entry.email_notification_error  = email_notification_error
        entry.email_notification_camera = email_notification_camera
        db.session.commit()
        
        WRITE_LOGFILE_SYSTEM("EVENT", "Database >>> User >>> " + old_username + " >>> changed >>> Username: " +
                             entry.username + " /// eMail: " + entry.email + " /// Role: " + role + 
                             " /// eMail-Info: " + email_notification_info +
                             " /// eMail-Error: " + email_notification_error +
                             " /// eMail-Camera: " + email_notification_camera)


def DELETE_USER(user_id):
    entry = GET_USER_BY_ID(user_id)
    WRITE_LOGFILE_SYSTEM("EVENT", "Database >>> User >>> " + entry.username + " >>> deleted")    
    
    User.query.filter_by(id=user_id).delete()
    db.session.commit()

""" ################### """
""" ################### """
"""        zigbee       """
""" ################### """
""" ################### """

    
def GET_ZIGBEE_PAIRING():
    return ZigBee.query.filter_by().first().pairing


def SET_ZIGBEE_PAIRING(setting):
    entry = ZigBee.query.filter_by().first()
    entry.pairing = setting
    db.session.commit()
