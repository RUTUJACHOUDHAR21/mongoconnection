from flask import Flask, request, render_template_string
from pymongo import MongoClient
import os

app = Flask(__name__)

# MongoDB Atlas URI from environment variable
uri = os.getenv("MONGO_URI")
if not uri or not uri.startswith(("mongodb://", "mongodb+srv://")):
    raise ValueError("MONGO_URI is missing or incorrectly formatted.")

client = MongoClient(uri)

# Connect to DB and Collection
db = client["test_database"]
signup_collection = db["signup_collection"]
contact_collection = db["contact_collection"]

# HTML Template with Tabs
template = """
<!DOCTYPE html>
<html>
<head>
    <title>Interactive Forms</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            background: #f4f4f4;
            padding: 50px 20px;
            display: flex;
            flex-direction: column;
            align-items: center;
        }
        .tabs {
            display: flex;
            margin-bottom: 20px;
        }
        .tab-button {
            padding: 10px 30px;
            border: none;
            border-bottom: 2px solid transparent;
            background: none;
            font-size: 16px;
            cursor: pointer;
        }
        .tab-button.active {
            border-bottom: 2px solid #4CAF50;
            font-weight: bold;
        }
        .form-container {
            background: white;
            padding: 30px 40px;
            border-radius: 12px;
            box-shadow: 0 8px 20px rgba(0, 0, 0, 0.1);
            width: 400px;
            display: none;
        }
        .form-container.active {
            display: block;
        }
        input[type="text"], input[type="email"], textarea {
            width: 100%;
            padding: 12px;
            margin: 10px 0 20px;
            border: 1px solid #ccc;
            border-radius: 6px;
            font-size: 16px;
        }
        textarea {
            resize: vertical;
            height: 80px;
        }
        input[type="submit"] {
            padding: 12px 25px;
            border: none;
            background-color: #4CAF50;
            color: white;
            border-radius: 6px;
            font-size: 16px;
            cursor: pointer;
        }
        input[type="submit"]:hover {
            background-color: #45a049;
        }
        .message {
            margin-top: 15px;
            color: green;
            font-weight: bold;
        }
    </style>
</head>
<body>
    <div class="tabs">
        <button class="tab-button active" onclick="showTab('signup')">Signup</button>
        <button class="tab-button" onclick="showTab('contact')">Contact Us</button>
    </div>

    <!-- Signup Form -->
    <div class="form-container active" id="signup-form">
        <h2>Signup</h2>
        <form method="POST" action="/">
            <input type="text" name="signup_name" placeholder="Enter your name" value="{{ signup_name }}" required>
            <input type="email" name="signup_email" placeholder="Enter your email" value="{{ signup_email }}" required>
            <input type="submit" value="Signup">
        </form>
        {% if signup_msg %}
            <div class="message">{{ signup_msg }}</div>
        {% endif %}
    </div>

    <!-- Contact Us Form -->
    <div class="form-container" id="contact-form">
        <h2>Contact Us</h2>
        <form method="POST" action="/contact">
            <input type="text" name="contact_name" placeholder="Enter your name" value="{{ contact_name }}" required>
            <input type="email" name="contact_email" placeholder="Enter your email" value="{{ contact_email }}" required>
            <textarea name="contact_query" placeholder="Your query..." required>{{ contact_query }}</textarea>
            <input type="submit" value="Submit">
        </form>
        {% if contact_msg %}
            <div class="message">{{ contact_msg }}</div>
        {% endif %}
    </div>

    <script>
        function showTab(tab) {
            const signupForm = document.getElementById('signup-form');
            const contactForm = document.getElementById('contact-form');
            const tabButtons = document.querySelectorAll('.tab-button');

            if (tab === 'signup') {
                signupForm.classList.add('active');
                contactForm.classList.remove('active');
                tabButtons[0].classList.add('active');
                tabButtons[1].classList.remove('active');
            } else {
                contactForm.classList.add('active');
                signupForm.classList.remove('active');
                tabButtons[1].classList.add('active');
                tabButtons[0].classList.remove('active');
            }
        }
    </script>
</body>
</html>
"""

# Route: Signup Page
@app.route("/", methods=["GET", "POST"])
def signup():
    signup_msg = ""
    name = email = ""
    if request.method == "POST":
        name = request.form["signup_name"]
        email = request.form["signup_email"]
        signup_collection.insert_one({"name": name, "email": email})
        signup_msg = "✅ Signup successful!"
    return render_template_string(template,
                                  signup_msg=signup_msg,
                                  contact_msg="",
                                  signup_name=name,
                                  signup_email=email,
                                  contact_name="",
                                  contact_email="",
                                  contact_query="")

# Route: Contact Us
@app.route("/contact", methods=["POST"])
def contact():
    contact_msg = ""
    name = request.form["contact_name"]
    email = request.form["contact_email"]
    query = request.form["contact_query"]
    contact_collection.insert_one({"name": name, "email": email, "query": query})
    contact_msg = "📩 Query submitted successfully!"
    return render_template_string(template,
                                  signup_msg="",
                                  contact_msg=contact_msg,
                                  signup_name="",
                                  signup_email="",
                                  contact_name=name,
                                  contact_email=email,
                                  contact_query=query)

# Run the Flask app
if __name__ == "__main__":
    app.run(debug=True)
