from __future__ import print_function # In python 2.7
import json
import random
import sys
from flask import Flask, request, render_template, send_from_directory, session, jsonify
from socketIO_client import SocketIO, BaseNamespace, LoggingNamespace
from utils import bcolors
import threading

import logging
logging.getLogger('socketIO-client').setLevel(logging.DEBUG)
logging.basicConfig()

app = Flask(__name__)

def disconnectHandler(path):
  print(bcolors.RED + '-----------------------------'  + bcolors.ENDC, file=sys.stderr)
  print(bcolors.RED + 'Name Space:', path, 'Socket was disconnected', file=sys.stderr)
  print(bcolors.RED + '-----------------------------' + bcolors.ENDC, file=sys.stderr)

def connectHandler(path):
  print(bcolors.PURPLE + '-----------------------------' + bcolors.ENDC, file=sys.stderr)
  print(bcolors.PURPLE + 'Name Space:', path, '[Connected]' + bcolors.ENDC, file=sys.stderr)
  print(bcolors.PURPLE + '-----------------------------' + bcolors.ENDC, file=sys.stderr)

def closeHandler(path):
  print(bcolors.RED + '-----------------------------', file=sys.stderr)
  print(bcolors.RED + 'Name Space:', path, 'CLOSED', file=sys.stderr)
  print(bcolors.RED + '-----------------------------' + bcolors.ENDC, file=sys.stderr)

def generalEvent(path, eventName):
  print(bcolors.PURPLE + '-----------------------------' + bcolors.ENDC, file=sys.stderr)
  print(bcolors.PURPLE + 'Name Space:', path, eventName + bcolors.ENDC, file=sys.stderr)
  print(bcolors.PURPLE + '-----------------------------' + bcolors.ENDC, file=sys.stderr)

class Namespace(BaseNamespace):
  def on_connect(self):
    connectHandler(self.path)
    self.emit('new_connection', { 'name': self.path, 'port': port})
  def on_disconnect(self):
    disconnectHandler(self.path)
  def on_close(self):
    closeHandler(self.path)
  def on_ping(self):
    generalEvent(self.path, 'Ping')
    self.emit('pong', { 'name': self.path, 'port': port} )
  def on_pong(self):
    generalEvent(self.path, 'Pong')
  def on_unique_event_response(self, *args):
    print(port, bcolors.BLUE + '-----------------------------' + bcolors.ENDC, file=sys.stderr)
    print(port, bcolors.BLUE + 'Name Space:', self.path, 'UNIQUE EVENT' + bcolors.ENDC, args, file=sys.stderr)
    print(port, bcolors.BLUE + '-----------------------------' + bcolors.ENDC, file=sys.stderr)
  def on_new_connection_recieved(self, *args):
    print(port, bcolors.GREEN + '-----------------------------' + bcolors.ENDC, file=sys.stderr)
    print(port, bcolors.GREEN + 'Name Space:', self.path, '[A new socket was opened]' + bcolors.ENDC, args, file=sys.stderr)
    print(port, bcolors.GREEN + '-----------------------------' + bcolors.ENDC, file=sys.stderr)
    # self.emit('unique_event', { 'name': self.path })

class DefaultNamespace(BaseNamespace):
  def on_connect(self):
    connectHandler(self.path)
  def on_close(self):
    closeHandler(self.path)
  def on_ping(self):
    generalEvent(self.path, 'Ping')
  def on_pong(self):
    generalEvent(self.path, 'Pong')
  def on_disconnect(self):
    disconnectHandler(self.path)


@app.route('/')
def hello_world():
  return 'home'

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
