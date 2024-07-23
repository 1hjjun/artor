from flask import Flask, request, jsonify
from openai import OpenAI
from dotenv import load_dotenv
from pymongo import MongoClient
from flask_cors import CORS
import os
import time
from datetime import datetime

load_dotenv()

app = Flask(__name__)
CORS(app)

client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

mongo_password = os.environ.get("MONGO_PASSWORD")
mongo_connection_string = f'mongodb+srv://aut7410:{mongo_password}@resumecluster.j7ejmtd.mongodb.net/?retryWrites=true&w=majority&appName=resumeCluster'

mongoclient = MongoClient(mongo_connection_string)
db = mongoclient.log

def get_ip():
	if request.headers.get('X-Forwarded-For'):
		ip = request.headers.get('X-Forwarded-For').split(',')[0]
	else:
		ip = request.remote_addr
	return ip

@app.route('/createNewThread', methods=['POST'])
def createNewThread():
	try: 
		createdThread = client.beta.threads.create()
		createdThread_id = createdThread.id

		return jsonify({"thread_id" : createdThread_id})
	
	except Exception as e:
		return jsonify({"error" : str(e)})


@app.route('/sendMessage', methods=['POST'])
def sendMessage():
	data = request.get_json()
	user_input = data.get('question')
	user_thread_id = data.get('thread_id')

	try:
		assistant_id=os.environ.get("ASSISTANT_ID")
		thread_id=user_thread_id
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

		ip = get_ip()
		timestamp = datetime.now()

		log = {
			"ip_address": ip,
			"user_message": user_input,
			"response": ai_response,
			"timestamp": timestamp
		}
		db.users.insert_one(log)

		return jsonify({"response" : ai_response})
	
	except Exception as e:
		return jsonify({"error" : str(e)})
	

if __name__ == '__main__':
	app.run(port=5001, debug=True) 