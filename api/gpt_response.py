#-. .- - ..- .-. . / .. ... / -. --- - / -.-. .-. ..- . .-.. .-.-.#

from flask import Flask, request, jsonify
import g4f
import g4f.Provider

app = Flask(__name__)

@app.route('/get_gpt_response', methods=['POST'])
def get_gpt_response():
    try:
        # Get the user's input
        user_input = request.json.get('messages')
        if not user_input:
            return jsonify({"error": "Text not provided"}), 400

        # Make the API call to AI MODEL
        response = g4f.ChatCompletion.create(
            provider=g4f.Provider.Blackbox,
            model="claude-3.5-sonnet",
            messages=[{"role": "user", "content": user_input}],
            web_search=True
        )

        # Print the complete response from the API for debugging
        print("API Response: ", response)

        # In this case, response is already plain text.
        content = response if isinstance(response, str) else "Response not found"

        return jsonify({"response": content})

    except Exception as e:
        print("Error occurred: ", e)
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
