## lesson4/airesumeAPI.py
nohup를 이용해 EC2 백그라운드에서 24시간 실행되고 있는 API 코드.
1. EC2 컴퓨터 내에 5001번 포트로 요청이 들어오면
2. openAI assistant API를 이용해 openai thread 를 생성하고
3. 질문을 입력하여 답변을 받아온다.
4. 답변을 다시 HTTP response body 에 담아 리턴한다.
