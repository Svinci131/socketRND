import sys
import json
from __future__ import print_function
from socketIO_client import SocketIO, BaseNamespace
from flask import Flask, request, render_template, send_from_directory, session, jsonify

app = Flask(__name__)

class Namespace(BaseNamespace):

    def on_connect(self):
        print('[Connected]')

@app.route('/')
def hello_world():
  socketIO = SocketIO('10.1.133.238', 50, Namespace)

  socketIO.emit('connection name', { 'name': 'Sally' })

  return render_template('index.html')

@app.route('/testsubscriber', methods=['POST'])
def recieve():
  print ('hi', request)
  return 'recieved'

@app.route('/scanned', methods=['POST'])
def recieve_scanned():
  data = request.get_json()

  socketio.emit('scanned',
    data, namespace='/test')
  return render_template('index.html')


if __name__ == '__main__':
  app.run(host='0.0.0.0', port=9000, debug=True)