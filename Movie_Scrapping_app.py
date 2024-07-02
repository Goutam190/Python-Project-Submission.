import pandas as pd
import requests
import csv

from pathlib import Path
from bs4 import BeautifulSoup


genres = ['action', 'adventure', 'animation', 'comedy', 'crime', 'documentary', 'drama', 'family', 'fantasy',
          'history', 'horror', 'music', 'mystery', 'romance', 'thriller', 'tv-movie', 'science-fiction', 'war', 'western']

csv_file = Path('movies_data.csv')

if not csv_file.exists():
    movies = []
    for genre in genres:
        url = f"https://www.moviefone.com/movies/genres/{genre}/"

        try:
            response = requests.get(url)
            response.raise_for_status()
            soup = BeautifulSoup(response.text, 'html.parser')

            for movie in soup.find_all('div', class_="hub-movie"):
                title = movie.find('a', class_='hub-movie-title').text.strip()

                movie_data = {'Title': title, 'Genre': genre}
                movies.append(movie_data)

        except requests.exceptions.RequestException as e:
            print(f"Error scraping data for genre '{genre}': {e}")

    print("Scraped all movies data.")

    fields = ['Title', 'Genre']

    with open(csv_file, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.DictWriter(file, fieldnames=fields)

        writer.writeheader()
        writer.writerows(movies)

    print(f"Movies data saved to {csv_file}")


def suggest_movies(genre, csv_file):
    try:
        df = pd.read_csv(csv_file)
        genre_movies = df[df['Genre'] == genre]

        if len(genre_movies) == 0:
            return f"No movies found for genre '{genre}'."

        return genre_movies['Title'].tolist()

    except Exception as e:
        return print(e)


while True:
    genre_input = input(
        "Enter a genre to get movie suggestions (or 'exit' to quit): ").lower()
    print()

    if genre_input == 'exit':
        break

    suggestions = suggest_movies(genre_input, csv_file)
    if type(suggestions) is list:
        for movie in suggestions:
            print(movie)
        print()
    else:
        print(suggestions)
