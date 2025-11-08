from flask import Flask, render_template, request
import csv

app = Flask(__name__)

def load_movies():
    movies = []
    with open('movies.csv', encoding='utf-8-sig') as f:  # nota: utf-8-sig limpia el BOM
        reader = csv.DictReader(f)
        for row in reader:
            movies.append({
                'title': row.get('title', '').strip(),
                'genre': row.get('genre', '').strip(),
                'year': row.get('year', '').strip(),
                'rating': float(row.get('rating', 0))
            })
    return movies

@app.route('/')
def search_view():
    return render_template('search.html')

@app.route('/buscar')
def results_view():
    query = request.args.get('q', '').lower()
    genre = request.args.get('genre', '')
    year = request.args.get('year', '')
    rating = request.args.get('rating', '')

    movies = load_movies()
    filtered = movies

    if query:
        filtered = [m for m in filtered if query in m['title'].lower()]
    if genre:
        filtered = [m for m in filtered if m['genre'].lower() == genre.lower()]
    if year:
        filtered = [m for m in filtered if m['year'] == year]
    if rating:
        filtered = [m for m in filtered if m['rating'] >= float(rating)]

    if not filtered:
        return render_template('no_results.html', query=query, genre=genre, year=year, rating=rating)
    return render_template('results.html', movies=filtered, query=query, genre=genre, year=year, rating=rating)

if __name__ == '__main__':
    app.run(debug=True)
