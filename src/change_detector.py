import json
from enum import Enum

from .playlists import Playlists
from .data_types import TrackedPlaylistClusterType, TrackedPlaylistType

class PlaylistType(Enum):
	All = 'all'
	Snippet = 'snippet'
		
class ChangeDetector:
	def __init__(self, live_playlists: Playlists):
		self.live_playlists = live_playlists
		with open('./playlists.json') as f:
			self.tracked_clusters: list[TrackedPlaylistClusterType] = json.load(f)
			
	def check_for_changes(self):
		for cluster in self.tracked_clusters:
			if self._has_changed(cluster['snippet']):
				pass

			if self._has_changed(cluster['all']):
				pass


	def _has_changed(self, tracked: TrackedPlaylistType) -> bool:
		live = self.live_playlists.get_by_uri(tracked['uri'])
		return tracked['snapshot_id'] != live.snapshot_id