from flask import Flask
import requests
app = Flask(__name__)

@app.route('/')
def homepage():
    return """
    <h1>sup heroku</h1>
    """

@app.route('/user/<username>')
def homepage(username):
    r = requests.get('https://github.com/tomas-b')
    return """
        the user is {user}.
        <hr>
        {html}
        """.format(user=username, html=r.text)

if __name__ == '__main__':
    app.run(debug=True, use_reloader=True)