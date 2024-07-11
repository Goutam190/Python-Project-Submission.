import pandas as pd
import requests
import csv
import random

from pathlib import Path
from bs4 import BeautifulSoup

while True:
    genre_input = input("Enter a genre to fetch the Movie: ").lower()
    print()

    csv_file = Path(f'movies_{genre_input}.csv')

    movies = []
    url = f"https://www.moviefone.com/movies/genres/{genre_input}/"
     
    try:
        response = requests.get(url)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')

        for movie in soup.find_all('div', class_="hub-movie"):
            title = movie.find('a', class_='hub-movie-title').text.strip()

            movie_data = {'Title': title, 'Genre': genre_input}
            movies.append(movie_data)

    except requests.exceptions.RequestException as e:
        print(f"Error scraping data for genre '{genre_input}': {e}")

    fields = ['Title', 'Genre']

    # CSV file using csv module
    with open(csv_file, 'w', newline='', encoding='utf-8') as file:
        writer = csv.DictWriter(file, fieldnames= fields)
        writer.writeheader()
        writer.writerows(movies)

    # read from CSV file using pandas
    df = pd.read_csv(csv_file)

    random_movie = df.sample(n=1).iloc[0]

    print(f"Movie suggestion: {random_movie['Title']}")

    exit()
