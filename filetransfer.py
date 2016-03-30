from flask import Flask,request
from flask.ext.cors import CORS, cross_origin

app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

@app.route('/file', methods=['GET'])
@cross_origin()
def send_file():
    print request.args.get('postfile')
    return request.url


if __name__ == '__main__':
    app.debug = True
    app.run()
