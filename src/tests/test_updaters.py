from src import api, db
from src.tests import PlaylistIDs
from src.updaters import playlist_updater

def test_update_playlist():
	playlists = api.PlaylistsManager()
	unchanged = playlists.get_by_id(PlaylistIDs.unchanged)
	diff = playlist_updater.update_playlist_tracks_in_db(unchanged)

