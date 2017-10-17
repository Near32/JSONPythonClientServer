import jsonSocket
import threading
import socket

import logging

logger = logging.getLogger("ThreadedServer")
logger.setLevel(logging.DEBUG)
FORMAT = '[%(asctime)-15s][%(levelname)s][%(funcName)s] %(message)s'
logging.basicConfig(format=FORMAT)

class ThreadedServer( threading.Thread, jsonSocket.JSONServer) :
	def __init__(self, **kwargs) :
		threading.Thread.__init__(self)
		jsonSocket.JSONServer.__init__(self)
		self._isAlive = False

	def _processMessage(self, obj) :
		pass

	def run(self) :
		self.acceptConnection()
		
		while self._isAlive :
			try :
				obj = self.readObj()
				self._processMessage(obj)
			except socket.timeout as e :
				logger.debug("socket.timeout: {}".format(e) )
				continue
			except Exception as e :
				logger.exception(e)
				break		

	def start(self) :
		self._isAlive = True
		super(ThreadedServer, self).start()

	def stop(self) :
		self._isAlive = False

class ThreadedServerSender( threading.Thread, jsonSocket.JSONServer) :
	def __init__(self, **kwargs) :
		threading.Thread.__init__(self)
		jsonSocket.JSONServer.__init__(self)
		self._isAlive = False
		self.listMessage = []

	def sendMessage(self, obj) :
		self.listMessage.append(obj)

	def run(self) :
		self.acceptConnection()
		
		while self._isAlive :
			try :
				#obj = self.readObj()
				if len(self.listMessage) :
					obj = self.listMessage.pop()
					self.sendObj(obj)
			except socket.timeout as e :
				logger.debug("socket.timeout: {}".format(e) )
				continue
			except Exception as e :
				logger.exception(e)
				break		

	def start(self) :
		self._isAlive = True
		super(ThreadedServerSender, self).start()

	def stop(self) :
		self._isAlive = False

