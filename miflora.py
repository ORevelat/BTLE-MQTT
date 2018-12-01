
from btleconnector import BTLEConnector
from logger import Logger as logger

import devices

class MiFlora():
	"""
	Xiaomi MiFlora sensor interfacing

    """

	name = 'miflora'

	def __init__(self):
		self.name = MiFlora.name

	def read(self, mac):
		try:
			conn = BTLEConnector(mac)
			if not conn.connect():
				if not conn.connect():
					return None

			res = conn.readCharacteristic('0x38')
			if res is False:
				return None

			batt = bytearray(res)

			# live mode
			conn.writeCharacteristic('0x33','a01f',response=True)

			self._result = {}
			self._result['battery'] = batt[0]
			self._result['id'] = mac

			conn.writeCharacteristic('0x36','0100',response=True)
			conn.set_callback(0x35, self.handlenotification)
			conn.wait(2)
		except Exception as error:
			logger.error(str(error))
		conn.disconnect()

	def handlenotification(self, data):
		received = bytearray(data)
		temperature = float(received[1] * 256 + received[0]) / 10
		light = received[4] * 256 + received[3]
		moisture = received[7]
		fertility = received[9] * 256 + received[8]

		self._result['light'] = light
		self._result['moisture'] = moisture
		self._result['fertility'] = fertility
		self._result['temperature'] = temperature

		devices.update_values(self._result)
