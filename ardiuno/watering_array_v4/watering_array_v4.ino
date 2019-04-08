String ieeeAddr = "0x99999";

const char* ssid        = ""; 
const char* password    = ""; 
const char* mqtt_server = "";

#include <ESP8266WiFi.h>
#include <PubSubClient.h>
#include <MCP3008.h>

// mqtt connection
WiFiClient espClient;
PubSubClient client(espClient);
long lastMsg = 0;
char msg[200];
char path[50];
int value = 0;

// MCP3008
#define CS_PIN 15
#define CLOCK_PIN 14
#define MOSI_PIN 13
#define MISO_PIN 12
MCP3008 adc(CLOCK_PIN, MOSI_PIN, MISO_PIN, CS_PIN); 

// OUTPUT 
int Pin_D0 = 16;
int Pin_D1 = 5;
int Pin_D2 = 4;
int Pin_D3 = 0;

// Light Sensor
#define LIGHTPIN A0  

// split string
String getValue(String data, char separator, int index) {
    int found = 0;
    int strIndex[] = {0, -1};
    int maxIndex = data.length()-1;
  
    for(int i=0; i<=maxIndex && found<=index; i++){
        if(data.charAt(i)==separator || i==maxIndex){
            found++;
            strIndex[0] = strIndex[1]+1;
            strIndex[1] = (i == maxIndex) ? i+1 : i;
        }
    } 
    return found>index ? data.substring(strIndex[0], strIndex[1]) : "";
}

void setup_wifi() {
    delay(10);
    Serial.println();
    Serial.print("Connecting to ");
    Serial.println(ssid);
  
    WiFi.begin(ssid, password);
  
    while (WiFi.status() != WL_CONNECTED) {
        delay(500);
        Serial.print(".");
      }
  
    randomSeed(micros());
  
    Serial.println("");
    Serial.println("WiFi connected");
    Serial.println("IP address: ");
    Serial.println(WiFi.localIP());
}

void callback(char* topic, byte* payload, unsigned int length) {

    Serial.println("######################");
    Serial.print("Channel: ");
    Serial.println(topic);
    Serial.println("######################");

    String check_ieeeAddr = getValue(topic,'/',2);
    String check_command  = getValue(topic,'/',3);

    if(check_ieeeAddr == "devices"){

        // create msg  
        String payload = "{\"ieeeAddr\":\"" + ieeeAddr + "\",\"model\":\"watering_array_v4\",\"input\":8,\"output\":4}";      
        char attributes[50];
        payload.toCharArray( msg, 100 );
        
        Serial.print("Publish message: ");
        Serial.println(msg);
        Serial.print("Channel: ");
        Serial.println("SmartHome/mqtt/log");
        Serial.println();        
        client.publish("SmartHome/mqtt/log", msg);        
    }

    if(check_ieeeAddr == ieeeAddr and check_command == "get"){
      
        int sensor_0 = adc.readADC(0) - 1; 
        String STR_sensor_0 = String(sensor_0);
        int sensor_1 = adc.readADC(1) - 1; 
        String STR_sensor_1 = String(sensor_1);
        int sensor_2 = adc.readADC(2) - 1; 
        String STR_sensor_2 = String(sensor_2);  
        int sensor_3 = adc.readADC(3) - 1; 
        String STR_sensor_3 = String(sensor_3);
        int sensor_4 = adc.readADC(4) - 1; 
        String STR_sensor_4 = String(sensor_4);
        int sensor_5 = adc.readADC(5) - 1; 
        String STR_sensor_5 = String(sensor_5);
        int sensor_6 = adc.readADC(6) - 1; 
        String STR_sensor_6 = String(sensor_6);
        int sensor_7 = adc.readADC(7) - 1; 
        String STR_sensor_7 = String(sensor_7);

        // create msg   
        String payload_msg = "{\"sensor_0\":" + STR_sensor_0 + 
                             ",\"sensor_1\":" + STR_sensor_1 + 
                             ",\"sensor_2\":" + STR_sensor_2 +
                             ",\"sensor_3\":" + STR_sensor_3 +
                             ",\"sensor_4\":" + STR_sensor_4 +
                             ",\"sensor_5\":" + STR_sensor_5 +
                             ",\"sensor_6\":" + STR_sensor_6 +
                             ",\"sensor_7\":" + STR_sensor_7 + "}";
        char attributes_msg[100];
        payload_msg.toCharArray(  msg, 200 );

        // create path   
        String payload_path = "SmartHome/mqtt/" + ieeeAddr;
        char attributes_path[100];
        payload_path.toCharArray( path, 100 );        

        Serial.print("Publish message: ");
        Serial.println(msg);
        Serial.print("Channel: ");
        Serial.println("SmartHome/mqtt/" + ieeeAddr);
        Serial.println();
        client.publish(path, msg);         
    }    

    if(check_ieeeAddr == ieeeAddr and check_command == "set"){

        char msg[length+1];
  
        for (int i = 0; i < length; i++) {
            msg[i] = (char)payload[i];
        }
        msg[length] = '\0';
        
        Serial.print("msg: ");
        Serial.println(msg);

        // create path   
        String payload_path = "SmartHome/mqtt/" + ieeeAddr;
        char attributes_path[100];
        payload_path.toCharArray( path, 100 );          

        // get command
        String data_temp     = getValue(msg,':',1);      
        String output_number = getValue(data_temp,'=',0);
        String output_state  = getValue(data_temp,'=',1);
        
        if (output_number == "0") {
            if (output_state == "on") {
                digitalWrite(Pin_D0, HIGH);
                client.publish(path, "0_on");
                Serial.println("Start_Pump_0");
            }
            else {
                digitalWrite(Pin_D0, LOW); 
                client.publish(path, "0_off");
                Serial.println("Stop_Pump_0");
            }
        }
        if (output_number == "1") {
            if (output_state == "on") {
                digitalWrite(Pin_D3, HIGH);
                client.publish(path, "1_on");
                Serial.println("Start_Pump_1");
            }
            else {
                digitalWrite(Pin_D3, LOW); 
                client.publish(path, "1_off");                
                Serial.println("Stop_Pump_1");
            }
        }     
        if (output_number == "2") {
            if (output_state == "on") {
                digitalWrite(Pin_D2, HIGH);
                client.publish(path, "2_on");
                Serial.println("Start_Pump_2");
            }
            else {
                digitalWrite(Pin_D2, LOW); 
                client.publish(path, "2_off");
                Serial.println("Stop_Pump_2");
            }
        }
        if (output_number == "3") {
            if (output_state == "on") {
                digitalWrite(Pin_D1, HIGH);
                client.publish(path, "3_on");
                Serial.println("Start_Pump_3");
            }
            else {
                digitalWrite(Pin_D1, LOW); 
                client.publish(path, "3_off");
                Serial.println("Stop_Pump_3");
            }
        }       
    }     
}

void reconnect() {
    while (!client.connected()) {
        Serial.print("Attempting MQTT connection...");
        String clientId = "ESP8266Client-";
        clientId += String(random(0xffff), HEX);

        digitalWrite(BUILTIN_LED, HIGH);
        
        if (client.connect(clientId.c_str())) {     
            // create channel  
            String payload_path = "SmartHome/mqtt/" + ieeeAddr;      
            char attributes[100];
            payload_path.toCharArray( path, 100 );    
                 
            client.publish(path, "connected");
            client.subscribe("SmartHome/mqtt/#");
            Serial.println("MQTT Connected...");

            digitalWrite(BUILTIN_LED, LOW); 
          
        } else {        
            Serial.print("failed, rc=");
            Serial.print(client.state());
            Serial.println(" try again in 5 seconds");
            delay(5000);
        }
    }
}

void setup() {
  
    Serial.begin(115200);
    setup_wifi();
    client.setServer(mqtt_server, 1883);
    client.setCallback(callback);

    pinMode(CS_PIN, OUTPUT);  
    pinMode(Pin_D0,OUTPUT);
    pinMode(Pin_D1,OUTPUT);
    pinMode(Pin_D2,OUTPUT);
    pinMode(Pin_D3,OUTPUT);
    pinMode(BUILTIN_LED, OUTPUT); 
    
}

void loop() {

    if (!client.connected()) {
        reconnect();
    }
    
    client.loop();
}
