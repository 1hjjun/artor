from flask import Flask, request, jsonify
from openai import OpenAI
from dotenv import load_dotenv
from pymongo import MongoClient
from flask_cors import CORS
import os
import time
from datetime import datetime
from flask_caching import Cache

load_dotenv()

app = Flask(__name__)
app.config['CACHE_TYPE'] = 'SimpleCache'  # 사용할 캐시 타입
app.config['CACHE_DEFAULT_TIMEOUT'] = 60 * 60
cache = Cache(app)

TIME_WINDOW = 60 * 60
MAX_REQUESTS = 5

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
	client_ip = get_ip()
	timestamp = datetime.now()
	current_time = time.time()
    
	# IP에 대한 요청 기록을 캐시에서 가져옴
	request_log = cache.get(client_ip) or []

	# 타임 윈도우 내의 요청만 유지
	request_log = [log for log in request_log if current_time - log < TIME_WINDOW]

	# 요청 횟수 검사
	if len(request_log) >= MAX_REQUESTS:
		last_request_time = max(request_log)
		next_available_time = last_request_time + TIME_WINDOW
		next_available_datetime = datetime.fromtimestamp(next_available_time)
		formatted_next_available_time = next_available_datetime.strftime('%Y-%m-%d %H:%M:%S')
		
		return jsonify({"response": f"1시간에 5번만 질문할 수 있습니다. {formatted_next_available_time}에 다시 질문할 수 있습니다."}), 429
	
	# 요청 기록 갱신
	request_log.append(current_time)
	cache.set(client_ip, request_log, timeout=TIME_WINDOW)

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

		

		log = {
			"ip_address": client_ip,
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