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
    /* 1. Base Theme & Colors (Dark Mode) */
    .reportview-container .main {
        background-color: #1c1e20;
        color: #e0e0e0;
    }
    .stApp {
        background-color: #1c1e20;
    }
    
    /* 2. Typography and Titles */
    h1 {
        color: #00bcd4; /* Bright Teal for main titles */
        font-weight: 700;
        text-shadow: 1px 1px 3px rgba(0, 0, 0, 0.5);
    }
    h2, h3, h4 {
        color: #e0e0e0;
    }
    .st-emotion-cache-12fmw5g { /* Targets the internal style for Top 50 Books title */
        color: #00bcd4 !important; 
        text-shadow: 1px 1px 3px rgba(0, 0, 0, 0.5);
    }

    /* 3. Buttons (Interactive Highlight) */
    .stButton>button {
        color: white;
        background-color: #00a65a; /* Bright Green */
        border: none;
        border-radius: 8px;
        padding: 10px 20px;
        font-weight: bold;
        transition: all 0.2s ease;
        box-shadow: 0 4px 10px rgba(0, 166, 90, 0.4);
    }
    .stButton>button:hover {
        background-color: #00796b; /* Slightly darker green on hover */
        transform: translateY(-2px);
        box-shadow: 0 6px 15px rgba(0, 166, 90, 0.6);
    }

    /* 4. Tab Styling (Interactive Navigation) */
    .st-emotion-cache-1ftk8e { /* Targets the primary tab container */
        background-color: #2c3e50; /* Darker blue for tab background */
        border-radius: 10px;
        padding: 5px 0;
    }
    .st-emotion-cache-1gjnqny { /* Targets active tab link/button */
        color: #00bcd4; /* Teal for active text */
        border-bottom: 2px solid #00bcd4;
        font-weight: bold;
    }
    .st-emotion-cache-1gjnqny:hover {
        color: #a7ffeb; /* Lighter teal on hover */
    }


    /* 5. Book Card Styling (Simulate Card Look) */
    /* This targets the container holding each book in the grid */
    .st-emotion-cache-ocqkz3 { /* Column container */
        background-color: #282828;
        padding: 15px;
        border-radius: 12px;
        margin-bottom: 25px;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.5);
        transition: all 0.3s ease;
    }
    .st-emotion-cache-ocqkz3:hover {
        box-shadow: 0 6px 20px rgba(0, 188, 212, 0.3); /* Teal glow on hover */
        transform: translateY(-4px);
    }

    /* Input/Select Box Styling */
    .st-emotion-cache-4oy5x3 { /* Targets Selectbox input field */
        background-color: #333;
        color: white;
        border-radius: 8px;
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

st.title("Book Recommendation System")

@st.cache_data
def load_data():
    try:
        popular_df = pickle.load(open('popular.pkl', 'rb'))
        
        book_name = popular_df['Book-Title'].tolist()
        author = popular_df['Book-Author'].tolist()
        image = popular_df['Image-URL-M'].tolist()
        votes = popular_df['num_ratings'].tolist()
        rating = popular_df['avg_rating'].tolist()
        
        pt = pickle.load(open('pt.pkl', 'rb'))
        books = pickle.load(open('books.pkl', 'rb'))
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

    index = np.where(pt.index == book_title)[0][0]
    similar_items = sorted(list(enumerate(similarity_scores[index])), key=lambda x: x[1], reverse=True)[1:6]

    data = []
    for i in similar_items:
        item = []
        temp_df = books[books['Book-Title'] == pt.index[i[0]]]
        item.extend(list(temp_df.drop_duplicates('Book-Title')['Book-Title'].values))
        item.extend(list(temp_df.drop_duplicates('Book-Title')['Book-Author'].values))
        item.extend(list(temp_df.drop_duplicates('Book-Title')['Image-URL-M'].values))
        
        data.append(item)
    
    rec_names = [d[0] for d in data]
    rec_authors = [d[1] for d in data]
    rec_images = [d[2] for d in data]
    
    return rec_names, rec_authors, rec_images


def get_star_rating(avg_rating):
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
        
        rec_cols = st.columns(len(recommended_books) if recommended_books else 1) 
        
        for j in range(len(recommended_books)):
            with rec_cols[j]:
                st.image(recommended_images[j], width=120)
                st.markdown(f"**{recommended_books[j]}**")
                st.caption(f"by {recommended_authors[j]}")

with tab3:
    st.title("Contact Us")
    st.write("Thank you for using the Book Recommender system. For inquiries, technical support, or feedback, please reach out.")
    st.markdown(f"""
        <div style="padding: 20px; background-color: #2c3e50; border-radius: 10px;">
            <p><strong>Email:</strong> <a href="mailto:nandini9107@gmail.com" style="color: #00bcd4;">nandini9107@gmail.com</a></p>
            <p><strong>GitHub:</strong> <a href="https://github.com/Nandini776" style="color: #00bcd4;" target="_blank">https://github.com/Nandini776</a></p>
        </div>
        """, unsafe_allow_html=True)





