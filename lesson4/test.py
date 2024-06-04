from flask import Flask, request

app = Flask(__name__)

@app.route('/')
def index():
	return 'Home'


@app.route('/hello')
def hello():
	return 'Hello'

app.run(port=5001, debug=True) 