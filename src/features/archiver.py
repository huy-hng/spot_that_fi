from src.playlists.live_playlists import LivePlaylists

from src.playlists.tracked_playlists import TrackedPlaylists, TrackedPlaylist
from src.tracks import Tracks

class Archiver:
	"""
	Take the oldest songs from playlists that exceed the amount of tracks in
	a playlist, remove them, and put them into the corresponding archive playlist.

	This class doesnt know whether a playlist has changed or not,
	it archives the songs from current playlist
	"""

	def __init__(self, live_playlists: LivePlaylists,
										 tracked_playlists: TrackedPlaylists):
		self.live_playlists = live_playlists
		self.tracked_playlists = tracked_playlists

		self.tracks_amount = 50

	def check_for_changes(self):
		for tracked in self.tracked_playlists.tracked:
			live_playlist = self.live_playlists.get_by_uri(tracked.current_uri)
			if tracked.has_changed(live_playlist):
				self.on_update()


	def on_update(self, tracked_playlist: TrackedPlaylist):
		current_uri = tracked_playlist.current_uri
		archive_uri = tracked_playlist.archive_uri
		current_playlist = self.live_playlists.get_by_uri(current_uri)
		archive_playlist = self.live_playlists.get_by_uri(archive_uri)

		tracks = current_playlist.get_latest_tracks(None)

		if len(tracks) > self.tracks_amount:
			# one or more tracks were added to playlist
			archive_tracks = tracks.tracks[self.tracks_amount-1:]
			archive_playlist.add_tracks(archive_tracks)
			current_playlist.remove_tracks(archive_tracks)
			# TODO: check if order is correct

		elif len(tracks) < self.tracks_amount:
			# one or more songs were removed
			pass
		elif len(tracks) == self.tracks_amount:
			# an equivalent amount of songs were added and removed
			pass


	def calculate_playlist_length_with_duration(self):
		raise NotImplementedError()