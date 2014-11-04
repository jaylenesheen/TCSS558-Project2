#
# TCSS 558 - Fall 2014
# Project 2, rcp multi threaded client/server 
# File: client_rcp.py
# Authors Wiehan Jiang and Jaylene Sheen
# Date: 11/04/2014
#

import io
import traceback
import logging
import sys
from datetime import datetime
import Pyro4

logging.basicConfig(filename='client_rpc.log', level=logging.INFO)
#logging.info('[INFO][%s]:Client Started.' %str(datetime.now()))
data = " ".join(sys.argv[1:])
request = data
#request=raw_input("Command in your request: ").strip()
data = request
RPC_Server=Pyro4.Proxy("PYRONAME:example.greeting")    # use name server object lookup uri shortcut
#print RPC_Server.get_request(request)

try:
    # Communicate with server

    print "[{0}]Sent:{1}".format(str(datetime.now()),data)
    logging.info("[INFO][{0}]Requesting --> {1}".format(str(datetime.now()),data))
    received = RPC_Server.get_request(request)
    print "[{0}]Received:{1}".format(str(datetime.now()),received)
    logging.info("[INFO][{0}]Received --> {1}".format(str(datetime.now()),received))
    
except Exception, err:
    print "[ERROR][{0}]Error Communicating with the server. Check log for detailed info!".format(str(datetime.now()),sys.exc_info()[0])
    logging.info("[ERROR][{0}]Error Connecting the server -- {1} Check Server Please!".format(str(datetime.now()),sys.exc_info()[0]))
    logging.info("[ERROR][DETAIL]{0}".format(traceback.format_exc()))

finally:
    exit()

