from flask import Flask
app = Flask(__name__)

@app.route('/')
def home():
    return 'Hello, Paper Bag Software!'

@app.route('/healthz')
def healthz():
    return 'OK', 200