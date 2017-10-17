from jsonSocket import JSONClient
from threadedServer import ThreadedServer, ThreadedServerSender
import time
import logging


logger = logging.getLogger("jsonSocket Example")
logger.setLevel(logging.DEBUG)
FORMAT = '[%(asctime)-15s][%(levelname)s][%(funcName)s] %(message)s'

logging.basicConfig(format=FORMAT)


def test1() :
	server = Server()
	server.start()

	time.sleep(2)


	logger.debug("starting JSONClient")
	client = JSONClient()
	resultConnect = client.connect()
	logger.debug( "connection of the client : {}".format( resultConnect ) )
	
	i = 0
	while i < 10 :
		client.sendObj( {"i":i} )
		try :
			msg = client.readObj()
			logger.info("client received: ---{}---".format(msg) )
		except socket.timeout as e :
			logger.debug("client socket.timeout: {}".format(e) )
			continue
		except Exception as e :
			logger.error("client: {}".format(e) )
			break

		i = i+1

	return client,server

	

def test2() :
	server = Server()
	server.start()

	time.sleep(2)


	logger.debug("starting JSONClient")
	client = JSONClient()
	resultConnect = client.connect()
	logger.debug( "connection of the client : {}".format( resultConnect ) )
	
	i = 0
	while i < 5 :
		client.sendObj( {"i":i} )
		time.sleep(1)
		i = i+1

	return client,server


def test3() :
	server = ThreadedServerSender()
	server.start()

	time.sleep(2)


	logger.debug("starting JSONClient")
	client = JSONClient()
	resultConnect = client.connect()
	logger.debug( "connection of the client : {}".format( resultConnect ) )
	
	i = 0
	while i < 5 :
		server.sendMessage( {"i":i} )
		time.sleep(2)
		obj = None
		while obj is None :
			obj = client.readObj()
			logger.info("client received: ---{}---".format(obj) )

		i = i+1

	return client,server

class Server(ThreadedServer) :
		def __init__(self) :
			super(Server, self).__init__()
			#self.timeout = 2.0

		def _processMessage(self,obj) :
			logger.info("SERVER received: ---{}---".format(obj) )
			self.sendObj(obj)

	

if __name__ == "__main__" :
	"""echo server """
	
	#client, server = test1()
	#client, server = test2()
	client, server = test3()

	server.stop()

	time.sleep(1)

	server.close()
	client.close()

