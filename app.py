from flask import Flask, render_template, request
import pickle
import numpy as np
import pandas as pd

# Load data from pickle files
popular_df = pickle.load(open("popular.pkl", "rb"))
pt = pickle.load(open("pt.pkl", "rb"))
books = pickle.load(open("books.pkl", "rb"))
similarity_score = pickle.load(open("similarity_score.pkl", "rb"))

app = Flask(__name__)

@app.route('/')
def index():
    # Merge with the main books dataframe to get the ISBN for each popular book
    # Using drop_duplicates to prevent issues with multiple editions
    hd_popular_df = popular_df.merge(books, on='Book-Title').drop_duplicates('Book-Title').head(50)
    
    # Create a new list of high-definition image URLs using the ISBN
    hd_images = hd_popular_df['ISBN'].apply(lambda isbn: f"https://covers.openlibrary.org/b/isbn/{isbn}-L.jpg").tolist()
    
    return render_template(
        'index.html',
        book_name=list(hd_popular_df['Book-Title'].values),
        author=list(hd_popular_df['Book-Author'].values),
        image=hd_images,  # Send the new HD image links to the template
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
    
    # Handle case where user input is not in the pivot table
    if user_input not in pt.index:
        return render_template('recommend.html', data=None, error=f"'{user_input}' not found in our database. Please try another.", book_name=list(pt.index))
        
    index = np.where(pt.index == user_input)[0][0]
    similar_items = sorted(list(enumerate(similarity_score[index])), key=lambda x: x[1], reverse=True)[1:5] # Fetches 4 similar books
    
    data = []
    for i in similar_items:
        item = []
        temp_df = books[books['Book-Title'] == pt.index[i[0]]]
        
        # Ensure we get unique entries
        temp_df = temp_df.drop_duplicates('Book-Title')
        
        # Extract details
        title = temp_df['Book-Title'].values[0]
        author = temp_df['Book-Author'].values[0]
        isbn = temp_df['ISBN'].values[0]
        
        # Create HD image URL
        hd_image_url = f"https://covers.openlibrary.org/b/isbn/{isbn}-L.jpg"
        
        # Populate the item list
        item.extend([title, author, hd_image_url])
        data.append(item)
        
    return render_template('recommend.html', data=data, book_name=list(pt.index))

# Corrected syntax for the main execution block
if __name__ == '__main__':
    app.run(debug=True)
















































