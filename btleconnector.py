import time
import struct
import bluepy.bluepy.btle as btle
from threading import Thread

from logger import Logger as logger

class BTLEConnector(btle.DefaultDelegate):

	def __init__(self, mac):
		btle.DefaultDelegate.__init__(self)
		
		self._conn = btle.Peripheral()
		self._conn.withDelegate(self)
		self._mac = mac
		self._isconnected = False
		self._callbacks = {}

	def connect(self, retry=3, type='public'):
		logger.debug('BTLEConnector --- connecting : ' + str(self._mac))

		addrType = btle.ADDR_TYPE_PUBLIC
		if type != 'public':
			addrType = btle.ADDR_TYPE_RANDOM

		timeout = time.time() + 30

		for retrying in range(1, 3):
			try:
				self._conn.connect(self._mac, addrType=addrType)
				self._isconnected = True
				logger.debug('BTLEConnector --- connected to device ' + str(self._mac))
				return True

			except btle.BTLEException as ex:
				logger.debug('BTLEConnector --- unable to connect to device ' + str(self._mac) + ', ' + str(ex) + ' - attempt ' + str(retrying) + ', retrying ...')

				if time.time() > timeout:
					logger.debug('BTLEConnector --- issue connecting (exceeded 30s) to device ' + str(self._mac) + ' : the device is busy or too far')
					self._isconnected = False
					return False

		logger.error('BTLEConnector --- issue connecting to device ' + str(self._mac) + ' : the device is busy or too far')
		self._isconnected = False
		return False

	def disconnect(self):
		logger.debug('BTLEConnector --- disconnected : ' + str(self._mac))
		if self._conn:
			self._conn.disconnect()
			self._conn = None

	def wait(self, sec):
		end = time.time() + sec
		while time.time() < end:
			self._conn.waitForNotifications(timeout=0.1)
	
	def handleNotification(self, handle, data):
		logger.debug("BTLEConnector --- got notification from " + str(handle))
		if handle in self._callbacks:
			self._callbacks[handle](data)

	@property
	def mac(self):
		"""Return the MAC address of the connected device."""
		return self._mac

	def set_callback(self, handle, function):
		"""Set the callback for a Notification handle. It will be called with the parameter data, which is binary."""
		self._callbacks[handle] = function

	def readCharacteristic(self, handle, retry=1, type='public'):
		logger.debug('BTLEConnector ---readCharacteristic for device '+ str(self._mac))
		try:
			result = self._conn.readCharacteristic(int(handle,16))
			logger.debug('BTLEConnector --- readCharacteristic done for ' + str(self._mac))
			return result
		except Exception as e:
			logger.error('BTLEConnector --- readCharacteristic failed for device ' + str(self._mac) + ' : ' + str(e))
			return False

	def writeCharacteristic(self, handle, value, response=False, type='public'):
		logger.debug('BTLEConnector ---writeCharacteristic for device ' + str(self._mac))
		try:
			arrayValue = [int('0x'+value[i:i+2],16) for i in range(0, len(value), 2)]
			result = self._conn.writeCharacteristic(int(handle,16),struct.pack('<%dB' % (len(arrayValue)), *arrayValue), response)
	
			logger.debug('BTLEConnector --- writeCharacteristic done for ' + str(self._mac))
			if result :
				logger.debug(str(result))
			return True
		except Exception as e:
			logger.error('BTLEConnector --- writeCharacteristic failed for device ' + str(self._mac) + ' : ' + str(e))
			return False
	
	def getCharacteristics(self, handle='', handleend='', type='public'):
		logger.debug('BTLEConnector --- getCharacteristics for device ' + str(self._mac))
		if handleend == '':
			handleend = handle
		try:
			if handle == '':
				char = self._conn.getCharacteristics()
			else:
				char = self._conn.getCharacteristics(int(handle,16), int(handleend,16)+4)
			
			logger.debug('BTLEConnector ---- getCharacteristics gotten for device ' + str(self._mac))
			return char
		except Exception as e:
			logger.error('BTLEConnector --- getCharacteristics failed for device ' + str(self._mac) + ' : ' + str(e))
			return False
