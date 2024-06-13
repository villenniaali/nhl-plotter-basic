import os
import sys
import requests
import json
import matplotlib.pyplot as plt

def plot_shots(shots_locations, team_name, shot_type):
    x = [shot[0] for shot in shots_locations]
    y = [shot[1] for shot in shots_locations]
    colors = {'missed-shot': 'red', 'blocked-shot': 'orange', 'shot-on-goal': 'yellow', 'goal': 'green'}
    plt.scatter(x, y, c=colors[shot_type], label=f'{team_name} - {shot_type.capitalize()}')

game_id = sys.argv[1]

url = f'https://api-web.nhle.com/v1/gamecenter/{game_id}/play-by-play'
response = requests.get(url)

if response.status_code == 200:
    try:
        play_by_play_data = response.json()

        home_shots = {'missed-shot': [], 'blocked-shot': [], 'shot-on-goal': [], 'goal': []}
        away_shots = {'missed-shot': [], 'blocked-shot': [], 'shot-on-goal': [], 'goal': []}
        for event in play_by_play_data['plays']:
            event_type = event['typeDescKey'].lower()
            if event_type in ['shot-on-goal', 'blocked-shot', 'missed-shot', 'goal']:
                team_id = event['details']['eventOwnerTeamId']
                x = event['details'].get('xCoord', None)
                y = event['details'].get('yCoord', None)
                if x is not None and y is not None:
                    if team_id == play_by_play_data['homeTeam']['id']:
                        home_shots[event_type].append((x, y))
                    elif team_id == play_by_play_data['awayTeam']['id']:
                        away_shots[event_type].append((x, y))

        plt.figure(figsize=(10, 6))
        for shot_type, shots in home_shots.items():
            plot_shots(shots, play_by_play_data['homeTeam']['name']['default'], shot_type)
        for shot_type, shots in away_shots.items():
            plot_shots(shots, play_by_play_data['awayTeam']['name']['default'], shot_type)

        plt.xlabel('X Coordinate')
        plt.ylabel('Y Coordinate')
        plt.title('Shot Locations')
        plt.legend()
        plt.grid(True)
        plt.xlim(-100, 100)
        plt.ylim(-42.5, 42.5)
        plt.gca().set_aspect('equal', adjustable='box')
        
        output_folder = 'static/plots'
        os.makedirs(output_folder, exist_ok=True)
        plt.savefig(os.path.join(output_folder, f'plot_{game_id}.png'))

    except json.JSONDecodeError:
        print("Error: Could not decode the JSON response")
else:
    print("Error: Received a non-success status code")
