from __future__ import print_function # In python 2.7
import json
import sys
from flask import Flask, request, render_template, send_from_directory, session, jsonify
from socketIO_client import SocketIO, BaseNamespace, LoggingNamespace

import threading

import logging
logging.getLogger('socketIO-client').setLevel(logging.DEBUG)
logging.basicConfig()

app = Flask(__name__)

class Namespace(BaseNamespace):
    def on_connect(self):
      print('[Connected]', file=sys.stderr)
    def on_test(self, *args):
      print('test', file=sys.stderr)
    def on_new_user_response(self, *args):
      print('new user', file=sys.stderr)

def on_connect():
  print('-----------------------------')
  print('connected!!!', file=sys.stderr)
  print('-----------------------------')

def on_new_user_response():
  print('-----------------------------')
  print('new user', file=sys.stderr)
  print('-----------------------------')
  socketIO.emit('connection name', { 'name': 'recieved new user event' })

def on_test():
  print('-----------------------------')
  print('test', file=sys.stderr)
  print('-----------------------------')
  
@app.route('/')
def hello_world():
  print('hit home route', file=sys.stderr)
  socketIO.emit('connection name', { 'name': 'HELLO WORLD ROUTE' })
  return 'home'

@app.route('/test')
def test():
  print('hit test route', file=sys.stderr)
  socketIO.emit('test', 'testing')
  return 'test'

if __name__ == '__main__':
  socketIO = SocketIO('10.1.133.238', 50, Namespace)
  socketIO.on('new_user', on_new_user_response)
  socketIO.on('connection name', on_new_user_response)
  socketIO.on('test', on_test)
  t = threading.Thread(target=socketIO.wait)
  t.daemon = True
  t.start()
  app.run(host='0.0.0.0', port=9000, debug=True)

