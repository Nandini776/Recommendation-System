<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Book Recommender</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/css/bootstrap.min.css" rel="stylesheet">
    <style>
        body {
            background-color: #1a202c;
            color: white;
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
        }
        .navbar {
            background-color: #2d3748;
        }
        .navbar-brand, .nav-link {
            color: #48BB78 !important;
            font-weight: bold;
        }
        .card {
            background-color: #FF0000;
            border: none;
            border-radius: 10px;
            transition: transform 0.2s ease, box-shadow 0.2s ease;
            height: 100%; /* Ensure cards in a row are same height */
        }
        .card:hover {
            transform: translateY(-5px);
            box-shadow: 0 8px 16px rgba(0,0,0,0.3);
        }
        .card-img-top {
            width: 100%;
            height: 250px; /* Taller image for better quality display */
            object-fit: cover;
            border-top-left-radius: 10px;
            border-top-right-radius: 10px;
        }
        .card-body {
            padding: 1rem;
        }
        .card-title {
            font-size: 1.1rem;
            font-weight: bold;
            height: 3.3em; /* Fixed height for 2 lines of text */
            overflow: hidden;
        }
        .card-text {
            color: #A0AEC0;
            font-size: 0.9rem;
        }
    </style>
</head>
<body>

    <nav class="navbar navbar-expand-lg">
        <div class="container-fluid">
            <a class="navbar-brand">Book Recommender</a>
            <div class="collapse navbar-collapse">
                <ul class="navbar-nav">
                    <li class="nav-item"><a class="nav-link" href="/">Home</a></li>
                    <li class="nav-item"><a class="nav-link" href="/recommend">Recommend</a></li>
                </ul>
            </div>
        </div>
    </nav>

    <div class="container mt-4">
        <h1 class="text-center mb-4">Top 50 Books</h1>
        <div class="row">
            {% for i in range(book_name|length) %}
            <div class="col-md-3 mb-4">
                <div class="card">
                    <img src="{{ image[i] }}" class="card-img-top" alt="{{ book_name[i] }}">
                    <div class="card-body">
                        <h5 class="card-title">{{ book_name[i] }}</h5>
                        <p class="card-text">{{ author[i] }}</p>
                        <p class="card-text">Votes: {{ votes[i] }}</p>
                        <p class="card-text">Rating: {{ rating[i]|round(2) }}</p>
                    </div>
                </div>
            </div>
            {% endfor %}
        </div>
    </div>

</body>
</html>















































