from __future__ import print_function # In python 2.7
import json
import random
import sys
from flask import Flask, request, render_template, send_from_directory, session, jsonify
from socketIO_client import SocketIO, BaseNamespace, LoggingNamespace
from utils import printToConsole 
import threading

import logging
logging.getLogger('socketIO-client').setLevel(logging.DEBUG)
logging.basicConfig()

app = Flask(__name__)

class Namespace(BaseNamespace):
    def on_connect(self):
      self.socketId = random.randrange(0, 10000),
      print('-----------------------------', file=sys.stderr)
      print('Socket ID:', self.socketId, '[Connected]', file=sys.stderr)
      print('-----------------------------', file=sys.stderr)
    def on_test_event_from_node(self, *args):
      print('-----------------------------', file=sys.stderr)
      print('Socket ID:', self.socketId,'[Recieved test_event_from_node]', args, file=sys.stderr)
      print('-----------------------------', file=sys.stderr)
      self.emit('new_connection', { 'name': self.socketId })
    def on_test(self, *args):
      print('-----------------------------', file=sys.stderr)
      print('Socket ID:', self.socketId, '[Test]', args, file=sys.stderr)
      print('-----------------------------', file=sys.stderr)
    def on_connection_confirmed(self, *args):
      print('-----------------------------', file=sys.stderr)
      print('Socket ID:', self.socketId, '[Connection Confirmed]', args, file=sys.stderr)
      print('-----------------------------', file=sys.stderr)


@app.route('/')
def hello_world():
  print('hit home route', file=sys.stderr)
  return 'home'

# @app.route('/test')
# def test():
#   print('hit test route', file=sys.stderr)
#   socketIO.emit('test', 'testing')
#   return 'test'

if __name__ == '__main__':
  # for i in range(0, 2):
  socketIO = SocketIO('10.1.133.238', 50, Namespace)
  t = threading.Thread(target=socketIO.wait)
  t.daemon = True
  t.start()
  app.run(host='0.0.0.0', port=9000, debug=True)

