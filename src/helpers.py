import json

def write_dict_to_file(name: str, data):
	with open(f'./data/{name}.json', 'w') as f:
		f.write(json.dumps(data, indent=2))

def read_dict_from_file(name: str):
	with open(f'./data/{name}.json') as f:
		json.load(f)

def get_track_ids(tracks):
	return [track['track']['id'] for track in tracks]

def get_track_names(tracks: list):
	return [track['track']['name'] for track in tracks]



def create_data_class(data: dict):
	for k,v in data.items():
		print(f'{k}: {type(v).__name__}')
		type_ = type(v).__name__
		if type_ == 'list':
			print('=============')
			create_data_class(v[0])
		elif type_ == 'dict':
			print('=============')
			create_data_class(v)

if __name__ == '__main__':
	with open('../data/playlists.json') as f:
		playlists = f.read()
	playlists = json.loads(playlists)
	create_data_class(playlists)
	