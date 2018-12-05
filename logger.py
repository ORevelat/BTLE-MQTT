import syslog

debug = False

class Logger():

	@staticmethod
	def debug(msg):
		if debug == True:
			print('DEBUG - ' + msg)

	@staticmethod
	def error(msg):
		print('ERROR - ' + msg)
		syslog.syslog(syslog.LOG_ERR, msg)

