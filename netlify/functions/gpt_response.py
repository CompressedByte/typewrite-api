#-. .- - ..- .-. . / .. ... / -. --- - / -.-. .-. ..- . .-.. .-.-.#

import json
import os
import g4f
import g4f.Provider

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

# Main handler function for the Netlify function
def handler(event, context):
    try:
        # Get the request data (POST)
        body = json.loads(event['body'])
        user_input = body.get('messages')
        player_name = body.get('player_name')

        if not user_input or not player_name:
            return {
                'statusCode': 400,
                'body': json.dumps({"error": "Player name or text not provided"})
            }

        # Load previous player data or create new if not exists
        player_data = load_player_data(player_name)

        # Add the player's message to their history
        player_data["messages"].append({"role": "user", "content": user_input})

        # Make the API call to AI model
        response = g4f.ChatCompletion.create(
            provider=g4f.Provider.Blackbox,
            model="gpt-4",
            messages=player_data["messages"],
            web_search=True
        )

        # The response is plain text
        content = response if isinstance(response, str) else "Response not found"

        # Save the updated player history
        player_data["messages"].append({"role": "assistant", "content": content})
        save_player_data(player_name, player_data)

        return {
            'statusCode': 200,
            'body': json.dumps({"response": content})
        }

    except Exception as e:
        return {
            'statusCode': 500,
            'body': json.dumps({"error": str(e)})
        }
