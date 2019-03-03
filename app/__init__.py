from flask import Flask
from flask_bootstrap import Bootstrap

from app.components.colorpicker_local import colorpicker

""" ###### """
""" flasks """
""" ###### """

PATH = "/home/pi/Python/SmartHome"

UPLOAD_FOLDER = PATH + "/app/snowboy/resources/"

app = Flask(__name__)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'Thisissupposedtobesecret!'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
Bootstrap(app)
colorpicker(app)

from app.sites import index, user_login, dashboard, led, schedular, plants, settings
from app.components.plants_control import *
from app.database.database import *
from app.components.pixel_ring import PIXEL_RING_CONTROL


# stop all pumps
for plant in GET_ALL_PLANTS():
    STOP_PUMP(plant.pump_id) 
     
# deactivate pixel_ring
PIXEL_RING_CONTROL("off")


# start flask
class flask_Thread(threading.Thread):
    def __init__(self, ID = 1, name = "flask_Thread"):
        threading.Thread.__init__(self)
        self.ID = ID
        self.name = name

    def run(self):
        print("###### Start FLASK ######")

        @app.before_first_request
        def initialisation():
            pass

        app.run(host="0.0.0.0")
        #app.run()
    
t1 = flask_Thread()
t1.start()


# start snowboy
if GET_SETTING_VALUE("snowboy") == "True":
    try:
        from app.snowboy.snowboy import SNOWBOY_START

        print("###### Start SNOWBOY ######")
        SNOWBOY_START()

    except Exception as e:
        print("Fehler in SnowBoy: " + str(e))
