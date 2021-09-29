from src import sp
from src.playlists.live_playlists import LivePlaylists
from src.tracks import Tracks


live_playlists = LivePlaylists()
big_playlist = live_playlists.get_by_name('Strong All')

def get_tracks_via_generator():
	generator = sp.get_tracks_generator(
			big_playlist.uri, big_playlist.tracks_in_playlist)

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
