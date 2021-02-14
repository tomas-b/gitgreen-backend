from flask import Flask
import requests
app = Flask(__name__)

@app.route('/')
def homepage():
    return """
    <h1>sup heroku</h1>
    """

@app.route('/user/<username>')
def userpage(username):
    html = requests.get('https://github.com/%s' % username)
    calendar = html.text.split('class="js-calendar-graph-svg">')[1].split('</svg')[0]
    return """
        the user is {user}.
        <hr>
        {html}
        """.format(user=username, html=calendar)


if __name__ == '__main__':
    app.run(debug=True, use_reloader=True)