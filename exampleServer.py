from jsonSocket import JSONClient
from threadedServer import ThreadedServerSender
import time
import logging
import socket


logger = logging.getLogger("jsonSocket Example")
logger.setLevel(logging.DEBUG)
FORMAT = '[%(asctime)-15s][%(levelname)s][%(funcName)s] %(message)s'

logging.basicConfig(format=FORMAT)


def main() :
	server = ThreadedServerSender()
	server.start()

	while not server.isThereAnyClient() :
		logger.info("waiting for client to connect...")
		time.sleep(2)
	
	i = 0
	while True :
		obj = {"i":i}
		server.sendMessage( obj )
		logger.info("server sends : {}".format(obj))
		time.sleep(1)
		
		# reception :
		obj = None
		try :
			obj = server.readObj()
			logger.info("server received: ---{}---".format(obj) )
		
			#check the message :
			if 'close' in obj.keys() :
				if obj['close'] :
					logger.info("server received a TRUE closing command.")
					break
				else :
					logger.info("server received a FALSE closing command.")
					
		except socket.timeout as e :
			logger.debug("server socket.timeout: {}".format(e) )
			continue
		except Exception as e :
			logger.error("server: {}".format(e) )
			break

		i = i+1

	server.stop()
	time.sleep(1)
	server.close()
	
	

if __name__ == "__main__" :
	''' server for integers that stops when it receives a message.'''
	main()

	
