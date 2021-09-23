from src.playlists.live_playlists import LivePlaylists

from src.playlists.tracked_playlists import TrackedPlaylists, TrackedPlaylist

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

		self.TRACKS_AMOUNT = 50
		self.DURATION = 3 * 60 * 60 # 3 hours


	def check_for_changes(self):
		for tracked in self.tracked_playlists.playlists:
			live_playlist = self.live_playlists.get_by_uri(tracked.current_uri)
			if tracked.has_changed(live_playlist):
				self.update()


	def update(self, tracked_playlist: TrackedPlaylist):
		current = self.live_playlists.get_by_uri(tracked_playlist.current_uri)
		archive = self.live_playlists.get_by_uri(tracked_playlist.archive_uri)

		tracks = current.get_latest_tracks(None)

		if len(tracks) > self.TRACKS_AMOUNT:
			# one or more tracks were added to playlist
			archive_tracks = tracks.tracks[self.TRACKS_AMOUNT-1:]

			archive.add_tracks_at_end(archive_tracks)
			current.remove_tracks(archive_tracks)

			# TEST: check if order is correct
			# TODO: no duplicates should be added

		elif len(tracks) < self.TRACKS_AMOUNT:
			# one or more songs were removed
			pass
		elif len(tracks) == self.TRACKS_AMOUNT:
			# an equivalent amount of songs were added and removed
			pass


	def calculate_playlist_length_with_duration(self):
		raise NotImplementedError()
