import pytest

from src.api_handler import sp
from src.playlists_deprecated.live_playlists import LivePlaylists
from src.api_handler.tracks import Tracks
from src.tests.fixtures import reset_playlists, track_ids_55

live_playlists = LivePlaylists()
big_playlist = live_playlists.get_by_name('Strong All')

def get_tracks_via_generator():
	generator = sp.get_playlist_tracks_generator(
			big_playlist.uri, big_playlist.total_tracks)

	tracks = []
	for batch in generator:
		tracks += batch
		# print(names)
	names = Tracks.get_names(tracks)
	print(len(names))
	

def get_tracks_with_live_playlist():
	# check if len is same as input
	tracks = big_playlist.get_latest_tracks(120)
	last_track = tracks[-1]
	name_last_track = Tracks.get_names([last_track])
	print(name_last_track)

def get_all_tracks_with_live_playlist():
	# check if length is correct and first and last song are also correct
	tracks = big_playlist.get_latest_tracks()
	print(len(tracks))


@pytest.mark.parametrize(['track_amount', 'expected'], [
	1, track_ids_55[len(track_ids_55)-1:],
	20, track_ids_55[len(track_ids_55)-20:],
	49, track_ids_55[len(track_ids_55)-49:],
	50, track_ids_55[len(track_ids_55)-50:],
	51, track_ids_55[len(track_ids_55)-51:],
	55, track_ids_55[len(track_ids_55)-55:]
])
def test_get_songs(track_amount, expected):
	# * fixture
	playlists = LivePlaylists()
	playlist = playlists.get_by_name('Playlist')
	playlist.replace_tracks(track_ids_55)

	tracks = playlist.get_latest_tracks(track_amount)
	ids = Tracks.get_ids(tracks)

	assert ids == expected