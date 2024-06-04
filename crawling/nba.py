import requests
from bs4 import BeautifulSoup


url = "https://sports.news.naver.com/basketball/record/index?category=nba"
r = requests.get(url)

soup = BeautifulSoup(r.text, "html.parser")

lankings = soup.select("td>div>span[id]")
winningOdds = soup.select("td>strong")
print(lankings)
for i in range(15):
	print(f"{i+1} : {lankings[i].text}\t승률: {winningOdds[i].text}")