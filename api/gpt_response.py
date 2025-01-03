#-. .- - ..- .-. . / .. ... / -. --- - / -.-. .-. ..- . .-.. .-.-.#

import json
import g4f
import g4f.Provider

def handler(request):
    if request.method == 'POST':
        try:
            # Get user input
            user_input = request.json.get('messages')
            if not user_input:
                return json.dumps({"error": "Text not provided"}), 400

            # Call the AI model API
            response = g4f.ChatCompletion.create(
                provider=g4f.Provider.Blackbox,
                model="claude-3.5-sonnet",
                messages=[{"role": "user", "content": user_input}],
                web_search=True
            )

            # Print the full API response for debugging
            print("API Response: ", response)

            # In this case, the response is plain text
            content = response if isinstance(response, str) else "Response not found"

            return json.dumps({"response": content}), 200

        except Exception as e:
            print("Error occurred: ", e)
            return json.dumps({"error": str(e)}), 500

    else:
        # If the method is not POST, return an error
        return json.dumps({"error": "Method not allowed"}), 405
