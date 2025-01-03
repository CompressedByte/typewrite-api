#-. .- - ..- .-. . / .. ... / -. --- - / -.-. .-. ..- . .-.. .-.-.#

import json
from flask import Flask, request, jsonify
import g4f
import g4f.Provider

# Create a Flask application
app = Flask(__name__)

@app.route('/api/gpt_response', methods=['POST'])
def get_gpt_response():
    try:
        # Get the user's input from the request
        user_input = request.json.get('messages')
        if not user_input:
            return jsonify({"error": "Text not provided"}), 400

        # Make the API call to the AI model
        response = g4f.ChatCompletion.create(
            provider=g4f.Provider.Blackbox,
            model="claude-3.5-sonnet",
            messages=[{"role": "user", "content": user_input}],
            web_search=True
        )

        # Print the full response from the API for debugging purposes
        print("API Response: ", response)

        # Check if the response is a string
        content = response if isinstance(response, str) else "Response not found"

        return jsonify({"response": content})

    except Exception as e:
        print("Error occurred: ", e)
        return jsonify({"error": str(e)}), 500


# The handler function for Vercel, invoked by the platform
def handler(request):
    # Call the Flask app directly to handle the request
    return app(request)

