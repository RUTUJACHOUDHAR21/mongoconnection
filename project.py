from flask import Flask, request, render_template_string
from pymongo import MongoClient

app = Flask(__name__)

# MongoDB Atlas URI
uri = "mongodb+srv://rutu:1234@project.itbfimp.mongodb.net/project?retryWrites=true&w=majority&appName=project"
client = MongoClient(uri)

# Connect to DB and Collection
db = client["test_database"]
collection = db["test_collection"]

# HTML Template for Signup
signup_form = """
<!DOCTYPE html>
<html>
<head>
    <title>Signup Form</title>
    <style>
        body {
            background: #f4f4f4;
            font-family: Arial, sans-serif;
            display: flex;
            justify-content: center;
            align-items: center;
            height: 100vh;
            margin: 0;
        }
        .form-container {
            background: white;
            padding: 30px 40px;
            border-radius: 12px;
            box-shadow: 0 8px 20px rgba(0, 0, 0, 0.1);
            text-align: center;
        }
        h2 {
            margin-bottom: 20px;
            color: #333;
        }
        input[type="text"], input[type="email"] {
            width: 100%;
            padding: 12px;
            margin: 10px 0 20px;
            border: 1px solid #ccc;
            border-radius: 6px;
            font-size: 16px;
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
    <div class="form-container">
        <h2>Signup</h2>
        <form method="POST">
            <input type="text" name="name" placeholder="Enter your name" required>
            <input type="email" name="email" placeholder="Enter your email" required>
            <input type="submit" value="Signup">
        </form>
        {% if message %}
            <div class="message">{{ message }}</div>
        {% endif %}
    </div>
</body>
</html>
"""

# Route: Signup Page
@app.route("/", methods=["GET", "POST"])
def signup():
    message = ""
    if request.method == "POST":
        name = request.form["name"]
        email = request.form["email"]

        # Insert into MongoDB
        collection.insert_one({"name": name, "email": email})
        message = "Signup successful!"

    return render_template_string(signup_form, message=message)

# Run the Flask app
if __name__ == "__main__":
    app.run(debug=True)
