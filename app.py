from flask import Flask, jsonify
import os
import requests
from flask_cors import CORS, cross_origin
app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

@app.route('/')
def homepage():
    return ';)'


@app.route('/cb/<code>')
@cross_origin()
def githubCallback(code):
    client_secret = os.environ.get('client_secret')
    return client_secret

if __name__ == '__main__':
    app.run(debug=True, use_reloader=True)