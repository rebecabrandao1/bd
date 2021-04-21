#!/usr/bin/python -u

#!/usr/bin/python -u
import mysql.connector as workbench
import paho.mqtt.client as mqtt
import ssl

workbench_connection = workbench.connect(user='root', password='software1981HS', database='iot_db')
cursor = workbench_connection.cursor()

# MQTT Settings 
MQTT_Broker = "www.iot.hidrosolo.com.br"
MQTT_Port = 8883
Keep_Alive_Interval = 60
MQTT_Topic = "/weather/pywws/#"

# Subscribe
def on_connect(client, userdata, flags, rc):
  mqttc.subscribe(MQTT_Topic, 0)

def on_message(mosq, obj, msg):
  # Prepare Data, separate columns and values
  msg_clear = msg.payload.translate(None, '{}""').split(", ")
  msg_dict =    {}
  for i in range(0, len(msg_clear)):
    msg_dict[msg_clear[i].split(": ")[0]] = msg_clear[i].split(": ")[1]

  # Prepare dynamic sql-statement
  placeholders = ', '.join(['%s'] * len(msg_dict))
  columns = ', '.join(msg_dict.keys())
  sql = "INSERT INTO pws ( %s ) VALUES ( %s )" % (columns, placeholders)

  # Save Data into DB Table
  try:
      cursor.execute(sql, msg_dict.values())
  except workbench.Error as error:
      print("Error: {}".format(error))
  workbench_connection.commit()

def on_subscribe(mosq, obj, mid, granted_qos):
  pass

mqttc = mqtt.Client()

# Assign event callbacks
mqttc.on_message = on_message
mqttc.on_connect = on_connect
mqttc.on_subscribe = on_subscribe

# Connect
mqttc.tls_set(ca_certs="ca.crt", tls_version=ssl.PROTOCOL_TLSv1_2)
mqttc.connect(MQTT_Broker, int(MQTT_Port), int(Keep_Alive_Interval))

# Continue the network loop & close db-connection
mqttc.loop_forever()
workbench_connection.close()