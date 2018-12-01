# BTLE-MQTT
Simple MQTT <> BT-LE bridge 

Based on the Jeedom plugin BLEA made by sarakha63

## Geting started

Python server that allows to:

* 1/
examine a BT-LE device every X second
get some characteristics
publish values as json to a specific topic

```
every X sec
scan device mac='xx:xx:xx:xx:xx'
payload = json(on or more characteristics)
publish to mqtt server on topic (using config + device type and name) with payload
```

* 2/
listen to a specific topic (per device)
perform action defined in the receive message payload using a BT-LE device

```
subscribe to topic (using config + device type and name)
on message reception
perform action
```

### Prerequisites

```
pip install paho-mqtt
```

## Deployment

Once the files config.py and devices.py are updated to meet your requirements

```
python3 mqtt.py
```

## Disclamer

I made / use this server to connect my Bluetooth-LE devices to my home automation (Home Assistant).

Sensors used are :
* Xiaomi MiFlora  - temperature, moisture, light, fertility and battery values are read
* Xiaomi TemperatureHygro - temperature, humidity and battery values are read
* Dotti (https://www.wittidesign.com/) - only hour mode and single color mode are developped

Dotti is used have some visual feedbacks in addition to audio messages (through Amazon Echo / Echo Dot) from the Home, e.g. next trash color reminder.
