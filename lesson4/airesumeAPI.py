from flask import Flask, request, jsonify
from openai import OpenAI
from dotenv import load_dotenv
from flask_cors import CORS
import os
import time

load_dotenv()

app = Flask(__name__)
CORS(app)

client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))


@app.route('/')
def index():
	return 'Home'


@app.route('/hello')
def hello():
	return 'Hello'

@app.route('/sendMessage', methods=['POST'])
def sendMessage():
	data = request.get_json()
	user_input = data.get('question')

	try:
		assistant_id=os.environ.get("ASSISTANT_ID")
		thread_id=os.environ.get("THREAD_ID")
		message = client.beta.threads.messages.create(
			thread_id,
			role="user",
			content=user_input,
		)
		run = client.beta.threads.runs.create(
			thread_id=thread_id,
			assistant_id=assistant_id,
		)

		run_id = run.id

		while True:
			run = client.beta.threads.runs.retrieve(
				thread_id=thread_id,
				run_id=run_id,
			)
			if run.status == "completed":
				break
			else:
				time.sleep(2)

		thread_messages = client.beta.threads.messages.list(thread_id)
		ai_response = thread_messages.data[0].content[0].text.value

		return jsonify({"response" : ai_response})
	
	except Exception as e:
		return jsonify({"error" : str(e)})
	

if __name__ == '__main__':
	app.run(port=5001, debug=True) 