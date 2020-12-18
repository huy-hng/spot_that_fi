import json

def get_playlist_data():
	with open('../playlists.json') as f:
		return json.load(f)
def set_playlist_data(playlists_data):
	with open('../playlists.json', 'w') as f:
		f.write(json.dumps(playlists_data, indent=2))

def write_dict_to_file(name, data):
	with open(f'../{name}.json', 'w') as f:
		f.write(json.dumps(data, indent=2))
