import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

client = OpenAI(
	api_key = os.environ.get("OPENAI_API_KEY"),
)
response = client.completions.create(
	model="gpt-3.5-turbo-instruct",
	prompt="농구 좋아해? \n\nQ: nba 보니?\nA:",
	temperature=0,
	max_tokens=100,
	top_p=1,
	frequency_penalty=0.0,
	presence_penalty=0.0,
	stop=["\n"]
)
print(response)
print()
print(response.choices[0].text.strip())


