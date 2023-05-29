import time
import pytest

from src import api
from src.deprecated.live_playlists import LivePlaylists
from src.deprecated.tracked_playlists import TrackedPlaylists
from src.api import Tracks
from src.tests.conftest import replace_tracks, track_ids_55

new_tracks = ["4M3wJczMgJmUsSg1Hy4p5D",
 							"4mQTPwMKPNLGODbonuGCtP",
 							"5F223mR6ZL7MQVDdt9ajdY",
 							"33Axn97y8NTI3EQfUkMtA4"]

# @pytest.mark.usefixtures('reset_playlists')
def test_add_tracks_correctly():
	# * fixture
	replace_tracks('Playlist', track_ids_55)

	# * establish correct output
	correct_output = track_ids_55 + new_tracks

	# * actual test
	live_playlists = LivePlaylists()
	playlist = live_playlists.get_by_name('Playlist')

	playlist.add_tracks_at_end(new_tracks)
	time.sleep(2)

	live_playlists.update_data()
	current_tracks = playlist.get_latest_tracks(None)
	current_track_ids = Tracks.get_ids(current_tracks)

	assert current_track_ids == correct_output
