from flask import Flask

app = Flask(__name__)
@app.route('/')
def home():
    return 'Hello, World'

@app.route('/')
def hello(name):
    return 'Hello, ' + name + ', How are you'

@app.route('/about')
def about():
    return 'About'

if __name__ == "__name__":
    app.run()