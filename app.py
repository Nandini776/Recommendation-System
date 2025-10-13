import streamlit as st
import pickle
import numpy as np
import pandas as pd

# -----------------------------
# Load Pickle Data
# -----------------------------
@st.cache_data
def load_data():
    try:
        popular_df = pickle.load(open("popular.pkl", "rb"))
        pt = pickle.load(open('pt.pkl', 'rb'))
        books = pickle.load(open('books.pkl', 'rb'))
        similarity_score = pickle.load(open('similarity_score.pkl', 'rb'))
        return popular_df, pt, books, similarity_score
    except FileNotFoundError:
        st.error("❌ One or more pickle files not found. Please ensure all required files are in the directory.")
        return None, None, None, None


popular_df, pt, books, similarity_score = load_data()

# -----------------------------
# Page Configuration
# -----------------------------
st.set_page_config(
    layout="wide",
    page_title="Book Recommendation System",
    page_icon="📚"
)

# -----------------------------
# Custom CSS Styling
# -----------------------------
st.markdown("""
<style>
    html {
        scroll-behavior: smooth;
    }
    body {
        background-color: #0E1117;
    }
    .main .block-container {
        padding: 0;
    }

    /* Navbar */
    .navbar {
        background-color: #1a202c;
        padding: 1rem 2rem;
        display: flex;
        justify-content: space-between;
        align-items: center;
        flex-wrap: wrap;
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
    .navbar a:hover {
        color: #48BB78;
    }

    /* Container */
    .content-container {
        padding: 2rem 5%;
    }

    /* Title */
    .main-title {
        text-align: center;
        color: white;
        font-size: 2.3rem;
        font-weight: bold;
        margin-bottom: 2rem;
        margin-top: 2rem;
    }

    /* Responsive Grid */
    .book-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(180px, 1fr));
        gap: 1.2rem;
        width: 100%;
    }

    /* Book Cards */
    .book-card {
        background-color: #191919;
        border-radius: 0.75rem;
        overflow: hidden;
        color: white;
        display: flex;
        flex-direction: column;
        height: 100%;
        box-shadow: 0 4px 10px rgba(0,0,0,0.4);
        transition: transform 0.2s ease;
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
        font-size: 1rem;
        font-weight: bold;
        margin: 0 0 0.5rem 0;
        height: 3.2em;
        overflow: hidden;
    }
    .book-card-content p {
        font-size: 0.85rem;
        color: #A0AEC0;
        margin: 0.25rem 0;
    }

    /* Recommendation Section */
    .rec-container {
        margin-top: 3rem;
    }

    /* Footer */
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

    /* Mobile Fixes */
    @media (max-width: 768px) {
        .navbar {
            flex-direction: column;
            align-items: flex-start;
        }
        .navbar a {
            margin: 0.5rem 0 0 0;
        }
        .main-title {
            font-size: 1.8rem;
        }
        .book-card img {
            height: 220px;
        }
        .book-card-content h3 {
            font-size: 0.95rem;
        }
    }
</style>
""", unsafe_allow_html=True)

# -----------------------------
# Navbar
# -----------------------------
st.markdown("""
<div class="navbar" id="top">
    <h1>📚 Book Recommendation System</h1>
    <div>
        <a href="#home">Home</a>
        <a href="#recommend">Recommend</a>
    </div>
</div>
""", unsafe_allow_html=True)

st.markdown('<div class="content-container">', unsafe_allow_html=True)

# -----------------------------
# Recommendation Section
# -----------------------------
if pt is not None:
    st.markdown("<h2 class='main-title' id='recommend'>🔍 Find Similar Books</h2>", unsafe_allow_html=True)
    st.markdown("<div class='rec-container'>", unsafe_allow_html=True)

    book_list = ["Type a book name..."] + list(pt.index)
    selected_book_name = st.selectbox("Search your favorite book:", book_list, index=0)

    if st.button('Show Recommendations'):
        if selected_book_name == "Type a book name...":
            st.warning("⚠️ Please type or select a book from the dropdown.")
        else:
            st.subheader(f"Recommendations for **{selected_book_name}**:")
            
            index = np.where(pt.index == selected_book_name)[0][0]
            similar_items = sorted(list(enumerate(similarity_score[index])), key=lambda x: x[1], reverse=True)[1:6]
            
            st.markdown("<div class='book-grid'>", unsafe_allow_html=True)
            for item in similar_items:
                temp_df = books[books['Book-Title'] == pt.index[item[0]]]
                rec_title = temp_df.drop_duplicates('Book-Title')['Book-Title'].values[0]
                rec_author = temp_df.drop_duplicates('Book-Title')['Book-Author'].values[0]
                rec_image = temp_df.drop_duplicates('Book-Title')['Image-URL-M'].values[0]

                st.markdown(f"""
                <div class="book-card">
                    <img src="{rec_image}" alt="{rec_title}">
                    <div class="book-card-content">
                        <h3>{rec_title}</h3>
                        <p>Author: {rec_author}</p>
                    </div>
                </div>
                """, unsafe_allow_html=True)
            st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("</div>", unsafe_allow_html=True)

# -----------------------------
# Top 50 Books Section
# -----------------------------
if popular_df is not None:
    st.markdown("<h2 class='main-title' id='home'>🏆 Top 50 Books</h2>", unsafe_allow_html=True)
    
    st.markdown("<div class='book-grid'>", unsafe_allow_html=True)
    for i in range(len(popular_df)):
        st.markdown(f"""
        <div class="book-card">
            <img src="{popular_df['Image-URL-M'].iloc[i]}" alt="{popular_df['Book-Title'].iloc[i]}">
            <div class="book-card-content">
                <h3>{popular_df['Book-Title'].iloc[i]}</h3>
                <p>Author: {popular_df['Book-Author'].iloc[i]}</p>
                <p>Votes: {popular_df['num_ratings'].iloc[i]}</p>
                <p>Rating: {popular_df['avg_rating'].iloc[i]:.2f} ★</p>
            </div>
        </div>
        """, unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

# -----------------------------
# Footer
# -----------------------------
st.markdown("</div>", unsafe_allow_html=True)
st.markdown("""
<div class="footer">
    <p>© 2025 Book Recommendation System | Made with ♥ using Streamlit</p>
    <p>
        <a href="mailto:nandini9107@gmail.com">📧 Contact Us</a> | 
        <a href="https://github.com/Nandini776" target="_blank">👨‍💻 GitHub</a> | 
        <a href="#top">⬆ Back to Top</a>
    </p>
</div>
""", unsafe_allow_html=True)










































