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
        st.error("⚠️ Missing pickle files! Ensure all model files are in the same folder.")
        return None, None, None, None

popular_df, pt, books, similarity_score = load_data()

st.set_page_config(
    layout="wide",
    page_title="Book Recommendation System",
    page_icon="📚"
)

# ------------------------- STYLING -------------------------
st.markdown("""
<style>
    html { scroll-behavior: smooth; }
    body { background-color: #0E1117; }
    .main .block-container { padding: 0; }
    .navbar {
        background-color: #1a202c;
        padding: 1rem 2rem;
        display: flex;
        justify-content: space-between;
        align-items: center;
        width: 100%;
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
    .navbar a:hover { color: #48BB78; }
    .content-container { padding: 2rem 5%; }
    .main-title {
        text-align: center;
        color: white;
        font-size: 2.5rem;
        font-weight: bold;
        margin-bottom: 2rem;
        margin-top: 2rem;
    }
    .book-card-wrapper { padding: 0.5rem; }
    .book-card {
        background-color: #191919;
        border-radius: 0.5rem;
        overflow: hidden;
        color: white;
        height: 100%;
        display: flex;
        flex-direction: column;
        box-shadow: 0 4px 6px -1px rgba(0,0,0,0.1), 
                    0 2px 4px -1px rgba(0,0,0,0.06);
        transition: transform 0.2s;
    }
    .book-card:hover { transform: translateY(-5px); }
    .book-card img {
        width: 100%;
        height: 250px;
        object-fit: cover;
    }
    .book-card-content { padding: 1rem; }
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
</style>
""", unsafe_allow_html=True)

# ------------------------- NAVBAR -------------------------
st.markdown("""
<div class="navbar" id="top">
    <h1>📚 Book Recommendation System</h1>
    <div>
        <a href="#home">Home</a>
        <!-- Recommend button removed -->
    </div>
</div>
""", unsafe_allow_html=True)

st.markdown('<div class="content-container">', unsafe_allow_html=True)

# ------------------------- SEARCH BAR -------------------------
if books is not None and similarity_score is not None:
    st.markdown("<h2 class='main-title'>🔍 Find Similar Books</h2>", unsafe_allow_html=True)
    book_list = books['Book-Title'].values
    selected_book = st.selectbox("Search your favorite book:", book_list)

    if st.button('Show Recommendations'):
        index = np.where(pt.index == selected_book)[0][0]
        similar_items = sorted(
            list(enumerate(similarity_score[index])),
            key=lambda x: x[1],
            reverse=True
        )[1:6]

        st.markdown("### Recommended Books:")
        rec_cols = st.columns(5)
        for i, col in enumerate(rec_cols):
            with col:
                item = similar_items[i][0]
                temp_df = books[books['Book-Title'] == pt.index[item]]
                st.image(temp_df['Image-URL-M'].values[0], use_container_width=True)
                st.write(temp_df['Book-Title'].values[0])
                st.caption(f"By {temp_df['Book-Author'].values[0]}")

# ------------------------- TOP 50 BOOKS -------------------------
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

st.markdown("</div>", unsafe_allow_html=True)

# ------------------------- FOOTER -------------------------
st.markdown("""
<div class="footer">
    <p>© 2025 Book Recommendation System | Made with ♥ using Streamlit & Bootstrap</p>
    <p>
        <a href="mailto:nandini9107@gmail.com">📧 Contact Us</a> | 
        <a href="https://github.com/Nandini776" target="_blank">👨‍💻 GitHub</a> | 
        <a href="#top">⬆ Back to Top</a>
    </p>
</div>
""", unsafe_allow_html=True)








































