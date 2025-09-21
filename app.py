from flask import Flask, render_template,request
import pickle
import numpy as np
import pandas as pd


popular_df = pickle.load(open("popular.pkl", "rb"))
pt=pickle.load(open('pt.pkl','rb'))
books=pickle.load(open('books.pkl','rb'))
similarity_score=pickle.load(open('similarity_score.pkl','rb'))


app = Flask(__name__)  # ✅ FIXED LINE

@app.route('/')
def index():
    return render_template(
        'index.html',
        book_name=list(popular_df['Book-Title'].values),
        author=list(popular_df['Book-Author'].values),
        image=list(popular_df['Image-URL-M'].values),
        votes=list(popular_df['num_ratings'].values),
        rating=list(popular_df['avg_rating'].values)
    )
@app.route("/recommend")
def recommend_ui():
    # Make sure book_name is defined here
    book_name = [...]  # your list of book names
    return render_template("recommend.html", book_name=list(pt.index))

# ✅ New route for AJAX-based book suggestions
@app.route('/get_book_suggestions')
def get_book_suggestions():
    query = request.args.get('q', '').lower()
    matches = [book for book in pt.index if query in book.lower()]
    return {'books': matches[:10]}  # Return top 10 suggestions

@app.route('/recommend_books',methods=['POST'])
def recommend():
    user_input = request.form.get('user_input')
    matches = [book for book in pt.index if user_input.lower() in book.lower()]
    if not matches:
        return render_template('recommend.html', data=None, error="Book not found")

    # Use the first matching book title
    user_input = matches[0]
    index = np.where(pt.index == user_input)[0][0]
    similar_items = sorted(list(enumerate(similarity_score[index])), key=lambda x: x[1], reverse=True)[1:6]

    data = []
    for i in similar_items:
        item = []
        temp_df = (books[books['Book-Title'] == pt.index[i[0]]])
        item.extend(list(temp_df.drop_duplicates('Book-Title')['Book-Title'].values))
        item.extend(list(temp_df.drop_duplicates('Book-Title')['Book-Author'].values))
        item.extend(list(temp_df.drop_duplicates('Book-Title')['Image-URL-M'].values))
        data.append(item)

        print(data)
    return render_template('recommend.html',data=data)


if __name__ == '__main__':
    app.run(debug=True)
