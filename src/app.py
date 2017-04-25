from __future__ import print_function # In python 2.7
import json
import random
import sys
from flask import Flask, request, render_template, send_from_directory, session, jsonify
from socketIO_client import SocketIO, BaseNamespace, LoggingNamespace
from utils import printToConsole 
import threading

# import logging
# logging.getLogger('socketIO-client').setLevel(logging.DEBUG)
# logging.basicConfig()

app = Flask(__name__)


class NamespaceOne(BaseNamespace):
  def on_connect(self):
    self.socketId = 'NameSpace1',
    print('-----------------------------', file=sys.stderr)
    print('Socket ID:', self.socketId, '[Connected]', file=sys.stderr)
    print('-----------------------------', file=sys.stderr)
  def on_test_event_from_node(self, *args):
    print('-----------------------------', file=sys.stderr)
    print('Socket ID: ', self.socketId, '(For All Clients)[Recieved test_event_from_node]', args, file=sys.stderr)
    print('-----------------------------', file=sys.stderr)
    self.emit('new_connection', { 'name': self.socketId })
  # def on_test(self, *args):
  #   print('-----------------------------', file=sys.stderr)
  #   print('Socket ID:', self.socketId, '[Test]', args, file=sys.stderr)
  #   print('-----------------------------', file=sys.stderr)
  def new_connection_recieved(self, *args):
    print('-----------------------------', file=sys.stderr)
    print('Socket ID:', self.socketId, '[A new socket was opened]', args, file=sys.stderr)
    print('-----------------------------', file=sys.stderr)
    #event only to people in name space 

class NamespaceTwo(BaseNamespace):
  def on_connect(self):
    self.socketId = 'NameSpace2',
    print('-----------------------------', file=sys.stderr)
    print('Socket ID:', self.socketId, '[Connected]', file=sys.stderr)
    print('-----------------------------', file=sys.stderr)
  def on_test_event_from_node(self, *args):
    print('-----------------------------', file=sys.stderr)
    print('Socket ID: ', self.socketId, '(For All Clients)[Recieved test_event_from_node]', args, file=sys.stderr)
    print('-----------------------------', file=sys.stderr)
    self.emit('new_connection', { 'name': self.socketId })
  # def on_test(self, *args):
  #   print('-----------------------------', file=sys.stderr)
  #   print('Socket ID:', self.socketId, '[Test]', args, file=sys.stderr)
  #   print('-----------------------------', file=sys.stderr)
  def new_connection_recieved(self, *args):
    print('-----------------------------', file=sys.stderr)
    print('Socket ID:', self.socketId, '[A new socket was opened]', args, file=sys.stderr)
    print('-----------------------------', file=sys.stderr)
    #event only to people in name space 

@app.route('/')
def hello_world():
  print('hit home route', file=sys.stderr)
  return 'home'

def createSocketConnection(Namespace):
  socketIO = SocketIO('10.1.133.238', 140, Namespace)
  t = threading.Thread(target=socketIO.wait)
  t.daemon = True
  t.start()
# @app.route('/test')
# def test():
#   print('hit test route', file=sys.stderr)
#   socketIO.emit('test', 'testing')
#   return 'test'

if __name__ == '__main__':
  for i in range(0, 2):
    #event only to people in name space 
    if(i == 1):
      createSocketConnection(NamespaceOne)
    else:
      createSocketConnection(NamespaceTwo)


  app.run(host='0.0.0.0', port=9000, debug=True)

