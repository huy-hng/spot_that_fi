import time
import pytest

from src import sp
from src.playlists.live_playlists import LivePlaylists
from src.playlists.tracked_playlists import TrackedPlaylists
from src.tracks import Tracks
from src.features.archiver import Archiver
from src.tests.reset_playlists import reset_playlists

new_tracks = ["4M3wJczMgJmUsSg1Hy4p5D",
 							"4mQTPwMKPNLGODbonuGCtP",
 							"5F223mR6ZL7MQVDdt9ajdY",
 							"33Axn97y8NTI3EQfUkMtA4"]

@pytest.mark.usefixtures('reset_playlists')
def test_add_tracks_correctly(reset_playlists):
	live_playlists = LivePlaylists()
	playlist = live_playlists.get_by_name('Playlist')

	playlist_tracks = playlist.get_latest_tracks(None)
	playlist_track_ids = Tracks.get_ids(playlist_tracks)
	# playlist_tracks_ids.reverse()

	playlist.add_tracks_at_end(new_tracks)
	time.sleep(5)

	current_tracks = playlist.get_latest_tracks(None)
	current_track_ids = Tracks.get_ids(current_tracks)
	current_track_ids.reverse()

	expected = playlist_track_ids + new_tracks
	assert current_track_ids == expected

@pytest.mark.usefixtures('reset_playlists')
def test_archive_oldest_song(reset_playlists):

	live_playlists = LivePlaylists()
	playlist = live_playlists.get_by_name('Playlist')

	playlist.add_tracks_at_end(['4M3wJczMgJmUsSg1Hy4p5D'])
	live_playlists.update_data()
	tracked_playlists = TrackedPlaylists(live_playlists)

	archiver = Archiver(tracked_playlists)
	archiver.check_for_changes(live_playlists)
