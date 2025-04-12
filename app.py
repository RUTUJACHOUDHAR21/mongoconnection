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

# HTML Template with JS interactivity
template = """
<!DOCTYPE html>
<html>
<head>
    <title>Interactive Forms</title>
    <style>
        body {
            background: #f4f4f4;
            font-family: Arial, sans-serif;
            display: flex;
            flex-direction: column;
            align-items: center;
            height: 100vh;
            margin: 0;
            padding-top: 50px;
        }
        .form-container {
            background: white;
            padding: 30px 40px;
            border-radius: 12px;
            box-shadow: 0 8px 20px rgba(0, 0, 0, 0.1);
            text-align: center;
            width: 400px;
            margin-bottom: 30px;
        }
        h2 {
            margin-bottom: 20px;
            color: #333;
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
            animation: fadein 1s ease-in-out;
        }
        @keyframes fadein {
            from { opacity: 0; }
            to { opacity: 1; }
        }
    </style>
</head>
<body>
    <!-- Signup Form -->
    <div class="form-container">
        <h2>Signup</h2>
        <form method="POST" action="/" onsubmit="return validateSignupForm()">
            <input type="text" name="signup_name" placeholder="Enter your name" value="{{ signup_name }}" required>
            <input type="email" name="signup_email" placeholder="Enter your email" value="{{ signup_email }}" required>
            <input type="submit" value="Signup">
        </form>
        {% if signup_msg %}
            <div class="message">{{ signup_msg }}</div>
        {% endif %}
    </div>

    <!-- Contact Us Form -->
    <div class="form-container">
        <h2>Contact Us</h2>
        <form method="POST" action="/contact" onsubmit="return validateContactForm()">
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
        function validateSignupForm() {
            const name = document.querySelector('input[name="signup_name"]').value.trim();
            const email = document.querySelector('input[name="signup_email"]').value.trim();
            if (!name || !email) {
                alert("Please fill out all Signup fields.");
                return false;
            }
            return true;
        }

        function validateContactForm() {
            const name = document.querySelector('input[name="contact_name"]').value.trim();
            const email = document.querySelector('input[name="contact_email"]').value.trim();
            const query = document.querySelector('textarea[name="contact_query"]').value.trim();
            if (!name || !email || !query) {
                alert("Please fill out all Contact fields.");
                return false;
            }
            return true;
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
