from src.playlists import LivePlaylists
from src.data_types import TrackedPlaylistType
from src.api_handler import sp
from src.tracks import Tracks

class Archiver:
	"""
	Take the oldest songs from a playlist that exceed the amount of tracks in
	a playlist, remove them, and put them into the corresponding archive playlist.

	This class doesnt know whether a playlist has changed or not,
	it archives the songs from current playlist
	"""

	def __init__(self, live_playlists: LivePlaylists,
										 playlist: TrackedPlaylistType):
		self.live_playlists = live_playlists
		self.playlist = playlist

		self.tracks_amount = 50


	def on_update(self):
		tracks = self.get_current_tracks()
		if len(tracks) > self.tracks_amount:
			# one or more tracks were added to playlist
			archive_tracks = tracks.tracks[self.tracks_amount-1:]
			sp.remove_tracks(self.playlist['current'], archive_tracks)
			sp.add_tracks_at_beginning(self.playlist['archive'], archive_tracks)
			# TODO: check if order is correct

		elif len(tracks) < self.tracks_amount:
			# one or more songs were removed
			pass
		elif len(tracks) == self.tracks_amount:
			# an equivalent amount of songs were added and removed
			pass


	def get_current_tracks(self):
		live_playlist = self.live_playlists.get_by_uri(self.playlist['current'])
		tracks = live_playlist.get_latest_tracks(None)
		return tracks


	def calculate_playlist_length_with_duration(self):
		raise NotImplementedError()