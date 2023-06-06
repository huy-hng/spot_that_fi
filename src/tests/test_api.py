from src import api
from src.tests import PlaylistIDs

def test_get_playlist():
	playlist = api.get_playlist(PlaylistIDs.unchanged)

	assert playlist
	assert playlist.name == 'Playlist Unchanging'
	assert playlist.id == PlaylistIDs.unchanged

def test_get_all_playlists():
	playlists = api.get_all_playlists()

	assert playlists
