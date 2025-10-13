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
    </style>
    """, unsafe_allow_html=True)

@st.cache_data
def load_data():
    try:
        num_books = 20
        data = {
            'book_name': [f"Book Title {i+1}" for i in range(num_books)],
            'author': [f"Author Name {i+1}" for i in range(num_books)],
            'image': [
                "https://placehold.co/150x200/2c3e50/ffffff?text=Book+Cover+1", 
                "https://placehold.co/150x200/2c3e50/ffffff?text=Book+Cover+2",
                "https://placehold.co/150x200/2c3e50/ffffff?text=Book+Cover+3",
                "https://placehold.co/150x200/2c3e50/ffffff?text=Book+Cover+4"
            ] * 5,
            'votes': np.random.randint(100, 500, num_books),
            'rating': np.round(np.random.uniform(3.5, 5.0, num_books), 2)
        }
        df = pd.DataFrame(data)
        
        return df['book_name'].tolist(), df['author'].tolist(), df['image'].tolist(), df['votes'].tolist(), df['rating'].tolist()
        
    except FileNotFoundError:
        st.error("Error: Could not find model or data files (.pkl). Please ensure they are in the same directory.")
        return [], [], [], [], []

book_name, author, image, votes, rating = load_data()


def recommend(book_title):
    st.info(f"Generating recommendations for: {book_title}")
    
    return book_name[1:5], author[1:5], image[1:5]


tab1, tab2, tab3 = st.tabs(["📚 Top 50 Books (Home)", "✨ Get Recommendations", "📧 Contact Us"])

with tab1:
    st.title("Top 50 Books")
    
    cols = st.columns(4) 
    
    for i in range(len(book_name)):
        col_index = i % 4
        
        with cols[col_index]:
            st.markdown(f"**<h4 style='color:#00bcd4;'>{book_name[i]}</h4>**", unsafe_allow_html=True)
            
            st.image(image[i], width=150)
            
            st.markdown(f"**Author:** {author[i]}")
            st.markdown(f"**Votes:** {votes[i]}")
            st.markdown(f"**Rating:** {rating[i]}")
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
        
        rec_cols = st.columns(len(recommended_books))
        
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

