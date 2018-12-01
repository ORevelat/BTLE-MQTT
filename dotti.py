
import sys
import ast
import json
import time
import struct

from btleconnector import BTLEConnector
from logger import Logger as logger

class Dotti():
	"""
	DOTTI interfacing

	Small class that allow to set Hour mode or fill all pixel with a specific color 
	
	Requirements:
		- see https://github.com/MartyMacGyver/dotti-interfacing
	"""

	name = 'dotti'

	def __init__(self, mac):
		self.name = Dotti.name
		self.mac = mac

	def __twoDigitHex(self, number):
		return '%02x' % number

	def mode(self, mode = 'hour', color = [0, 0, 0]):
		"""
		Update Dotti to the given mode
		
		Args:
			mode (str): either 'hour' or 'color'
			color (arr[int, int, int]): R,G,B color to use
		"""

		try:
			conn = BTLEConnector(self.mac)
			if not conn.connect():
				if not conn.connect():
					return None
		
			if mode == 'color':
				conn.writeCharacteristic('0x2a', '0601'+self.__twoDigitHex(int(color[0]))+self.__twoDigitHex(int(color[1]))+self.__twoDigitHex(int(color[2]))+'00')
			elif mode == 'hour':
				conn.writeCharacteristic('0x2a', '040502')

		except Exception as error:
			logger.error(str(error))

		conn.disconnect()

	def handle_message(self, data):
		try:
			j = json.loads(str(data.decode("utf-8")))
		
			mode = str(j["mode"])
			color = [0,0,0]
			if mode == "color" and "color" in j:
				color = ast.literal_eval(str(j["color"]))

			if mode == "exit":
				return False

			if mode != "hour" and mode != "color":
				logger.error("Dotti --- unknown mode=" + mode)
				return None

			self.mode(mode, color)
		
		except ValueError:
			logger.error("Dotti -- decoding payload failed !")
		except:
			logger.error("Dotti -- processing payload failed !")

		return None
