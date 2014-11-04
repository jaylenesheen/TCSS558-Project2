import pickle
import sys
import re
import os.path
import logging
import datetime
from datetime import datetime
import Pyro4
import os

#
# TCSS 558 - Fall 2014
# Project 2, rcp multi threaded client/server
# File: client_rcp.py
# Authors Wiehan Jiang and Jaylene Sheen
# Date: 11/04/2014
#

class RPC_Server(object):
    def get_request(self, request):
        print "\n[INFO][%s]+++++++++ new requesting coming in +++++++++" %str(datetime.now())
        logging.info('[INFO][%s]:+++++++++ new requesting coming in ++++++++.' %str(datetime.now()))
        print "[INFO][{0}]Following request coming from Client:".format(str(datetime.now()))
        logging.info('[INFO][{0}]Request coming from Client:'.format(str(datetime.now())))
        self.db_init()
        self.data = request
        print "[INFO]Request detail --> \"{0}\"".format(self.data)
        parsed_data = self.input_parser()
        sent_back_db_value = self.db_operation(parsed_data)
        print "[INFO][%s]Server responding -->  %s" %(str(datetime.now()),sent_back_db_value)
        logging.info("[INFO][%s]Server responding -->  %s" %(str(datetime.now()),sent_back_db_value))
        print "[INFO][%s]+++++++++ this request session completes ++++++++\n" %str(datetime.now())
        logging.info("[INFO][%s]+++++++++ this request session completes ++++++++"%str(datetime.now()))
        return "{0}".format(sent_back_db_value)


    def db_init(self):
        # initiate a DB once server gets running
        if not os.path.isfile('db_on_disk'):
           self.db = {'Jaylene': '2533550659', 'Weihan': '2065197252'}           
           pickle.dump(self.db, open('db_on_disk', 'wb'))
        if (os.path.isfile('db_on_disk')):
           self.db = pickle.load(open('db_on_disk', 'rb'))


    def replace_acronym(self,a_dict,check_for,replacement_key,replacement_text):
        c = a_dict.get(check_for)
        if c is not None:
          del a_dict[check_for]
          a_dict[replacement_key] = replacement_text
          self.db = a_dict
        elif c is None:
          a_dict[replacement_key] = replacement_text
          self.db = a_dict
          print self.db
        pickle.dump(self.db, open('db_on_disk', 'wb'))
        return self.db

    def purge_db(self,a_dict,check_for):
        c = a_dict.get(check_for)
        if c is not None:
          del a_dict[check_for]
          self.db = a_dict
          pickle.dump(self.db, open('db_on_disk', 'wb'))
        elif c is None:
          pass   #here need send warning message to client



    def db_operation(self, input):
        # initiate a DB once server gets running
#        self.db = {'Jaylene': '2533550659', 'Weihan': '2065197252'}
        if re.findall(r"error_input", input[0]):
           return 'Invalid Input, now we support four oprands {QUERY|GET arg1|PUT arg1 arg2|DELETE arg1}'
        if re.findall(r"GET", input[0]):
           if (input[1] in self.db): 
              return_string = "The value of KEY \"%s\" is %s" %(input[1],self.db[input[1]])
              return return_string
           else:
              return_string = "The KEY is not in DB. Try {QUERY} or {PUT} to add one." 
              return return_string
        if re.findall(r"PUT", input[0]):
#           self.db[input[1]] = input[2]
           self.replace_acronym(self.db,input[1],input[1],input[2]) 
           return_string = "Key/Value Pair {%s/%s} has been added to DB" %(input[1],input[2])
           return return_string
        if re.findall(r"QUERY", input[0]):
           return_string = "DB status: %s"% self.db
           return return_string
        if re.findall(r"DELETE", input[0]):
           self.purge_db(self.db,input[1]) 
           return_string = "Key/Value Pair of KEY {%s} has been purged from DB" %(input[1])
           return return_string


    def input_parser(self):
        #parses the query from client, to check either it is a PUT or GET

        m = re.match(r"(?P<KEY>\w+) (?P<INPUT>.*)", "%s" %self.data)
        if (m.group('KEY') == 'QUERY'):
          return ['QUERY'] 
        if (m.group('KEY') == 'PUT'):
          m1 = re.match(r"(?P<INPUT1>\w+) (?P<INPUT2>\w+)", m.group('INPUT'))
          return [m.group('KEY'),m1.group('INPUT1'),m1.group('INPUT2')] 
        elif not (m.group('KEY') == 'PUT'):
          return [m.group('KEY'),m.group('INPUT')]
        else:
          return ['error_input']


logging.basicConfig(filename='server_rpc.log', level=logging.INFO)
logging.info('[%s]:Name Server Started.' %str(datetime.now()))
os.system("nohup python -m Pyro4.naming &")
logging.info('[%s]:Server Started.' %str(datetime.now()))

greeting_maker=RPC_Server()

daemon=Pyro4.Daemon()                 # make a Pyro daemon
ns=Pyro4.locateNS()                   # find the name server
uri=daemon.register(greeting_maker)   # register the greeting object as a Pyro object
ns.register("example.greeting", uri)  # register the object with a name in the name server

print "Server is Up and Ready."
daemon.requestLoop()                  # start the event loop of the server to wait for calls
