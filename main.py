import json
import os
import statistics
from flask import Flask, render_template, send_from_directory

def extract_json_from_rofl(file_name):
  with open(file_name, 'rb') as file:
    content = file.read()
    brace_stack = []
    start_idx = None
    end_idx = None
    for idx, byte in enumerate(content):
      if byte == ord('{'):
        brace_stack.append(idx)
        if start_idx is None:
          start_idx = idx
      elif byte == ord('}'):
        if brace_stack:
          brace_stack.pop()
          if not brace_stack:
            end_idx = idx
            break
    if start_idx is not None and end_idx is not None:
      json_bytes = content[start_idx:end_idx + 1]
      try:
        json_str = json_bytes.decode('utf-8', 'ignore')
        json_object = json.loads(json_str)
        return json_object
      except json.JSONDecodeError as e:
        print(f"Error decoding JSON: {e}")
    return None

def save_json(data, file_path):
  with open(file_path, 'w') as json_file:
    json.dump(data, json_file, indent=2)
  print(f"File saved successfully at {file_path}")

def process_replays(replays_folder, json_folder):
  if not os.path.exists(json_folder):
    os.makedirs(json_folder)
  for file_name in os.listdir(replays_folder):
    if file_name.endswith(".rofl"):
      file_path = os.path.join(replays_folder, file_name)
      json_data = extract_json_from_rofl(file_path)
      json_data = process_json(json_data)
      if json_data:
        json_file_name = os.path.splitext(file_name)[0] + ".json"
        json_file_path = os.path.join(json_folder, json_file_name)
        save_json(json_data, json_file_path)
      else:
        print(f"The file {file_name} could not be processed.")

def process_json(json_data):
  stats_json_str = json_data["statsJson"]
  stats_json = json.loads(stats_json_str)
  simplified_data_map = simplify_json(stats_json)
  new_json = {
    "timestamp": json_data["gameLength"],
    "data": simplified_data_map
  }
  return new_json

def simplify_json(participants):
  simplified_data_map = {}
  with open('./info/players.json', 'r') as file:
    players = json.load(file)

  ignore_players = set()
  for player, data in players.items():
    for combination in data['combinationToIgnore']:
      if all(any(participant.get('SKIN', '') == champion for participant in participants) for champion in combination.values()):
        ignore_players.add(player)
        break

  for participant in participants:
    name = participant.get('NAME', '')
    player = None
    for key, value in players.items():
      if name in value['aliases']:
        player = key
        break

    if player and player not in ignore_players:
      simplified_data = {}

      time_played = int(participant.get('TIME_PLAYED', 1))
      minions_killed = int(participant.get('MINIONS_KILLED', 0))
      neutral_minions_killed = int(participant.get('NEUTRAL_MINIONS_KILLED', 0))
      simplified_data['CSPM'] = round((minions_killed + neutral_minions_killed) / (time_played / 60), 2)
      simplified_data['GDPM'] = round(int(participant.get('GOLD_EARNED', 0)) / (time_played / 60), 2)
      simplified_data['DPM'] = round(int(participant.get('TOTAL_DAMAGE_DEALT_TO_CHAMPIONS', 0)) / (time_played / 60), 2)
      kda_ratio = (int(participant.get('CHAMPIONS_KILLED', 0)) + int(participant.get('ASSISTS', 0))) / max(int(participant.get('NUM_DEATHS', 1)), 1)
      simplified_data['KDA'] = round(kda_ratio, 2)
      kp_percentage = (int(participant.get('CHAMPIONS_KILLED', 0)) + int(participant.get('ASSISTS', 0))) / max(int(participant.get('CHAMPIONS_KILLED', 0)) + int(participant.get('NUM_DEATHS', 0)) + int(participant.get('ASSISTS', 0)), 1) * 100
      simplified_data['KP%'] = round(kp_percentage, 2)
      simplified_data['visionScore'] = int(participant.get('VISION_SCORE', 0))

      simplified_data_map[player] = simplified_data

  return simplified_data_map

def process_json_files(json_folder):
  player_data = {}

  for file_name in os.listdir(json_folder):
    if file_name.endswith(".json"):
      file_path = os.path.join(json_folder, file_name)
      with open(file_path, 'r') as json_file:
        data = json.load(json_file)
        for player, stats in data['data'].items():
          if player not in player_data:
            player_data[player] = {
              'CSPM': [],
              'GDPM': [],
              'DPM': [],
              'KDA': [],
              'KP%': [],
              'visionScore': []
            }
          player_data[player]['CSPM'].append(stats['CSPM'])
          player_data[player]['GDPM'].append(stats['GDPM'])
          player_data[player]['DPM'].append(stats['DPM'])
          player_data[player]['KDA'].append(stats['KDA'])
          player_data[player]['KP%'].append(stats['KP%'])
          player_data[player]['visionScore'].append(stats['visionScore'])

    return player_data

def generate_summary(player_data):
  summary = {
    'players': []
  }
  for player, stats in player_data.items():
    player_summary = {
      'name': player,
      'total_games': len(stats['CSPM']),
      'stats': {
        'avg_CSPM': round(statistics.mean(stats['CSPM']), 2),
        'avg_GDPM': round(statistics.mean(stats['GDPM']), 2),
        'avg_DPM': round(statistics.mean(stats['DPM']), 2),
        'avg_KDA': round(statistics.mean(stats['KDA']), 2),
        'avg_KP%': round(statistics.mean(stats['KP%']), 2),
        'avg_visionScore': round(statistics.mean(stats['visionScore']), 2)
      },
      'performance': {}
    }
    for metric in ['CSPM', 'GDPM', 'DPM', 'KDA', 'KP%', 'visionScore']:
      player_summary['performance'][metric] = {
        'highest': round(max(stats[metric]), 2),
        'lowest': round(min(stats[metric]), 2),
        'average': round(statistics.mean(stats[metric]), 2),
        'SD': round(statistics.stdev(stats[metric]), 2) if len(stats[metric]) > 1 else 0.0
      }
    summary['players'].append(player_summary)
  return summary

def save_summary(summary, file_path):
  with open(file_path, 'w') as json_file:
    json.dump(summary, json_file, indent=2)
  print(f"Summary saved successfully at {file_path}")

summary_file_path = "./static/summary.json"
replays_folder = "./replays"
json_folder = "./data"
process_replays(replays_folder, json_folder)

player_data = process_json_files(json_folder)
summary = generate_summary(player_data)
save_summary(summary, summary_file_path)

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/js/<path:path>')
def send_js(path):
    return send_from_directory('static/js', path)

@app.route('/css/<path:path>')
def send_css(path):
    return send_from_directory('static/css', path)

if __name__ == '__main__':
    app.run(debug=True)