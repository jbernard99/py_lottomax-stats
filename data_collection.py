"""Utilities for scraping LottoMax results from lottomaxnumbers.com."""

import result
import requests
from bs4 import BeautifulSoup
from datetime import datetime
from os import system

BASE_URL = "https://www.lottomaxnumbers.com"


def clear():
    """Clear the terminal screen."""
    system("clear")


	
def get_soup(url: str) -> BeautifulSoup:
    """Return BeautifulSoup object for the given URL."""
    page = requests.get(url)
    return BeautifulSoup(page.content, "html.parser")

def get_result_from_balls(balls):
    """Return a list of integers from a <ul class="balls"> element."""
    result_list = []
    for ball in balls.find_all("li"):
        result_list.append(int(ball.text.strip()))
    return result_list


def get_extra(draw_soup: BeautifulSoup) -> str:
    """Return the Ontario Encore number as a string if available."""
    encore_img = draw_soup.find("img", {"src": "/images/logos/lottery-logos/ontario_encore.svg"})
    if encore_img and encore_img.parent:
        digits = [li.get_text(strip=True) for li in encore_img.parent.parent.select("ul li")]
        return "".join(digits)
    return ""


def get_max_millions(draw_soup: BeautifulSoup) -> list:
    """Return a list of Max Millions combinations if present."""
    results = []
    wrapper = draw_soup.find("div", class_="maxMillionsResultsWrap")
    if wrapper:
        for ul in wrapper.select("div.maxMillionResults ul.balls"):
            results.append([int(li.get_text(strip=True)) for li in ul.select("li")])
    return results

def scan(start_year: int = 2025, end_year: int = 2009):
    """Scan yearly result pages and store draw information in the database."""
    clear()
    for year in range(start_year, end_year - 1, -1):
        year_url = f"{BASE_URL}/numbers/{year}"
        soup = get_soup(year_url)
        for row in soup.select("table.archiveResults tbody tr"):
            cells = row.find_all("td")
            if len(cells) != 3:
                continue

            link = cells[0].find("a")
            if not link:
                continue

            date_obj = datetime.strptime(link.text.strip(), "%B %d %Y")
            saved_date = date_obj.strftime("%Y-%m-%d")

            numbers = [int(li.get_text(strip=True)) for li in cells[1].select("li")]
            bonus = numbers.pop()
            jackpot = cells[2].get_text(strip=True)

            draw_soup = get_soup(BASE_URL + link["href"])
            extra = get_extra(draw_soup)
            max_combos = get_max_millions(draw_soup)

            res = result.Result(saved_date)
            res.set_winning_combo(numbers)
            res.set_bonus(bonus)
            res.set_extra(extra)
            res.set_prize(jackpot)
            if max_combos:
                res.set_maxi_combos(max_combos)
            res.save_result_to_db()

