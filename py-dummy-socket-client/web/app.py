from __future__ import print_function # In python 2.7
import json
import sys
from flask import Flask, request, render_template, send_from_directory, session, jsonify
from socketIO_client import SocketIO, BaseNamespace

import logging
logging.getLogger('socketIO-client').setLevel(logging.DEBUG)
logging.basicConfig()

app = Flask(__name__)

class Namespace(BaseNamespace):

    def on_connect(self):
        print('[Connected]')

@app.route('/')
def hello_world():
  socketIO = SocketIO('10.1.133.238', 50, Namespace)
  socketIO.emit('connection name', { 'name': 'HELLO WORLD ROUTE' })
  return render_template('index.html')


if __name__ == '__main__':
  app.run(host='0.0.0.0', port=9000, debug=True)