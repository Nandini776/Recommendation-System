from flask import Flask, render_template, request
import pickle
import numpy as np
import pandas as pd


popular_df = pickle.load(open("popular.pkl", "rb"))
pt = pickle.load(open("pt.pkl", "rb"))
books = pickle.load(open("books.pkl", "rb"))
similarity_score = pickle.load(open("similarity_score.pkl", "rb"))

app = Flask(__name__)

def get_high_quality_cover(title):
    try:
        url = f"https://openlibrary.org/search.json?title={title}"
        res = requests.get(url, timeout=5).json()
        if res.get("docs"):
            cover_id = res["docs"][0].get("cover_i")
            if cover_id:
                return f"https://covers.openlibrary.org/b/id/{cover_id}-L.jpg"
    except Exception:
        pass
    return None

@app.route('/')
def index():
    high_quality_images = []
    for title, img_url in zip(popular_df['Book-Title'], popular_df['Image-URL-M']):
        cover_url = get_high_quality_cover(title)
        high_quality_images.append(cover_url if cover_url else img_url)
    return render_template(
        'index.html',
        book_name=list(popular_df['Book-Title'].values),
        author=list(popular_df['Book-Author'].values),
        image=high_quality_images,
        votes=list(popular_df['num_ratings'].values),
        rating=list(popular_df['avg_rating'].values)
    )

@app.route("/recommend")
def recommend_ui():
    return render_template("recommend.html", book_name=list(pt.index))

@app.route('/get_book_suggestions')
def get_book_suggestions():
    query = request.args.get('q', '').lower()
    matches = [book for book in pt.index if query in book.lower()]
    return {'books': matches[:10]}

@app.route('/recommend_books', methods=['POST'])
def recommend():
    user_input = request.form.get('user_input')
    matches = [book for book in pt.index if user_input.lower() in book.lower()]
    if not matches:
        return render_template('recommend.html', data=None, error="Book not found")
    user_input = matches[0]
    index = np.where(pt.index == user_input)[0][0]
    similar_items = sorted(list(enumerate(similarity_score[index])), key=lambda x: x[1], reverse=True)[1:5]
    data = []
    for i in similar_items:
        item = []
        temp_df = books[books['Book-Title'] == pt.index[i[0]]]
        title = list(temp_df.drop_duplicates('Book-Title')['Book-Title'].values)[0]
        author = list(temp_df.drop_duplicates('Book-Title')['Book-Author'].values)[0]
        cover_url = get_high_quality_cover(title)
        if not cover_url:
            cover_url = list(temp_df.drop_duplicates('Book-Title')['Image-URL-M'].values)[0]
        item.extend([title, author, cover_url])
        data.append(item)
    return render_template('recommend.html', data=data)

if _name_ == '_main_':
    app.run(debug=True)















































