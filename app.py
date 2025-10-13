import streamlit as st
import pickle
import numpy as np
import pandas as pd

@st.cache_data
def load_data():
    try:
        popular_df = pickle.load(open("popular.pkl", "rb"))
        pt = pickle.load(open('pt.pkl', 'rb'))
        books = pickle.load(open('books.pkl', 'rb'))
        similarity_score = pickle.load(open('similarity_score.pkl', 'rb'))
        return popular_df, pt, books, similarity_score
    except FileNotFoundError:
        st.error("One or more pickle files not found. Please make sure popular.pkl, pt.pkl, books.pkl, and similarity_score.pkl are in the same directory.")
        return None, None, None, None

popular_df, pt, books, similarity_score = load_data()

st.set_page_config(
    layout="wide",
    page_title="Book Recommendation System",
    page_icon="📚"
)

st.markdown("""
<style>
    html {
        scroll-behavior: smooth;
    }
    body {
        background-color: #0E1117;
    }
    /* Remove padding from the main block container */
    .main .block-container {
        padding: 0;
    }
    /* Adjust padding for Streamlit's main content area */
    .st-emotion-cache-16txtl3 {
        padding-top: 2rem;
    }
    .content-container {
        padding: 2rem 5%;
    }
    .main-title {
        text-align: center;
        color: white;
        font-size: 2.5rem;
        font-weight: bold;
        margin-bottom: 2rem;
        margin-top: 2rem;
    }
    .book-card-wrapper {
        padding: 0.5rem;
    }
    .book-card {
        background-color: #191919;
        border-radius: 0.5rem;
        overflow: hidden;
        color: white;
        height: 100%;
        display: flex;
        flex-direction: column;
        box-shadow: 0 4px 6px -1px rgba(0,0,0,0.1), 0 2px 4px -1px rgba(0,0,0,0.06);
        transition: transform 0.2s;
    }
    .book-card:hover {
        transform: translateY(-5px);
    }
    .book-card img {
        width: 100%;
        height: 250px;
        object-fit: cover;
    }
    .book-card-content {
        padding: 1rem;
    }
    .book-card-content h3 {
        font-size: 1.1rem;
        font-weight: bold;
        margin: 0 0 0.5rem 0;
        height: 3.3em; 
        overflow: hidden;
    }
    .book-card-content p {
        font-size: 0.9rem;
        color: #A0AEC0;
        margin: 0.25rem 0;
    }
    .footer {
        text-align: center;
        padding: 2rem;
        margin-top: 3rem;
        color: #A0AEC0;
        font-size: 0.9rem;
    }
    .footer a {
        color: #48BB78;
        text-decoration: none;
    }
    .navbar {
        background-color: #1a202c;
        padding: 1rem 2rem;
        display: flex;
        justify-content: space-between;
        align-items: center;
        width: 100%;
        position: fixed;
        top: 0;
        left: 0;
        z-index: 1000;
    }
    .navbar h1 {
        color: #48BB78;
        margin: 0;
        font-size: 1.5rem;
    }
    .navbar a {
        color: white;
        text-decoration: none;
        margin-left: 1.5rem;
        font-weight: 500;
    }
    .navbar a:hover {
        color: #48BB78;
    }
    .main-content-wrapper {
        padding-top: 80px; /* Add padding to offset fixed navbar */
    }
</style>
""", unsafe_allow_html=True)


# --- Top Navigation Bar ---
st.markdown("""
<div class="navbar" id="top">
    <h1>📚 Book Recommendation System</h1>
    <div>
        <a href="#home">Home</a>
        <a href="#recommend">Recommend</a>
    </div>
</div>
""", unsafe_allow_html=True)


# --- Main Content Area ---
st.markdown('<div class="main-content-wrapper"><div class="content-container">', unsafe_allow_html=True)

# --- Recommend Section ---
if pt is not None:
    st.markdown("<h2 class='main-title' id='recommend'>📖 Recommend Books</h2>", unsafe_allow_html=True)

    book_list = ["Type book name..."] + list(pt.index)
    selected_book_name = st.selectbox(
        "Type or select a book to get recommendations",
        book_list,
        index=0
    )

    if st.button('Show Recommendations'):
        if selected_book_name == "Type book name...":
            st.warning("Please select a book from the dropdown list.")
        else:
            st.subheader(f"Recommendations for {selected_book_name}:")
            
            index = np.where(pt.index == selected_book_name)[0][0]
            similar_items = sorted(list(enumerate(similarity_score[index])), key=lambda x: x[1], reverse=True)[1:6]

            rec_cols = st.columns(5)
            
            for i, item in enumerate(similar_items):
                with rec_cols[i]:
                    temp_df = books[books['Book-Title'] == pt.index[item[0]]]
                    rec_title = temp_df.drop_duplicates('Book-Title')['Book-Title'].values[0]
                    rec_author = temp_df.drop_duplicates('Book-Title')['Book-Author'].values[0]
                    rec_image = temp_df.drop_duplicates('Book-Title')['Image-URL-M'].values[0]

                    st.markdown(f"""
                    <div class="book-card-wrapper">
                        <div class="book-card">
                            <img src="{rec_image}" alt="{rec_title}">
                            <div class="book-card-content">
                                <h3>{rec_title}</h3>
                                <p>Author: {rec_author}</p>
                            </div>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)

# --- Home Section (Top 50) ---
if popular_df is not None:
    st.markdown("<h2 class='main-title' id='home'>🏆 Top 50 Books</h2>", unsafe_allow_html=True)
    
    num_columns = 5
    cols = st.columns(num_columns)

    for i in range(50):
        with cols[i % num_columns]:
            st.markdown(f"""
            <div class="book-card-wrapper">
                <div class="book-card">
                    <img src="{popular_df['Image-URL-M'].iloc[i]}" alt="{popular_df['Book-Title'].iloc[i]}">
                    <div class="book-card-content">
                        <h3>{popular_df['Book-Title'].iloc[i]}</h3>
                        <p>Author: {popular_df['Book-Author'].iloc[i]}</p>
                        <p>Votes: {popular_df['num_ratings'].iloc[i]}</p>
                        <p>Rating: {popular_df['avg_rating'].iloc[i]:.2f} ★★★★★</p>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)

st.markdown("</div></div>", unsafe_allow_html=True)


# --- Footer ---
st.markdown("""
<div class="footer">
    <p>© 2025 Book Recommendation System | Made with ♥ using Flask & Bootstrap</p>
    <p>
        <a href="mailto:nandini9107@gmail.com">📧 Contact Us</a> | 
        <a href="https://github.com/Nandini776" target="_blank">👨‍💻 GitHub</a> |
        <a href="#top">⬆️ Back to Top</a>
    </p>
</div>
""", unsafe_allow_html=True)




























