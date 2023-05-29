from src.deprecated.live_playlists import LivePlaylists
from src.api import Tracks, DurationScale
from src.deprecated.tracked_playlists import TrackedPlaylists, TrackedPlaylist

class Archiver:
	"""
	Take the oldest songs from playlists that exceed the amount of tracks in
	a playlist, remove them, and put them into the corresponding archive playlist.

	This class doesnt know whether a playlist has changed or not,
	it archives the songs from current playlist
	"""

	def __init__(self, tracked_playlists: TrackedPlaylists):
		self.tracked_playlists = tracked_playlists

		self.TRACKS_AMOUNT = 50
		self.DURATION_IN_MINUTES = 3 * 60 # 3 hours


	def check_for_changes(self, live_playlists: LivePlaylists):
		# todo: refactor out logic, this function does too much
		self.live_playlists = live_playlists
		for _, tracked in self.tracked_playlists.playlists.items():
			live_playlist = self.live_playlists.get_by_uri(tracked.current_uri)
			if tracked.has_changed(live_playlist):
				self._update(tracked)


	def _update(self, tracked_playlist: TrackedPlaylist):
		current = self.live_playlists.get_by_uri(tracked_playlist.current_uri)
		archive = self.live_playlists.get_by_uri(tracked_playlist.archive_uri)

		tracks = current.get_latest_tracks(0)
		archive_tracks = self.tracks_to_archive_by_amount(tracks)

		if len(archive_tracks) == 0:
			return

		archive.add_tracks_at_end(archive_tracks)
		current.remove_tracks(archive_tracks)

	# : check if order is correct
	# : no duplicates should be added

	def tracks_to_archive_by_amount(self, tracks: list):
		if len(tracks) > self.TRACKS_AMOUNT:
			return tracks[:self.TRACKS_AMOUNT]
		return []

	def tracks_to_archive_by_duration(self, tracks: list):
		""" if current_duration > self.DURATION
				remove last item in tracks and put it in archive_tracks
				until current_duration <= self.DURATION """
		archive_tracks = []
		current_duration = Tracks.get_duration(tracks, DurationScale.MINUTES)
		while current_duration > self.DURATION_IN_MINUTES:
			archive_track = tracks.pop(-1)
			archive_tracks.append(archive_track)
			current_duration = Tracks.get_duration(tracks, DurationScale.MINUTES)

		return archive_tracks