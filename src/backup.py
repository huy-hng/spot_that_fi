import json
from datetime import date

from src.playlist_handler import Playlists

def backup_all_playlists(playlistsCls: Playlists):
	# TODO: print progress

	backups = []
	playlists = playlistsCls.playlists
	for playlist in playlists:

		if playlist.num_tracks > 1500:
			print(f'skipping {playlist.name} because too many songs')
			continue

		tracks = playlist.get_latest_tracks(None)
		backups.append({
			'tracks': tracks.ids,
			'name': playlist.name,
			'uri': playlist.uri,
			'snapshot_id': playlist.snapshot_id
		})

	create_backup_file(date.today(), backups)

def create_backup_file(name: str, data):
	with open(f'./backup/{name}.json', 'w') as f:
		f.write(json.dumps(data, indent=2))