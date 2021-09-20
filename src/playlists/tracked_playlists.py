import json
from typing import Callable
from src.data_types import TrackedPlaylistType
from .live_playlists import LivePlaylist

class TrackedPlaylist:
	""" A class that handles the tracked playlist,
			including checking for changes
			as well as updating the snapshot_id in data """

	def __init__(self, tracked_playlist: TrackedPlaylistType,
										 update_snapshot: Callable):

		self.name = tracked_playlist['name']
		self.snapshot_id = tracked_playlist['snapshot_id']
		self.current_uri = tracked_playlist['current']
		self.archive_uri = tracked_playlist['archive']

		self.update_snapshot = update_snapshot


	def has_changed(self, live_playlist: LivePlaylist):
		""" compare the live snapshot_id with
		the one saved locally and check for differences """
		live_snapshot_id = live_playlist.snapshot_id

		changed = live_snapshot_id == self.snapshot_id

		if changed:
			self.update_snapshot(self.name, live_snapshot_id)
		return changed


class TrackedPlaylists:
	""" a class that loads the tracked_playlists and updates them """
	def __init__(self):
		self.FILE_LOCATION = './data/tracked_playlist.json'
		self.playlists: list[TrackedPlaylist] = []
		self.load_data()

	def load_data(self):
		playlists = self.read_file()

		for playlist in playlists:
			tracked = TrackedPlaylist(playlist, self.update_snapshot)
			self.playlists.append(tracked)

	def update_snapshot(self, playlist_name: str, snapshot_id: str):
		# TEST: if this behaves correctly
		for playlist in self.playlists:
			if playlist.name == playlist_name:
				playlist.snapshot_id = snapshot_id

		self.write_file()
		self.load_data()


	def write_file(self):
		with open(self.FILE_LOCATION, 'w') as f:
			f.write(self.playlists)

	def read_file(self) -> list[TrackedPlaylistType]:
		with open(self.FILE_LOCATION) as f:
			return json.load(f)
