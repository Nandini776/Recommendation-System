import streamlit as st

st.set_page_config(
    layout="wide",
    page_title="Book Recommendation System",
    page_icon="📚"
)

st.markdown("""
<style>
    body {
        background-color: #0E1117;
    }
    .main .block-container {
        padding: 0;
    }
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
    .navbar a:hover {
        color: #48BB78;
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

st.markdown("""
<div class="navbar">
    <h1>📚 Book Recommendation System</h1>
    <div>
        <a href="#">Home</a>
        <a href="#">Recommend</a>
    </div>
</div>
""", unsafe_allow_html=True)

st.markdown('<div class="content-container">', unsafe_allow_html=True)

st.markdown("<h2 class='main-title'>🏆 Top 50 Books</h2>", unsafe_allow_html=True)

books_data = [
    {"title": "Harry Potter and the Prisoner of Azkaban", "author": "J.K. Rowling", "votes": 428, "rating": 5.86, "stars": "★★★★★", "image_url": "https://placehold.co/200x250/7e22ce/white?text=Azkaban"},
    {"title": "Harry Potter and the Goblet of Fire", "author": "J.K. Rowling", "votes": 387, "rating": 5.82, "stars": "★★★★★", "image_url": "https://placehold.co/200x250/f97316/white?text=Goblet+of+Fire"},
    {"title": "Harry Potter and the Sorcerer's Stone", "author": "J.K. Rowling", "votes": 278, "rating": 5.74, "stars": "★★★★★", "image_url": "https://placehold.co/200x250/ef4444/white?text=Sorcerer's+Stone"},
    {"title": "Harry Potter and the Order of the Phoenix", "author": "J.K. Rowling", "votes": 347, "rating": 5.5, "stars": "★★★★★", "image_url": "https://placehold.co/200x250/3b82f6/white?text=Order+of+Phoenix"},
    {"title": "The Chamber of Secrets", "author": "J.K. Rowling", "votes": 301, "rating": 5.4, "stars": "★★★★★", "image_url": "https://placehold.co/200x250/10b981/white?text=Chamber+of+Secrets"},
    {"title": "The Hobbit", "author": "J.R.R. Tolkien", "votes": 489, "rating": 5.9, "stars": "★★★★★", "image_url": "https://placehold.co/200x250/f59e0b/white?text=The+Hobbit"},
    {"title": "The Lord of the Rings", "author": "J.R.R. Tolkien", "votes": 521, "rating": 5.95, "stars": "★★★★★", "image_url": "https://placehold.co/200x250/be123c/white?text=Lord+of+the+Rings"},
    {"title": "The Fellowship of the Ring", "author": "J.R.R. Tolkien", "votes": 450, "rating": 5.88, "stars": "★★★★★", "image_url": "https://placehold.co/200x250/1f2937/white?text=Fellowship"},
]

num_columns = 4
cols = st.columns(num_columns)

for index, book in enumerate(books_data):
    with cols[index % num_columns]:
        st.markdown(f"""
        <div class="book-card-wrapper">
            <div class="book-card">
                <img src="{book['image_url']}" alt="{book['title']}">
                <div class="book-card-content">
                    <h3>{book['title']}</h3>
                    <p>Author: {book['author']}</p>
                    <p>Votes: {book['votes']}</p>
                    <p>Rating: {book['rating']} {book['stars']}</p>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)

st.markdown("</div>", unsafe_allow_html=True)
st.markdown("""
<div class="footer">
    <p>© 2025 Book Recommendation System | Made with ♥ using Flask & Bootstrap</p>
    <p>
        <a href="#">📧 Contact Us</a> | 
        <a href="#">👨‍💻 GitHub</a> | 
        <a href="#">⬆️ Back to Top</a>
    </p>
</div>
""", unsafe_allow_html=True)









