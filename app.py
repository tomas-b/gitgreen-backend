from flask import Flask
app = Flask(__name__)

@app.route('/')
def homepage():
    return """
    <h1>sup heroku</h1>
    """

if __name__ == '__main__':
    app.run(debug=True, use_reloader=True)