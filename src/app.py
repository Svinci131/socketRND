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

class bcolors:
  PURPLE = '\033[95m'
  BLUE = '\033[94m'
  GREEN = '\033[92m'

class Namespace(BaseNamespace):
  def on_connect(self):
    print(bcolors.PURPLE + '-----------------------------', file=sys.stderr)
    print(bcolors.PURPLE + 'Name Space:', self.path, '[Connected]', file=sys.stderr)
    print(bcolors.PURPLE + '-----------------------------', file=sys.stderr)
    self.emit('new_connection', { 'name': self.path })
  def on_unique_event_response(self, *args):
    print(bcolors.BLUE + '-----------------------------', file=sys.stderr)
    print(bcolors.BLUE + 'Name Space:', self.path, 'UNIQUE EVENT', args, file=sys.stderr)
    print(bcolors.BLUE + '-----------------------------', file=sys.stderr)
  def on_new_connection_recieved(self, *args):
    print(bcolors.GREEN + '-----------------------------', file=sys.stderr)
    print(bcolors.GREEN + 'Name Space:', self.path, '[A new socket was opened]', args, file=sys.stderr)
    print(bcolors.GREEN + '-----------------------------', file=sys.stderr)
    self.emit('unique_event', { 'name': self.path })

class DefaultNamespace(BaseNamespace):
  def on_connect(self):
    print(bcolors.PURPLE + '-----------------------------', file=sys.stderr)
    print(bcolors.PURPLE + 'Name Space:', self.path, '[Connected]', file=sys.stderr)
    print(bcolors.PURPLE + '-----------------------------', file=sys.stderr)
    self.emit('new_connection', { 'name': self.path })
  def on_new_connection_recieved(self, *args):
    print(bcolors.GREEN + '-----------------------------', file=sys.stderr)
    print(bcolors.GREEN + 'Name Space:', self.path, '[A new socket was opened]', args, file=sys.stderr)
    print(bcolors.GREEN + '-----------------------------', file=sys.stderr)


@app.route('/')
def hello_world():
  print('hit home route', file=sys.stderr)
  return 'home'

def createSocketConnection(name):
  if (name == None):
    socketIO = SocketIO('10.1.133.238', 140, DefaultNamespace)
  else:
    socketIO = SocketIO('10.1.133.238', 140)
    namespace = socketIO.define(Namespace, name)

  t = threading.Thread(target=socketIO.wait)
  t.daemon = True
  t.start()

if __name__ == '__main__':
  
  createSocketConnection(None)

  for i in range(0, 3):
    name = '/robot'+str(i)
    createSocketConnection(name)

  app.run(host='0.0.0.0', port=9000, debug=True)

