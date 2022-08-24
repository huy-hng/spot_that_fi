from src.api_handler.tracks import Tracks
from src.playlists_deprecated.live_playlists import LivePlaylists
from src.playlists_deprecated.tracked_playlists import TrackedPlaylists
from features.archiver import Archiver

from src.tests.fixtures import track_ids, replace_tracks

def test_archive():
	""" 
	get x amount of track ids that exceeds archive amount
		and safe them locally in code

	consider correct output, when x amount of tracks is the stragey,
		the correct output should be the playlist track ids with
		the correct length and correct ids, which can be taken from prev todo

	compare actual output and correct output
	"""

	# * test variables
	playlist_length = 50

	# * fixture
	replace_tracks('Playlist', track_ids)
	replace_tracks('Playlist Archive', [])

	# * establish correct output
	correct_output = track_ids[5:]
	assert len(correct_output) == playlist_length

	# * actual test
	live_playlists = LivePlaylists()
	tracked_playlists = TrackedPlaylists(live_playlists)

	archiver = Archiver(tracked_playlists)
	archiver.check_for_changes(live_playlists)
	
	# * check if correct
	live_playlists.update_data()
	playlist = live_playlists.get_by_name('Playlist')
	playlist_tracks = playlist.get_latest_tracks(None)
	playlist_tracks.reverse()
	assert len(playlist_tracks) == playlist_length
	assert playlist_tracks == correct_output
