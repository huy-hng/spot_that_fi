import json

with open('../data/playlists.json') as f:
	playlists = f.read()

playlists = json.loads(playlists)
playlist = playlists['items'][0]
for k,v in playlist.items():
	print(f'{k}: {type(v).__name__}')
