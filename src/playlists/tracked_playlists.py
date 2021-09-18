import json
from typing import Callable
from src.data_types import TrackedPlaylistType
from .live_playlists import LivePlaylist

class TrackedPlaylist:
	""" A class that handles the tracked playlist, including checking for changes
	as well as updating the snapshot_id in data """
	def __init__(self, tracked_playlist: dict, update_snapshot: Callable):
			self.name = tracked_playlist['name']
			self.snapshot_id = tracked_playlist['snapshot_id']
			self.current_uri= tracked_playlist['current']
			self.archive_uri= tracked_playlist['archive']
		

	def has_changed(self, live_playlist: LivePlaylist):
		""" compare the live snapshot_id with
		the one saved locally and check for differences """
		live_snapshot_id = live_playlist.snapshot_id

		changed: bool = live_snapshot_id == self.snapshot_id

		if changed:
			self.update_snapshot(self.name, live_snapshot_id)
		return changed


class TrackedPlaylists:
	""" a class that loads the tracked_playlists and updates them """
	def __init__(self):
		self.tracked = []
		

	def load_data(self):
		with open('./data/tracked_playlist.json') as f:
			playlists: list[TrackedPlaylistType] = json.load(f)

		for playlist in playlists:
			tracked = TrackedPlaylist(playlist, self.update_snapshot)
			self.tracked.append(tracked)

	def update_snapshot(self, playlist_name: str, snapshot_id: str):
		raise NotImplementedError()
