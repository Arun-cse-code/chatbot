from flask import Flask, request, jsonify
from flask_cors import CORS
import google.generativeai as genai
import os

app = Flask(__name__)
CORS(app, resources={r"/chat": {"origins": "*"}})  # Allow all frontend requests

# Store your API key in an environment variable for security
GOOGLE_API_KEY = "AIzaSyB2MuaUxllKLDMeltAsVjPy_-xa6fRZnY4"  # Replace with your actual key
genai.configure(api_key=GOOGLE_API_KEY)

# Built-in FAQ Data
faq = {
    "admission requirements": "To apply, you need to have passed your 12th-grade exams with a minimum of 60%.",
    "working hours": "The university is open from 9 AM to 5 PM on weekdays.",
    "scholarships": "You can apply for scholarships via the university's portal during the admissions process.",
    "computer science courses": "The Computer Science department offers B.Tech, M.Tech, and Ph.D. programs.",
    "campus facilities": "The campus offers state-of-the-art labs, a library, sports facilities, and hostels.",
    "faculty contact": "You can find faculty contact information on the university's official website."
}

# Function to get chatbot response from Gemini
def get_gemini_response(user_message):
    try:
        model = genai.GenerativeModel("gemini-pro")
        response = model.generate_content(user_message)
        return response.text.strip()
    except Exception as e:
        return f"Error: {str(e)}"

# API Endpoint for Chatbot
@app.route("/chat", methods=["POST"])
def chat():
    user_message = request.json.get("message").strip().lower()  # Get message from frontend

    # Check if the message matches any FAQ
    if user_message in faq:
        bot_response = faq[user_message]  # Provide FAQ answer
    else:
        bot_response = get_gemini_response(user_message)  # Get response from Gemini if no FAQ match

    return jsonify({"response": bot_response})  # Return JSON response

# Run Flask Server
if __name__ == "__main__":
    app.run(debug=True)
