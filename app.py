from flask import Flask, render_template, request
import pickle
import numpy as np
import pandas as pd

# Load data from pickle files
popular_df = pickle.load(open("popular.pkl", "rb"))
pt = pickle.load(open("pt.pkl", "rb"))
books = pickle.load(open("books.pkl", "rb"))
similarity_score = pickle.load(open("similarity_score.pkl", "rb"))

# --- Corrected syntax: __name__ with double underscores ---
app = Flask(__name__)

@app.route('/')
def index():
    # --- More efficient method for HD images using ISBN ---
    # Merge with the main books dataframe to get the ISBN for each popular book
    hd_popular_df = popular_df.merge(books, on='Book-Title').drop_duplicates('Book-Title').head(50)
    
    # Create a new list of high-definition image URLs using the ISBN
    hd_images = hd_popular_df['ISBN'].apply(lambda isbn: f"https://covers.openlibrary.org/b/isbn/{isbn}-L.jpg").tolist()
    
    return render_template(
        'index.html',
        book_name=list(hd_popular_df['Book-Title'].values),
        author=list(hd_popular_df['Book-Author_x'].values), # Use correct column name after merge
        image=hd_images,
        votes=list(hd_popular_df['num_ratings'].values),
        rating=list(hd_popular_df['avg_rating'].values)
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
    
    if user_input not in pt.index:
        return render_template('recommend.html', data=None, error=f"'{user_input}' not found. Please try another.", book_name=list(pt.index))
        
    index = np.where(pt.index == user_input)[0][0]
    similar_items = sorted(list(enumerate(similarity_score[index])), key=lambda x: x[1], reverse=True)[1:5]
    
    data = []
    for i in similar_items:
        item = []
        temp_df = books[books['Book-Title'] == pt.index[i[0]]].drop_duplicates('Book-Title')
        
        # --- Efficiently get details and HD image URL ---
        title = temp_df['Book-Title'].values[0]
        author = temp_df['Book-Author'].values[0]
        isbn = temp_df['ISBN'].values[0]
        hd_image_url = f"https://covers.openlibrary.org/b/isbn/{isbn}-L.jpg"
        
        item.extend([title, author, hd_image_url])
        data.append(item)
        
    return render_template('recommend.html', data=data, book_name=list(pt.index))

# --- Corrected syntax: __name__ and __main__ with double underscores ---
if __name__ == '__main__':
    app.run(debug=True)



















































