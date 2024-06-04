from bs4 import BeautifulSoup
import requests

base_url = "https://search.naver.com/search.naver?where=nexearch&sm=top_hty&fbm=0&ie=utf8&query="

keyword = input("검색어를 입력하세요 :")

search_url = base_url + keyword

r = requests.get(search_url)

soup = BeautifulSoup(r.text, "html.parser")

items = soup.select(".news_tit")

for e, item in enumerate(items, 1):
	print(f"{e} : {item.text}")