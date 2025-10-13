import streamlit as st
import pandas as pd
import pickle
import numpy as np

st.set_page_config(
    page_title="Book Recommender System",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
    <style>
    .reportview-container .main {
        background-color: #1c1e20;
        color: #e0e0e0;
    }
    h1 {
        color: #00bcd4;
    }
    h4 {
        color: #e0e0e0;
    }
    .stButton>button {
        color: white;
        background-color: #00796b;
    }
    .book-details {
        font-size: 0.9em;
        line-height: 1.5;
        margin-top: 10px;
    }
    .star-rating {
        color: gold;
        font-size: 1.1em;
    }
    </style>
    """, unsafe_allow_html=True)

@st.cache_data
def load_data():
    try:
        # Load the popular books data
        popular_df = pickle.load(open('popular.pkl', 'rb'))
        
        # Extract lists for Top 50 Books display
        book_name = popular_df['Book-Title'].tolist()
        author = popular_df['Book-Author'].tolist()
        image = popular_df['Image-URL-M'].tolist()
        votes = popular_df['num_ratings'].tolist()
        rating = popular_df['avg_rating'].tolist()
        
        # Load the main book data and the similarity matrix (needed for recommendations)
        pt = pickle.load(open('pt.pkl', 'rb')) # Pivot table
        books = pickle.load(open('books.pkl', 'rb')) # Books DataFrame
        similarity_scores = pickle.load(open('similarity_score.pkl', 'rb'))
        
        return book_name, author, image, votes, rating, pt, books, similarity_scores
        
    except FileNotFoundError:
        st.error("Error: Could not find model or data files (.pkl). Please ensure they are in the same directory.")
        return [], [], [], [], [], None, None, None

book_name, author, image, votes, rating, pt, books, similarity_scores = load_data()


def recommend(book_title):
    if pt is None or similarity_scores is None or books is None:
        st.error("Recommendation data is not loaded. Please check your data files.")
        return [], [], []

    if book_title not in pt.index:
        st.warning(f"Book '{book_title}' not found in the trained recommendation data.")
        return [], [], []

    # get index of the selected book
    index = np.where(pt.index == book_title)[0][0]
    # Calculate similarity scores and get top 5 (excluding the book itself)
    similar_items = sorted(list(enumerate(similarity_scores[index])), key=lambda x: x[1], reverse=True)[1:6]

    data = []
    for i in similar_items:
        item = []
        temp_df = books[books['Book-Title'] == pt.index[i[0]]]
        item.extend(list(temp_df.drop_duplicates('Book-Title')['Book-Title'].values))
        item.extend(list(temp_df.drop_duplicates('Book-Title')['Book-Author'].values))
        item.extend(list(temp_df.drop_duplicates('Book-Title')['Image-URL-M'].values))
        
        data.append(item)
    
    # Process data list into separate lists for Streamlit display
    rec_names = [d[0] for d in data]
    rec_authors = [d[1] for d in data]
    rec_images = [d[2] for d in data]
    
    return rec_names, rec_authors, rec_images


# Helper function to create star rating display
def get_star_rating(avg_rating):
    # Convert numerical rating to a string of Unicode stars
    stars_full = '★' * int(avg_rating)
    stars_half = '½' if (avg_rating - int(avg_rating)) >= 0.5 else ''
    stars_empty = '☆' * (5 - int(avg_rating) - (1 if stars_half else 0))
    return f'<span class="star-rating">{stars_full}{stars_half}</span>{stars_empty} ({avg_rating:.2f})'


tab1, tab2, tab3 = st.tabs(["📚 Top 50 Books (Home)", "✨ Get Recommendations", "📧 Contact Us"])

with tab1:
    st.title("Top 50 Books")
    
    cols = st.columns(4) 
    
    for i in range(len(book_name)):
        col_index = i % 4
        
        with cols[col_index]:
            st.markdown(f"**<h4 style='color:#00bcd4;'>{book_name[i]}</h4>**", unsafe_allow_html=True)
            
            st.image(image[i], width=150)
            
            # Use improved formatting with HTML/Markdown
            st.markdown(f"""
                <div class="book-details">
                    **Author:** {author[i]}<br>
                    **Votes:** {votes[i]}<br>
                    **Rating:** {get_star_rating(rating[i])}
                </div>
            """, unsafe_allow_html=True)
            
            st.markdown("---")

with tab2:
    st.title("Book Recommendation Engine")
    
    selected_book = st.selectbox(
        "Select a book to get personalized recommendations:",
        book_name
    )

    if st.button("Show Recommendations"):
        recommended_books, recommended_authors, recommended_images = recommend(selected_book)
        
        st.subheader(f"Recommendations for {selected_book}")
        
        # Adjust columns based on the number of actual recommendations (up to 5)
        rec_cols = st.columns(len(recommended_books) if recommended_books else 1) 
        
        for j in range(len(recommended_books)):
            with rec_cols[j]:
                st.image(recommended_images[j], width=120)
                st.markdown(f"**{recommended_books[j]}**")
                st.caption(f"by {recommended_authors[j]}")

with tab3:
    st.title("Contact Us")
    st.write("Thank you for using the My Book Recommender system. For inquiries, technical support, or feedback, please reach out.")
    st.markdown("""
        <div style="padding: 20px; background-color: #2c3e50; border-radius: 10px;">
            <p><strong>Email:</strong> support@bookrecommender.com</p>
            <p><strong>GitHub:</strong> [Link to your GitHub Repo]</p>
            <p><strong>Phone:</strong> +1-555-BOOK-REC</p>
        </div>
        """, unsafe_allow_html=True)


