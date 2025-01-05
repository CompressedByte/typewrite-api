#-. .- - ..- .-. . / .. ... / -. --- - / -.-. .-. ..- . .-.. .-.-.#

from flask import Flask, request, jsonify
import g4f
import asyncio
import json
import os
import g4f.Provider

app = Flask(__name__)

# Path where player data will be stored
players_data_path = "players_data"

# Create the directory if it doesn't exist
if not os.path.exists(players_data_path):
    os.makedirs(players_data_path)

# Function to load player data from the JSON file
def load_player_data(player_name):
    player_file = os.path.join(players_data_path, f"{player_name}.json")
    if os.path.exists(player_file):
        with open(player_file, 'r') as f:
            return json.load(f)
    return {"messages": []}  # Return an empty dict if no previous data

# Function to save player data to the JSON file
def save_player_data(player_name, data):
    player_file = os.path.join(players_data_path, f"{player_name}.json")
    with open(player_file, 'w') as f:
        json.dump(data, f, indent=4)

@app.route('/gpt_response', methods=['POST'])
def gpt_response():
    try:
        # Get the user's input (player)
        user_input = request.json.get('messages')
        player_name = request.json.get('player_name')

        if not user_input or not player_name:
            return jsonify({"error": "Player name or text not provided"}), 400

        # Load previous player data or create new if not exists
        player_data = load_player_data(player_name)

        # Add the player's message to their history
        player_data["messages"].append({"role": "user", "content": user_input})

        # Make the API call to AI model
        response = g4f.ChatCompletion.create(
            provider=g4f.Provider.Blackbox,
            model="claude-3.5-sonnet",
            messages=player_data["messages"],
            web_search=True
        )

        # Print the complete response from the API for debugging
        print("API Response: ", response)

        # In this case, the response is plain text
        content = response if isinstance(response, str) else "Response not found"

        # Save the updated player history
        player_data["messages"].append({"role": "assistant", "content": content})
        save_player_data(player_name, player_data)

        return jsonify({"response": content})

    except Exception as e:
        print("Error occurred: ", e)
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
