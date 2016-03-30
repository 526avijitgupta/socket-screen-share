from flask import Flask,request
from flask.ext.cors import CORS, cross_origin
import socket

app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

HOST = ''
PORT = 4500
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((HOST,PORT))

@app.route('/file', methods=['GET'])
@cross_origin()
def send_file():
    print request.args.get('postfile')
    f = open(request.args.get('postfile'), 'r+')
    l = f.read(1024)
    s.send('filestart')
    s.send(request.args.get('postfile'))
    while (l):
        s.send(l)
        l = f.read(1024)
    f.close()
    s.send('fileend')
    s.close()
    return request.url


if __name__ == '__main__':
    app.debug = True
    app.run()
