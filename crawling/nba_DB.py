import requests
from bs4 import BeautifulSoup
import pymysql

conn = pymysql.connect(
	host="HOST_IP",
	user='root',
	password="AWS_PASSWORD",
	db='NBA',
	charset='utf8'
)

cur = conn.cursor()
cur.execute("DROP TABLE IF EXISTS teams")
cur.execute("CREATE TABLE teams(team_rank INT NOT NULL AUTO_INCREMENT,team_name VARCHAR(64),winning_odds DEC(10,3),PRIMARY KEY (team_rank))")


url = "https://sports.news.naver.com/basketball/record/index?category=nba"
r = requests.get(url)
soup = BeautifulSoup(r.text, "html.parser")

lankings = soup.select("td>div>span[id]")
winningOdds = soup.select("td>strong")

for i in range(15):
	cur.execute(f"INSERT INTO teams VALUES({i+1},\"{lankings[i].text}\",\"{winningOdds[i].text}\")")

conn.commit()
conn.close()