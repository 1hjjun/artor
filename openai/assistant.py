from openai import OpenAI
from dotenv import load_dotenv
import os
import json
import time


def display(obj):
    print(json.dumps(obj, indent=4))
    
def show_json(obj):
	display(json.loads(obj.model_dump_json()))

load_dotenv()


client = OpenAI(
	api_key = os.environ.get("OPENAI_API_KEY"),
)

file_ids=[
    "file-9DdWlanIt6JwTEuUTP3mHQGs",
]


assistant = client.beta.assistants.update(
    os.environ.get("ASSISTANT_ID"),
    tools=[
      {"type": "code_interpreter"},
      {"type": "file_search"},
		],
    instructions="You are a chatbot that provides information about Jun's resume.",
)

def create_new_thread():
    # 새로운 스레드를 생성합니다.
    thread = client.beta.threads.create()
    return thread



def wait_on_run(run, thread):
    # 주어진 실행(run)이 완료될 때까지 대기합니다.
    # status 가 "queued" 또는 "in_progress" 인 경우에는 계속 polling 하며 대기합니다.
    while run.status == "queued" or run.status == "in_progress":
        # run.status 를 업데이트합니다.
        run = client.beta.threads.runs.retrieve(
            thread_id=os.environ.get("THREAD_ID"),
            run_id=run.id,
        )
        # API 요청 사이에 잠깐의 대기 시간을 두어 서버 부하를 줄입니다.
        time.sleep(0.5)
    return run

def submit_message(assistant_id, thread_id, user_message):
    # 3-1. 스레드에 종속된 메시지를 '추가' 합니다.
    client.beta.threads.messages.create(
        thread_id=os.environ.get("THREAD_ID"), role="user", content=user_message
    )
    # 3-2. 스레드를 실행합니다.
    run = client.beta.threads.runs.create(
        thread_id=thread_id,
        assistant_id=assistant_id,
    )
    return run

def get_response(thread_id):
    # 3-4. 스레드에 종속된 메시지를 '조회' 합니다.
    return client.beta.threads.messages.list(thread_id=thread_id, order="asc")

def print_message(response):
    for res in response:
        print(f"[{res.role.upper()}]\n{res.content[0].text.value}\n")

def ask(assistant_id, thread_id, user_message):
    run = submit_message(
        assistant_id,
        thread_id,
        user_message,
    )
    # 실행이 완료될 때까지 대기합니다.
    run = wait_on_run(run, thread_id)
    print_message(get_response(thread_id).data[-2:])
    return run

def upload_files(files):
    uploaded_files = []
    for filepath in files:
        file = client.files.create(
            file=open(
                # 업로드할 파일의 경로를 지정합니다.
                filepath,  # 파일경로. (예시) data/sample.pdf
                "rb",
            ),
            purpose="assistants",
        )
        uploaded_files.append(file)
        print(f"[업로드한 파일 ID]\n{file.id}")
    return uploaded_files

run = ask(
    os.environ.get("ASSISTANT_ID"),
    os.environ.get("THREAD_ID"),
    "한형준의 나이를 파일에서 검색하여 알려주세요. ",
)