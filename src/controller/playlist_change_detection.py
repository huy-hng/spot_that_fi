from helpers.data_types import LivePlaylistType
from src.api_handler import sp
from src.database.db_playlists import get_playlist_snapshot_id, update_playlist_snapshot


def has_playlist_changed(playlist: LivePlaylistType):
	current_snapshot = playlist.snapshot_id
	previous_snapshot = get_playlist_snapshot_id(playlist.id)
	return previous_snapshot != current_snapshot

def changed_playlists():
	playlists = sp.get_all_playlists()
	changed = []
	for playlist in playlists:
		if has_playlist_changed(playlist):
			changed.append(playlist.id)

	return changed
		