import json

from .features.archiver import Archiver
from .playlists import Playlists
from .data_types import ArchivePlaylistType

class ChangeDetector:
	def __init__(self, live_playlists: Playlists):
		self.live_playlists = live_playlists
		with open('./playlists.json') as f:
			self.tracked_playlists: list[ArchivePlaylistType] = json.load(f)
			
	def check_for_changes(self):
		# TODO: think about using an event handler here
		for playlist in self.tracked_playlists:
			if self._has_changed(playlist['snapshot_id'], playlist['current']):
				print(f'{playlist["name"]} has changed')
				# archiver = Archiver(self.live_playlists, playlist)
				# archiver.on_update()

	def _has_changed(self, current_snapshot: str, uri: str):
		live = self.live_playlists.get_by_uri(uri)
		return current_snapshot != live.snapshot_id
