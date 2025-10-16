from flask import Flask, render_template, request
import pickle
import pandas as pd
import numpy as np

popular_books = pickle.load(open("popular.pkl", "rb"))
pt = pickle.load(open("pt.pkl", "rb"))
books_df = pickle.load(open("books.pkl", "rb"))
similarity = pickle.load(open("similarity_score.pkl", "rb"))

app = Flask(__name__)

@app.route('/')
def index():
    top_books = popular_books.merge(books_df, on='Book-Title').drop_duplicates('Book-Title').head(50)
    images = top_books['ISBN'].apply(lambda x: f"https://covers.openlibrary.org/b/isbn/{x}-L.jpg").tolist()
    return render_template(
        'index.html',
        book_name=list(top_books['Book-Title'].values),
        author=list(top_books['Book-Author_x'].values),
        image=images,
        votes=list(top_books['num_ratings'].values),
        rating=list(top_books['avg_rating'].values)
    )

@app.route("/recommend")
def recommend_ui():
    return render_template("recommend.html", book_name=list(pt.index))

@app.route('/get_book_suggestions')
def get_book_suggestions():
    query = request.args.get('q', '').strip().lower()
    matches = [title for title in pt.index if query in title.lower()]
    return {'books': matches[:10]}

@app.route('/recommend_books', methods=['POST'])
def recommend():
    user_input = request.form.get('user_input')
    if user_input not in pt.index:
        error_msg = f"'{user_input}' not found. Try another book title."
        return render_template('recommend.html', data=None, error=error_msg, book_name=list(pt.index))
    
    idx = np.where(pt.index == user_input)[0][0]
    similar = sorted(list(enumerate(similarity[idx])), key=lambda x: x[1], reverse=True)[1:5]

    data = []
    for i in similar:
        match = books_df[books_df['Book-Title'] == pt.index[i[0]]].drop_duplicates('Book-Title')
        if not match.empty:
            title = match['Book-Title'].values[0]
            author = match['Book-Author'].values[0]
            isbn = match['ISBN'].values[0]
            img_url = f"https://covers.openlibrary.org/b/isbn/{isbn}-L.jpg"
            data.append([title, author, img_url])

    return render_template('recommend.html', data=data, book_name=list(pt.index))

if __name__ == '__main__':
    app.run(debug=True)




















































