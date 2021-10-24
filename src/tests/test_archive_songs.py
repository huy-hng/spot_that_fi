from src.tracks import Tracks
from src.playlists.live_playlists import LivePlaylists
from src.playlists.tracked_playlists import TrackedPlaylists
from src.features.archiver import Archiver

# get x amount of track ids that exceeds archive amount
	# and safe them locally in code

# consider correct output, when x amount of tracks is the stragey,
	# the correct output should be the playlist track ids with
	# the correct length and correct ids, which can be taken from prev todo

# compare actual output and correct output


track_ids = ['13KLstO6ywva9h94FOqpeW', '2xeW5CIB5XHkaDLYEFOSjs', '5PF2WtSZV4EtmGx4oER1zt', '2VvohoUXfl1dW6gM1UHPvK', '0HX7Qdf2R0pfeDueFpF6C4', '3Yojk6oNOGZGlxMrYXsaJh', '3A6WcOcwVB3dFZppYvlEvi', '0euC0zrWPMPACwjnyulC6l', '6WoloXr2PXu8FRYZFtzbij', '4qDVck33icBULgnvP6WmPh', '6CRrPTcxzM4pIO29GJF7Nk', '2KnuaZYoGzDoHiBTNYOTXG', '0FfqyjhB6Kspvit1oOo7ax', '2EZemIRw1LnIUM7YoiKWPQ', '7r8SEXh79XwN1tmOG2dbxN', '4dDEkdgT6gLXG1VSI0Qgtq', '02zYabT1FTwMy8byKpd40O', '6XR59BEFC1Z2kQ7PayDNPj', '7u2PsDpp4FdXsbn4sTh6MY', '5EMGQPQI60jvyDjKT2Fn2I', '6rSUrh8ErKSKfbH0t0IzCM', '6UdoWvHXqS0T4j0qCFFxBl', '0VMmHFqENPTDq3lHafvOPt', '2hNBhYGXQbq9KHYvK2itFY', '7x0vY5vTKzxMqozQWCj8Nd', '6dquCx5KAW5jCgGgoTlghL', '1IY1Ge6tFl0m9pr2Yg0OFe', '4jPr49jXRJHftXlwTEA2w4', '7kTlyuaUciX2wQx7ogrd9w', '3j57f5yEpiLZYgkcA1GKjc', '7B76OJ0ExVlSkDh1xelvRl', '2aLH4EiEoZLpbeEQvTBbtH', '1USo158Kncaxfyq9q306dn', '0DXZHcAQAkXx8YlMIdzqgG', '7ycZN2o5PMNuTkUg2Q73wN', '0dNN5wjTkbJnQkOnzh9WUH', '6xS02EfbvnneFWCM90PJFG', '69jstgacdd40OwG9cLl45r', '3wdkrgUEyjhUSNSMV7cWgP', '2hmn4VOZepYRxdw7vKyagU', '6OZ3FzEORUBi1lvU4EfypC', '4jTnSGGfLpQTiORJxYxy65', '0HCFZGK3c1TQorbyPHcj1l', '74ZQkrS93fcV6fcRYxqjjK', '41RrVUJeCOVsBmjUM2sdQs', '0JL7DoEqAUcOntWmBuOSdh', '3TtxaSTGwLOyWNA73lPioY', '3p9zEhikB0h8QF3YbfNUcM', '1eBaPBwmO4HOqc7Kk9D9qg', '4u45ry45w5m8fHbKX9ZCzw', '24qTFQSTSe3cac6LAgBuC4', '410rGaFDJPwjsr9m9RPCkz', '6PcDDuSAPG1AE1wefg6Y7D', '7fWmftb04n0GsxEjezNhXt', '4NpJL7yrDXaL5OGhvcPSi3']

def get_track_ids():
	playlists = LivePlaylists()
	calm = playlists.get_by_name('Calm All')

	tracks = calm.get_latest_tracks(55)
	tracks.reverse()
	return Tracks.get_ids(tracks)


def replace_tracks(playlist_name: str, track_ids: list[str]):
	playlists = LivePlaylists()
	playlist = playlists.get_by_name(playlist_name)
	playlist.replace_tracks(track_ids)


def test_archive():
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
	



