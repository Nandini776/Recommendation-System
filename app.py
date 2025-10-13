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
    @import url('https://fonts.googleapis.com/css2?family=Montserrat:wght@400;600;700&display=swap');
    
    html {
        scroll-behavior: smooth;
    }
    body {
        font-family: 'Montserrat', sans-serif;
        background: linear-gradient(to right, #0E1117, #1a202c);
        color: #fff;
    }
    .main .block-container {
        padding: 0;
    }
    .st-emotion-cache-16txtl3 {
        padding-top: 2rem;
    }
    .content-container {
        padding: 2rem 5%;
    }
    .main-title {
        text-align: center;
        color: white;
        font-size: 3rem;
        font-weight: 700;
        margin-bottom: 1rem;
        margin-top: 2rem;
        letter-spacing: 1.5px;
    }
    .book-card-wrapper {
        padding: 0.75rem;
    }
    .book-card {
        background-color: #1a202c;
        border-radius: 10px;
        overflow: hidden;
        color: white;
        height: 100%;
        display: flex;
        flex-direction: column;
        box-shadow: 0 4px 8px rgba(0,0,0,0.2);
        transition: transform 0.3s ease, box-shadow 0.3s ease;
        border: 1px solid #2d3748;
    }
    .book-card:hover {
        transform: translateY(-10px) scale(1.03);
        box-shadow: 0 12px 24px rgba(72, 187, 120, 0.2);
    }
    .book-card img {
        width: 100%;
        height: 250px;
        object-fit: cover;
    }
    .book-card-content {
        padding: 1rem;
        flex-grow: 1;
        display: flex;
        flex-direction: column;
    }
    .book-card-content h3 {
        font-size: 1.1rem;
        font-weight: 600;
        margin: 0 0 0.5rem 0;
        height: 3.3em; 
        overflow: hidden;
        flex-grow: 1;
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
        border-top: 1px solid #2d3748;
    }
    .footer a {
        color: #48BB78;
        text-decoration: none;
        transition: color 0.2s;
    }
    .footer a:hover {
        color: #fff;
    }
    .navbar {
        background-color: rgba(26, 32, 44, 0.8);
        backdrop-filter: blur(10px);
        padding: 1rem 2rem;
        display: flex;
        justify-content: space-between;
        align-items: center;
        width: 100%;
        position: fixed;
        top: 0;
        left: 0;
        z-index: 1000;
        border-bottom: 1px solid #2d3748;
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
        transition: color 0.2s;
    }
    .navbar a:hover {
        color: #48BB78;
    }
    .main-content-wrapper {
        padding-top: 80px;
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

# --- Home Section (Top 50 Books) ---
if popular_df is not None:
    st.markdown("<h2 class='main-title' id='home'>🏆 Top 50 Books</h2>", unsafe_allow_html=True)
    
    # --- Search Bar ---
    search_query = st.text_input("", placeholder="Search for a book by title or author...", label_visibility="collapsed")

    with st.spinner('Loading your favorite books...'):
        if search_query:
            filtered_df = popular_df[
                popular_df['Book-Title'].str.contains(search_query, case=False, na=False) |
                popular_df['Book-Author'].str.contains(search_query, case=False, na=False)
            ]
        else:
            # Display top 50 if no search query
            filtered_df = popular_df.head(50)

        if not filtered_df.empty:
            num_columns = 5
            cols = st.columns(num_columns)
            
            # Reset index to iterate properly
            filtered_df = filtered_df.reset_index()

            for i, row in filtered_df.iterrows():
                with cols[i % num_columns]:
                    st.markdown(f"""
                    <div class="book-card-wrapper">
                        <div class="book-card">
                            <img src="{row['Image-URL-M']}" alt="{row['Book-Title']}">
                            <div class="book-card-content">
                                <h3>{row['Book-Title']}</h3>
                                <p>Author: {row['Book-Author']}</p>
                                <p>Votes: {row['num_ratings']}</p>
                                <p>Rating: {row['avg_rating']:.2f} ★★★★★</p>
                            </div>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
        elif search_query:
            st.warning("No books found matching your search criteria.")

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


































