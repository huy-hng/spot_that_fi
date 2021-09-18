import json

from dataclasses import dataclass

from src.data_types import TrackedPlaylistType
from .live_playlists import LivePlaylist, LivePlaylists

@dataclass
class TrackedPlaylist:
	name: str
	snapshot_id: str
	current_uri: str
	archive_uri: str
	live_playlist: LivePlaylist

	def has_changed(self):
		return self.live_playlist.snapshot_id == self.snapshot_id

	def update_snapshot(self):
		# TODO
		pass


class TrackedPlaylists:
	def __init__(self, live_playlists: LivePlaylists):
		self.live_playlists = live_playlists
		self.tracked = []
		

	def load_data(self):
		with open('./data/tracked_playlist.json') as f:
			playlists: list[TrackedPlaylistType] = json.load(f)

		for playlist in playlists:
			name = playlist['name']
			current = playlist['current']
			archive = playlist['archive']
			snapshot_id = playlist['snapshot_id']
			live_playlist = self.live_playlists.get_by_uri(current)
			tracked = TrackedPlaylist(name, snapshot_id, current,
																archive, live_playlist)
			self.tracked.append(tracked)
