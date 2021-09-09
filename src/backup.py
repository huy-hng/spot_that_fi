# from playlist_handler import Playlists
from helpers import write_dict_to_file

# def backup_all_playlists(playlistsCls: Playlists):
def backup_all_playlists(playlistsCls):
	backups = []
	playlists = playlistsCls.playlists
	for playlist in playlists:
		tracks = playlist.get_latest_tracks(None)
		backups.append({
			'tracks': tracks,
			'name': playlist.name,
			'uri': playlist.uri,
			'snapshot_id': playlist.snapshot_id
		})
		break

	write_dict_to_file('backup', backups)

