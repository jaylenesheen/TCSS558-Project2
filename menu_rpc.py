#
# TCSS 558 - Fall 2014
# Project 2, rcp multi threaded client/server 
# File: menu_rcp.py
# Authors Wiehan Jiang and Jaylene Sheen
# Date: 11/04/2014
#
 
import cmd
import logging
import os
import sys
from datetime import datetime

class RPC_Client(cmd.Cmd):
    """Simple command processor."""

    def do_GET(self, person):
        """GET [person]
        GET the phone number of this person"""
        if person:
           os.system('python client_rpc.py GET %s' %(person))
        else:
            print 'Invalid Syntax! Try {GET argument1}'

    def do_QUERY(self, line):
        """QUERY [no argument]
        Query all data in DB"""

        os.system('python client_rpc.py QUERY all')


    def do_PUT(self, person_number):
        """PUT [person number] 
        Add key/value to DB"""
        if person_number:
           os.system('python client_rpc.py PUT %s'%(person_number))
        else:
            print 'Invalid Syntax! Try {PUT argument1 argument2}'


    def do_DELETE(self, person):
        """DELETE [person]
        Delete the key [person] and its value in DB"""
        if person:
           os.system('python client_rpc.py DELETE %s' %(person))
        else:
            print 'Invalid Syntax! Try {DELETE argument1}'

    def do_exit(self, line):
        """exit [no argument]
        Gracefully exit the CMD Menu"""
        print "[{0}]Shutting the Client down...".format(str(datetime.now()))
        print "[{0}]Client has been shut down...".format(str(datetime.now()))
        logging.info("[{0}]Client is gracefully shut down.".format(str(datetime.now())))
        return True

if __name__ == '__main__':
    logging.basicConfig(filename='client_rpc.log', level=logging.INFO)
    logging.info('[INFO][%s]:Client Started.' %str(datetime.now()))
    print "[TEST][{0}]Start to pre-populating the following 5 pairs of data when Client is up.".format(str(datetime.now()))
    logging.info("[TEST][{0}]Start to pre-populating the following 5 pairs of data when Client is up".format(str(datetime.now())))
    RPC_Client().do_PUT("person1 number1")
    RPC_Client().do_PUT("person2 number2")
    RPC_Client().do_PUT("person3 number3")
    RPC_Client().do_PUT("person4 number4")
    RPC_Client().do_PUT("person5 number5")
    print "[TEST][{0}]Get value from each pair.".format(str(datetime.now()))
    logging.info("[TEST][{0}]Get value from each pair.".format(str(datetime.now())))
    RPC_Client().do_GET('person1')
    RPC_Client().do_GET('person2')
    RPC_Client().do_GET('person3')
    RPC_Client().do_GET('person4')
    RPC_Client().do_GET('person5')
    print "[TEST][{0}]Cleansing the pre-populated pairs.".format(str(datetime.now()))
    logging.info("[TEST][{0}]Cleansing the pre-populated pairs of data.".format(str(datetime.now())))
    RPC_Client().do_DELETE('person1')
    RPC_Client().do_DELETE('person2')
    RPC_Client().do_DELETE('person3')
    RPC_Client().do_DELETE('person4')
    RPC_Client().do_DELETE('person5')

#   doing initial setup of ports, hostname, and instance
    print "\n"
    print "*** Welcome to TCSS558 Group7 Project2 *** \n"
    print "***                                    *** \n"    
    print "***     Input cmd or help or exit      *** \n"    
    print "***                                    *** \n"    
    print "****************************************** \n"    

#    print "[INFO]By default the client is using <localhost>:<port-9999> via TCP"    
#    print "[INFO]To customize them, use cmd <port>, <hostname>, and <network>"

    RPC_Client().cmdloop()
