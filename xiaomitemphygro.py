
from btleconnector import BTLEConnector
from logger import Logger as logger

import devices

class XiaomiTempHygro:
	"""
	Xiaomi Temperature-Hygro sensor interfacing

	"""
	name = 'xiaomith'

	def __init__(self):
		self.name = XiaomiTempHygro.name

	def read(self, mac):
		try:
			conn = BTLEConnector(mac)
			if not conn.connect():
				if not conn.connect():
					return None

			res = conn.readCharacteristic('0x18')
			if res is False:
				return None

			batt = bytearray(res)
			battery = batt[0]

			self._result = {}
			self._result['battery'] = battery
			self._result['id'] = mac

			conn.set_callback(0xe, self.handlenotification)
			conn.writeCharacteristic('0x10', '0100', response=True)
			conn.wait(2)
		except Exception as error:
			logger.error(str(error))
		conn.disconnect()

	def handlenotification(self, data):
		received = bytearray(data)
		s = "".join(map(chr, received)).replace("T=", "").replace("H=", "").rstrip(' \t\r\n\0')
		temp, hum = s.split(" ", 1)

		self._result['humidity'] = float(hum)
		self._result['temperature'] = float(temp)

		devices.update_values(self._result)
