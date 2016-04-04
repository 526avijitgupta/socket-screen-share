from flask import Flask,request,render_template
from flask.ext.cors import CORS, cross_origin
import socket

app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

HOST = ''
PORT = 4502
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((HOST,PORT))

@app.route('/')
def index():
    return render_template('index_1.html')

@app.after_request
def after_request(resp):
    resp.headers['Access-Control-Allow-Origin'] = request.headers.get('Origin','*')
    resp.headers['Access-Control-Allow-Credentials'] = 'true'
    resp.headers['Access-Control-Allow-Methods'] = 'POST, OPTIONS, GET'
    resp.headers['Access-Control-Allow-Headers'] = request.headers.get( 
        'Access-Control-Request-Headers', 'Authorization' )
    # set low for debugging
    if app.debug:
        resp.headers['Access-Control-Max-Age'] = '1'
    return resp

@app.route('/file', methods=['GET'])
@cross_origin()
def send_file():
    print request.args.get('postfile')
    f = open(request.args.get('postfile'), 'w')
    f.close()
    f = open(request.args.get('postfile'),'r')
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
