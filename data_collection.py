import result
import requests
from bs4 import BeautifulSoup
from datetime import datetime, timedelta
from os import system

date = datetime(2009, 9, 25)
end_date = datetime(2021, 6, 25)
is_tuesday = False

def clear():
		system("clear")

def skip_days():
	global date
	global is_tuesday
	if is_tuesday:
		date = date + timedelta(days = 3)
	else:
		date = date + timedelta(days = 4)
	is_tuesday = not is_tuesday
	
def get_soup(date):
	url = "https://www.lottomaxnumbers.com/numbers/lotto-max-result-"
	page = requests.get(url + date.strftime("%m-%d-%Y"))
	soup = BeautifulSoup(page.content, 'html.parser')
	if "404 Error" in str(soup.find().title):
		return False
	else:
		return soup

def get_result_from_balls(balls):
	result = []
	for ball in balls.find_all("li"):
		result.append(int(ball.text.strip()))
	return result

def scan():
	clear()
	while date <= end_date:
			soup = get_soup(date)
			saved_date = date.strftime("%Y-%m-%d")
			skip_days()
			if soup == False:
				continue
			else:
				result_object = result.Result(saved_date)

				big_div = soup.find(class_ = "results")
				div = big_div.find(class_ = "balls")
				ball_result = get_result_from_balls(div)
				result_object.set_bonus(ball_result.pop())
				result_object.set_winning_combo(ball_result)

				div = big_div.find(class_="encore-title")
				result_object.set_extra(div.span.text)

				div = soup.find(class_="breakdown-table")
				rows = div.find_all("tr")
				row = rows[1].find_all("td")
				prize = row[1].text
				result_object.set_prize(prize.strip())

				div = soup.find(id="this-draw-max-results")
				if div != None:
					all_max = []
					for item in div.find_all(class_="max-millions-result"):
						one_max = get_result_from_balls(item.find(class_="balls"))
						all_max.append(one_max)
					result_object.set_maxi_combos(all_max)
				result_object.save_result_to_db()
