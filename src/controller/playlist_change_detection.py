from helpers.data_types import SpotifyPlaylistType
from src.api_handler import sp
import db


def has_playlist_changed(playlist: SpotifyPlaylistType):
	current_snapshot = playlist.snapshot_id
	previous_snapshot = db.playlists.get_playlist_snapshot_id(playlist.id)
	return previous_snapshot != current_snapshot

def changed_playlists() -> list[SpotifyPlaylistType]:
	playlists = sp.get_all_playlists()
	changed: list[SpotifyPlaylistType] = []
	for playlist in playlists:
		if has_playlist_changed(playlist):
			changed.append(playlist)

	return changed

def update_playlist(playlist: SpotifyPlaylistType):
	db.playlists.update_playlist_snapshot()


def update_all_playlists(playlists: list[SpotifyPlaylistType]):
	for playlist in playlists:
		update_playlist(playlist)
