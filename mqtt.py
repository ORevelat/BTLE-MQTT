import paho.mqtt.client as mqtt
import ast
import json
import syslog
import time

from threading import Thread

from config import MqttConfig
from logger import Logger as logger

import devices

from xiaomitemphygro import XiaomiTempHygro
from miflora import MiFlora
from dotti import Dotti

mqtt_topic_handle = {}

"""

Entry point
	- server to run continuously
	-  mqtt client that publish if necessary message
	-  mqtt client that listen to a topic

Requirements:
	- pip install paho-mqtt
	
"""

def mqtt_on_message(client, userdata, message):
	if message.topic in mqtt_topic_handle:
		Thread(target = mqtt_topic_handle[message.topic], args = (message.payload, )).start()

def mqtt_on_log(client, userdata, level, buf):
    logger.debug("mqtt_on_log: " + buf)

## perform reading of sensor information once
def btle_connect(device):
	if device is None:
		return
	
	x = None
	if device['sensor'] == XiaomiTempHygro.name:
		x = XiaomiTempHygro()
	if device['sensor'] == MiFlora.name:
		x = MiFlora()

	if x is not None:
		x.read(device['mac'])

## initialise mqtt listeners
def mqtt_listeners():
	for d in devices.KNOWN_DEVICES:
		x = None
		if d['sensor'] == Dotti.name:
			x = Dotti(d['mac'])

		if x is not None:
			topic = MqttConfig.server_topic + d['sensor'] + '/' + d['name']
			logger.debug('subscribe to ' + topic)
			client.subscribe(topic)

			mqtt_topic_handle[topic] = x.handle_message

## initialise mqtt client
client = mqtt.Client("hass-ble-client1")
client.username_pw_set(MqttConfig.user_name, MqttConfig.user_pwd)

client.on_message = mqtt_on_message

client.connect(MqttConfig.server_addr, MqttConfig.server_port)
client.loop_start()

mqtt_listeners()

## main loop to get btle sensor information
try:
	DoNotExit = True
	while DoNotExit:

		## get sensors information
		for d in devices.KNOWN_DEVICES:
			beat = d['last_beat']
			now = int(time.time())
			if (beat == 0) or (now - beat > d['timer']):
				d['last_beat'] = now
				logger.debug(d['name'])

				Thread(target = btle_connect, args = (d, )).start()

		## publish sensors information to mqtt
		for d in devices.KNOWN_DEVICES:
			if d['last_update'] == 0:
				continue

			if d['last_update'] > d['last_publish'] + 5:
				d['last_publish'] = int(time.time())

				topic = MqttConfig.server_topic + d['sensor'] + '/' + d['name']
				msg = json.dumps(d['values'])

				syslog.syslog(syslog.LOG_NOTICE, topic + ' == ' + msg)
				client.publish(topic, payload=msg, qos=1)

		time.sleep(1)

except KeyboardInterrupt:
	logger.error('interrupted!')

## clear mqtt client
client.loop_stop()
