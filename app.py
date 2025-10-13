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
    {"title": "Harry Potter and the Prisoner of Azkaban", "author": "J.K. Rowling", "votes": 428, "rating": 5.86, "stars": "★★★★★", "image_url": "http://images.amazon.com/images/P/0439136350.01.LZZZZZZZ.jpg"},
    {"title": "Harry Potter and the Goblet of Fire", "author": "J.K. Rowling", "votes": 387, "rating": 5.82, "stars": "★★★★★", "image_url": "http://images.amazon.com/images/P/0439139597.01.LZZZZZZZ.jpg"},
    {"title": "Harry Potter and the Sorcerer's Stone", "author": "J.K. Rowling", "votes": 278, "rating": 5.74, "stars": "★★★★★", "image_url": "http://images.amazon.com/images/P/059035342X.01.LZZZZZZZ.jpg"},
    {"title": "Harry Potter and the Order of the Phoenix", "author": "J.K. Rowling", "votes": 347, "rating": 5.5, "stars": "★★★★★", "image_url": "http://images.amazon.com/images/P/043935806X.01.LZZZZZZZ.jpg"},
    {"title": "The Chamber of Secrets", "author": "J.K. Rowling", "votes": 301, "rating": 5.4, "stars": "★★★★★", "image_url": "http://images.amazon.com/images/P/0439064872.01.LZZZZZZZ.jpg"},
    {"title": "The Hobbit", "author": "J.R.R. Tolkien", "votes": 489, "rating": 5.9, "stars": "★★★★★", "image_url": "http://images.amazon.com/images/P/0618260307.01.LZZZZZZZ.jpg"},
    {"title": "The Lord of the Rings", "author": "J.R.R. Tolkien", "votes": 521, "rating": 5.95, "stars": "★★★★★", "image_url": "http://images.amazon.com/images/P/0618346244.01.LZZZZZZZ.jpg"},
    {"title": "The Fellowship of the Ring", "author": "J.R.R. Tolkien", "votes": 450, "rating": 5.88, "stars": "★★★★★", "image_url": "http://images.amazon.com/images/P/0618346252.01.LZZZZZZZ.jpg"},
    {"title": "To Kill a Mockingbird", "author": "Harper Lee", "votes": 632, "rating": 5.98, "stars": "★★★★★", "image_url": "http://images.amazon.com/images/P/0446310786.01.LZZZZZZZ.jpg"},
    {"title": "1984", "author": "George Orwell", "votes": 741, "rating": 5.91, "stars": "★★★★★", "image_url": "http://images.amazon.com/images/P/0451524934.01.LZZZZZZZ.jpg"},
    {"title": "The Great Gatsby", "author": "F. Scott Fitzgerald", "votes": 521, "rating": 5.72, "stars": "★★★★★", "image_url": "http://images.amazon.com/images/P/0743273567.01.LZZZZZZZ.jpg"},
    {"title": "The Catcher in the Rye", "author": "J.D. Salinger", "votes": 488, "rating": 5.65, "stars": "★★★★★", "image_url": "http://images.amazon.com/images/P/0316769487.01.LZZZZZZZ.jpg"},
    {"title": "Pride and Prejudice", "author": "Jane Austen", "votes": 589, "rating": 5.85, "stars": "★★★★★", "image_url": "http://images.amazon.com/images/P/0553213105.01.LZZZZZZZ.jpg"},
    {"title": "Animal Farm", "author": "George Orwell", "votes": 615, "rating": 5.81, "stars": "★★★★★", "image_url": "http://images.amazon.com/images/P/0451526341.01.LZZZZZZZ.jpg"},
    {"title": "Fahrenheit 451", "author": "Ray Bradbury", "votes": 499, "rating": 5.79, "stars": "★★★★★", "image_url": "http://images.amazon.com/images/P/0345342968.01.LZZZZZZZ.jpg"},
    {"title": "The Diary of a Young Girl", "author": "Anne Frank", "votes": 401, "rating": 5.92, "stars": "★★★★★", "image_url": "http://images.amazon.com/images/P/0553296981.01.LZZZZZZZ.jpg"},
    {"title": "Dune", "author": "Frank Herbert", "votes": 850, "rating": 5.96, "stars": "★★★★★", "image_url": "http://images.amazon.com/images/P/0441013597.01.LZZZZZZZ.jpg"},
    {"title": "The Two Towers", "author": "J.R.R. Tolkien", "votes": 480, "rating": 5.91, "stars": "★★★★★", "image_url": "http://images.amazon.com/images/P/0618346260.01.LZZZZZZZ.jpg"},
    {"title": "The Return of the King", "author": "J.R.R. Tolkien", "votes": 495, "rating": 5.94, "stars": "★★★★★", "image_url": "http://images.amazon.com/images/P/0618346279.01.LZZZZZZZ.jpg"},
    {"title": "The Hitchhiker's Guide to the Galaxy", "author": "Douglas Adams", "votes": 721, "rating": 5.89, "stars": "★★★★★", "image_url": "http://images.amazon.com/images/P/0345391802.01.LZZZZZZZ.jpg"},
    {"title": "Brave New World", "author": "Aldous Huxley", "votes": 654, "rating": 5.82, "stars": "★★★★★", "image_url": "http://images.amazon.com/images/P/0060929871.01.LZZZZZZZ.jpg"},
    {"title": "Moby Dick", "author": "Herman Melville", "votes": 350, "rating": 5.60, "stars": "★★★★★", "image_url": "http://images.amazon.com/images/P/0553213113.01.LZZZZZZZ.jpg"},
    {"title": "War and Peace", "author": "Leo Tolstoy", "votes": 388, "rating": 5.75, "stars": "★★★★★", "image_url": "http://images.amazon.com/images/P/0679723275.01.LZZZZZZZ.jpg"},
    {"title": "Adventures of Huckleberry Finn", "author": "Mark Twain", "votes": 412, "rating": 5.71, "stars": "★★★★★", "image_url": "http://images.amazon.com/images/P/0553210726.01.LZZZZZZZ.jpg"},
    {"title": "Alice's Adventures in Wonderland", "author": "Lewis Carroll", "votes": 510, "rating": 5.83, "stars": "★★★★★", "image_url": "http://images.amazon.com/images/P/0451527747.01.LZZZZZZZ.jpg"},
    {"title": "The Shining", "author": "Stephen King", "votes": 689, "rating": 5.88, "stars": "★★★★★", "image_url": "http://images.amazon.com/images/P/0385121679.01.LZZZZZZZ.jpg"},
    {"title": "A Game of Thrones", "author": "George R.R. Martin", "votes": 954, "rating": 5.97, "stars": "★★★★★", "image_url": "http://images.amazon.com/images/P/0553573403.01.LZZZZZZZ.jpg"},
    {"title": "The Hunger Games", "author": "Suzanne Collins", "votes": 789, "rating": 5.84, "stars": "★★★★★", "image_url": "http://images.amazon.com/images/P/0439023521.01.LZZZZZZZ.jpg"},
    {"title": "The Girl with the Dragon Tattoo", "author": "Stieg Larsson", "votes": 699, "rating": 5.87, "stars": "★★★★★", "image_url": "http://images.amazon.com/images/P/0307269752.01.LZZZZZZZ.jpg"},
    {"title": "Gone Girl", "author": "Gillian Flynn", "votes": 711, "rating": 5.90, "stars": "★★★★★", "image_url": "http://images.amazon.com/images/P/0307588378.01.LZZZZZZZ.jpg"},
    {"title": "The Martian", "author": "Andy Weir", "votes": 821, "rating": 5.93, "stars": "★★★★★", "image_url": "http://images.amazon.com/images/P/0804139024.01.LZZZZZZZ.jpg"},
    {"title": "Sapiens", "author": "Yuval Noah Harari", "votes": 765, "rating": 5.95, "stars": "★★★★★", "image_url": "http://images.amazon.com/images/P/0062316095.01.LZZZZZZZ.jpg"},
    {"title": "Educated", "author": "Tara Westover", "votes": 680, "rating": 5.94, "stars": "★★★★★", "image_url": "http://images.amazon.com/images/P/0399590501.01.LZZZZZZZ.jpg"},
    {"title": "Becoming", "author": "Michelle Obama", "votes": 702, "rating": 5.92, "stars": "★★★★★", "image_url": "http://images.amazon.com/images/P/1524763136.01.LZZZZZZZ.jpg"},
    {"title": "The Alchemist", "author": "Paulo Coelho", "votes": 810, "rating": 5.85, "stars": "★★★★★", "image_url": "http://images.amazon.com/images/P/0062502174.01.LZZZZZZZ.jpg"},
    {"title": "The Kite Runner", "author": "Khaled Hosseini", "votes": 755, "rating": 5.91, "stars": "★★★★★", "image_url": "http://images.amazon.com/images/P/1594480001.01.LZZZZZZZ.jpg"},
    {"title": "Where the Crawdads Sing", "author": "Delia Owens", "votes": 798, "rating": 5.88, "stars": "★★★★★", "image_url": "http://images.amazon.com/images/P/0735219095.01.LZZZZZZZ.jpg"},
    {"title": "The Silent Patient", "author": "Alex Michaelides", "votes": 732, "rating": 5.89, "stars": "★★★★★", "image_url": "http://images.amazon.com/images/P/1250301696.01.LZZZZZZZ.jpg"},
    {"title": "Atomic Habits", "author": "James Clear", "votes": 888, "rating": 5.97, "stars": "★★★★★", "image_url": "http://images.amazon.com/images/P/0735211299.01.LZZZZZZZ.jpg"},
    {"title": "The Da Vinci Code", "author": "Dan Brown", "votes": 763, "rating": 5.80, "stars": "★★★★★", "image_url": "http://images.amazon.com/images/P/0385504209.01.LZZZZZZZ.jpg"},
    {"title": "The Subtle Art of Not Giving a F*ck", "author": "Mark Manson", "votes": 791, "rating": 5.82, "stars": "★★★★★", "image_url": "http://images.amazon.com/images/P/0062457713.01.LZZZZZZZ.jpg"},
    {"title": "Ready Player One", "author": "Ernest Cline", "votes": 801, "rating": 5.86, "stars": "★★★★★", "image_url": "http://images.amazon.com/images/P/030788743X.01.LZZZZZZZ.jpg"},
    {"title": "Circe", "author": "Madeline Miller", "votes": 692, "rating": 5.93, "stars": "★★★★★", "image_url": "http://images.amazon.com/images/P/0316556343.01.LZZZZZZZ.jpg"},
    {"title": "The Song of Achilles", "author": "Madeline Miller", "votes": 715, "rating": 5.94, "stars": "★★★★★", "image_url": "http://images.amazon.com/images/P/0062060627.01.LZZZZZZZ.jpg"},
    {"title": "The Road", "author": "Cormac McCarthy", "votes": 621, "rating": 5.81, "stars": "★★★★★", "image_url": "http://images.amazon.com/images/P/0307265439.01.LZZZZZZZ.jpg"},
    {"title": "The Handmaid's Tale", "author": "Margaret Atwood", "votes": 733, "rating": 5.89, "stars": "★★★★★", "image_url": "http://images.amazon.com/images/P/038549081X.01.LZZZZZZZ.jpg"},
    {"title": "Frankenstein", "author": "Mary Shelley", "votes": 555, "rating": 5.78, "stars": "★★★★★", "image_url": "http://images.amazon.com/images/P/0553212478.01.LZZZZZZZ.jpg"},
    {"title": "Dracula", "author": "Bram Stoker", "votes": 582, "rating": 5.79, "stars": "★★★★★", "image_url": "http://images.amazon.com/images/P/0553212761.01.LZZZZZZZ.jpg"},
    {"title": "Jane Eyre", "author": "Charlotte Brontë", "votes": 567, "rating": 5.84, "stars": "★★★★★", "image_url": "http://images.amazon.com/images/P/0553211404.01.LZZZZZZZ.jpg"},
    {"title": "Wuthering Heights", "author": "Emily Brontë", "votes": 531, "rating": 5.76, "stars": "★★★★★", "image_url": "http://images.amazon.com/images/P/0553212583.01.LZZZZZZZ.jpg"},
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













