import json

from src.playlist_handler import Playlists
from .data_types import TrackedPlaylistsType, TrackedPlaylistsTypeHelper

with open('./playlists.json') as f:
	tracked_playlists: list[TrackedPlaylistsType] = json.load(f)
	
def check_changes(live_playlists: Playlists):
	for tracked in tracked_playlists:
		if has_changed(tracked['snippet'], live_playlists):
			pass

		if has_changed(tracked['all'], live_playlists):
			pass


def has_changed(tracked: TrackedPlaylistsTypeHelper,
								live_playlists: Playlists) -> bool:
	live = live_playlists.get_by_uri(tracked['uri'])
	return (tracked['snapshot_id'] != live.snapshot_id)