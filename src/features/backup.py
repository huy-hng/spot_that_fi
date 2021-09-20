import json
from datetime import date

from src.playlists.live_playlists import LivePlaylists

def backup_all_playlists(playlistsCls: LivePlaylists):

	backups = []
	playlists = playlistsCls.playlists
	for playlist in playlists:

		if playlist.num_tracks > 1500:
			print(f'skipping {playlist.name} because too many songs')
			continue

		print(f'Backing {playlist.name} up with {playlist.num_tracks} tracks.')
		tracks = playlist.get_latest_tracks(None)
		backups.append({
			'tracks': tracks.ids,
			'name': playlist.name,
			'uri': playlist.uri,
			'snapshot_id': playlist.snapshot_id
		})

	create_backup_file(str(date.today()), backups)

def create_backup_file(name: str, data):
	with open(f'./backup/{name}.json', 'w') as f:
		f.write(json.dumps(data, indent=2))