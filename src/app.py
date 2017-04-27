from __future__ import print_function # In python 2.7
import json
import random
import sys
from flask import Flask, request, render_template, send_from_directory, session, jsonify
from socketIO_client import SocketIO, BaseNamespace, LoggingNamespace
import threading

# import logging
# logging.getLogger('socketIO-client').setLevel(logging.DEBUG)
# logging.basicConfig()

app = Flask(__name__)

class bcolors:
  PURPLE = '\033[95m' 
  BLUE = '\033[94m'
  GREEN = '\033[92m'
  RED = '\033[91m'
  ENDC = '\033[0m'

def disconnect(path):
  print(bcolors.RED + '-----------------------------'  + bcolors.ENDC, file=sys.stderr)
  print(bcolors.RED + 'Name Space:', path, 'Socket was disconnected', file=sys.stderr)
  print(bcolors.RED + '-----------------------------' + bcolors.ENDC, file=sys.stderr)

def connectHandler(path):
  print(bcolors.PURPLE + '-----------------------------' + bcolors.ENDC, file=sys.stderr)
  print(bcolors.PURPLE + 'Name Space:', path, '[Connected]' + bcolors.ENDC, file=sys.stderr)
  print(bcolors.PURPLE + '-----------------------------' + bcolors.ENDC, file=sys.stderr)

class Namespace(BaseNamespace):
  def on_connect(self):
    connectHandler(self.path)
    self.emit('new_connection', { 'name': self.path, 'port': port})
  def on_disconnect(self):
    disconnect(self.path)
  def on_close(self):
    print(port, bcolors.RED + '-----------------------------' + bcolors.ENDC, file=sys.stderr)
    print(port, bcolors.RED + 'Name Space:', self.path, 'CLOSED' + bcolors.ENDC, file=sys.stderr)
    print(port, bcolors.RED + '-----------------------------' + bcolors.ENDC, file=sys.stderr)
  def on_pong(self):
    print(bcolors.PURPLE + '-----------------------------' + bcolors.ENDC, file=sys.stderr)
    print(bcolors.PURPLE + 'Name Space:', self.path, 'PONG' + bcolors.ENDC, file=sys.stderr)
    print(bcolors.PURPLE + '-----------------------------' + bcolors.ENDC, file=sys.stderr)
  def on_unique_event_response(self, *args):
    print(port, bcolors.BLUE + '-----------------------------' + bcolors.ENDC, file=sys.stderr)
    print(port, bcolors.BLUE + 'Name Space:', self.path, 'UNIQUE EVENT' + bcolors.ENDC, args, file=sys.stderr)
    print(port, bcolors.BLUE + '-----------------------------' + bcolors.ENDC, file=sys.stderr)
  # def on_new_connection_recieved(self, *args):
  #   print(port, bcolors.GREEN + '-----------------------------' + bcolors.ENDC, file=sys.stderr)
  #   print(port, bcolors.GREEN + 'Name Space:', self.path, '[A new socket was opened]' + bcolors.ENDC, args, file=sys.stderr)
  #   print(port, bcolors.GREEN + '-----------------------------' + bcolors.ENDC, file=sys.stderr)
    # self.emit('unique_event', { 'name': self.path })

class DefaultNamespace(BaseNamespace):
  def on_connect(self):
    connectHandler(self.path)
    # self.emit('new_connection', { 'name': self.path })
  def on_close(self):
    print(bcolors.RED + '-----------------------------', file=sys.stderr)
    print(bcolors.RED + 'Name Space:', self.path, 'CLOSED', file=sys.stderr)
    print(bcolors.RED + '-----------------------------' + bcolors.ENDC, file=sys.stderr)
  def on_pong(self):
    print(bcolors.PURPLE + '-----------------------------' + bcolors.ENDC, file=sys.stderr)
    print(bcolors.PURPLE + 'Name Space:', self.path, 'PONG' + bcolors.ENDC, file=sys.stderr)
    print(bcolors.PURPLE + '-----------------------------' + bcolors.ENDC, file=sys.stderr)
  def on_disconnect(self):
    disconnect(self.path)
  def on_new_connection_recieved(self, *args):
    print(bcolors.GREEN + '-----------------------------', file=sys.stderr)
    print(bcolors.GREEN + 'Name Space:', self.path, '[A new socket was opened]', args, file=sys.stderr)
    print(bcolors.GREEN + '-----------------------------'+ bcolors.ENDC, file=sys.stderr)


@app.route('/')
def hello_world():
  print('hit home route', file=sys.stderr)
  return 'home'

@app.route('/test')
def test():
  print('hit home route', file=sys.stderr)
  return 'test'

def createSocketConnection(name, port):
  socketIO = SocketIO('10.1.133.238', 140)
  namespace = socketIO.define(Namespace, name)
  t = threading.Thread(name=name, target=socketIO.wait)
  t.daemon = True
  t.start()


if __name__ == '__main__':
  namespace = sys.argv[1:][1]
  port = sys.argv[1:][0]

  createSocketConnection(namespace, port)
  app.run(host='0.0.0.0', port=int(port), debug=True, use_reloader=False)


#- 
