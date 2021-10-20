import pytest

from src.playlists.live_playlists import LivePlaylists
from src import sp
from src.tracks import Tracks

playlists = LivePlaylists()
playlist = playlists.get_by_name('Playlist')
archive_playlist = playlists.get_by_name('Playlist Archive')

@pytest.fixture
def reset_playlists():
	# yield
	calm = playlists.get_by_name('Calm')
	tracks = calm.get_latest_tracks(51)
	track_ids = Tracks.get_ids(tracks)

	playlist.replace_tracks(track_ids)
	archive_playlist.replace_tracks([])
	return
