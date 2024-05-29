import sys
import requests
import csv
import time
from bs4 import BeautifulSoup
import re

douban_id = ''
watched_csv = 'douban_watched.csv'
wish_csv = 'douban_wish.csv'

# Headers
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
}

# Pagination
start = 0

# Urls

with open(watched_csv, 'a') as watched_file:
    writer = csv.writer(watched_file, delimiter=',')
    writer.writerow(["Title", "Release Year", "Rating", "Date"])
    while True:
        watched_url = f'https://movie.douban.com/people/{douban_id}/collect?start={start}&sort=time&rating=all&mode=grid&filter=all&type=movie'
        wish_url = f'https://movie.douban.com/people/{douban_id}/wish?start={start}&sort=time&rating=all&mode=grid&type=all&filter=all&type=movie'
        
        res = requests.get(watched_url, headers=headers)

        soup = BeautifulSoup(res.text, 'html.parser')

        movies = soup.find_all('div', class_='comment-item')
        if not movies:
            break

        for movie in movies:
            title = movie.find('li', class_='title').find('em').get_text().split('/')[0].strip()
            release_year = movie.find('li', class_='intro').get_text().split('(')[0][0:4]
            rating_element = movie.find('span', {'class' : re.compile('^rating.*')})
            rating = rating_element.attrs['class'][0][6:7] if rating_element else ''
            date = movie.find('span', class_='date').get_text()

            print(f'Movie: {title}, {release_year}, {rating}, {date}')

            # Write to csv
            writer.writerow([title,release_year,rating,date])

        # Update vars
        start += 15
        # Sleep to prevent IP ban
        time.sleep(20)

print('Douban watched list exported.')