from src.api_handler import sp

def changed_playlists():
	playlists = sp.get_all_playlists()
	for playlist in playlists:
		current_snapshot = playlist.snapshot_id
		