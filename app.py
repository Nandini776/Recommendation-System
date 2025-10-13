from flask import Flask, render_template, request
import pickle
import numpy as np
import pandas as pd
import requests

# -----------------------------
# Load data
# -----------------------------
popular_df = pickle.load(open("popular.pkl", "rb"))
pt = pickle.load(open("pt.pkl", "rb"))
books = pickle.load(open("books.pkl", "rb"))
similarity_score = pickle.load(open("similarity_score.pkl", "rb"))

app = Flask(_name_)

# -----------------------------
# Google Books Cover Helper
# -----------------------------
GOOGLE_BOOKS_API_KEY = "AIzaSyAwI6A05ZJvHRILm0UbqATst_I_q0iCO6c"  # 🔹 Replace with your real key


def get_google_books_cover(title):
    """Fetch a high-resolution cover image using Google Books API."""
    try:
        url = f"https://www.googleapis.com/books/v1/volumes?q=intitle:{title}&key={GOOGLE_BOOKS_API_KEY}"
        res = requests.get(url, timeout=5).json()
        if "items" in res and len(res["items"]) > 0:
            image_links = res["items"][0]["volumeInfo"].get("imageLinks", {})
            # Prefer large, then medium, then thumbnail
            for size in ["large", "medium", "small", "thumbnail"]:
                if size in image_links:
                    return image_links[size].replace("http:", "https:")
    except Exception:
        pass
    return None


# -----------------------------
# Routes
# -----------------------------
@app.route('/')
def index():
    high_quality_images = []
    for title, img_url in zip(popular_df['Book-Title'], popular_df['Image-URL-M']):
        cover_url = get_google_books_cover(title)
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
    similar_items = sorted(list(enumerate(similarity_score[index])),
                           key=lambda x: x[1], reverse=True)[1:5]

    data = []
    for i in similar_items:
        item = []
        temp_df = books[books['Book-Title'] == pt.index[i[0]]]

        title = list(temp_df.drop_duplicates('Book-Title')['Book-Title'].values)[0]
        author = list(temp_df.drop_duplicates('Book-Title')['Book-Author'].values)[0]

        cover_url = get_google_books_cover(title)
        if not cover_url:
            cover_url = list(temp_df.drop_duplicates('Book-Title')['Image-URL-M'].values)[0]

        item.extend([title, author, cover_url])
        data.append(item)

    return render_template('recommend.html', data=data)


if _name_ == '_main_':
    app.run(debug=True)














































