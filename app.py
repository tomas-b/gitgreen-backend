from flask import Flask, jsonify
import requests
from flask_cors import CORS, cross_origin
app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

@app.route('/')
def homepage():
    return """
    <h1>sup heroku</h1>
    """

# https://stackoverflow.com/questions/46490348/split-a-list-with-nn-elements-into-n-lists-with-n-elements-in-every-list
# def chunkify(items, chunk_len):
#     return [items[i:i+chunk_len] for i in range(0,len(items),chunk_len)]

@app.route('/user/<username>')
@cross_origin()
def userpage(username):

    html = requests.get('https://github.com/%s' % username)
    calendar = html.text.split('class="js-calendar-graph-svg">')[1].split('</svg')[0]
    dates = []
    
    for box in calendar.split('data-count="')[1:]:
        dates.append( {
            'count': box.split('"')[0],
            'date':  box.split('data-date="')[1].split('"')[0],
            'level': box.split('data-level="')[1].split('"')[0]
            } )

    return jsonify(dates)
    # return jsonify(chunkify(dates, 7))

if __name__ == '__main__':
    app.run(debug=True, use_reloader=True)