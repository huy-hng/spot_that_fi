import json
from typing import Callable
from src.helpers.data_types import TrackedPlaylistType
from .live_playlists import LivePlaylist, LivePlaylists

class TrackedPlaylist:
	""" A class that handles the tracked playlist,
			including checking for changes
			as well as updating the snapshot_id in data """

	def __init__(self, tracked_playlist: TrackedPlaylistType,
										 update_snapshot: Callable):

		self.name = tracked_playlist.name
		self.snapshot_id = tracked_playlist.snapshot_id
		self.current_uri = tracked_playlist.current
		self.archive_uri = tracked_playlist.archive

		self.update_snapshot = update_snapshot


	def has_changed(self, live_playlist: LivePlaylist):
		""" compare the live snapshot_id with
		the one saved locally and check for differences """
		live_snapshot_id = live_playlist.snapshot_id

		changed = live_snapshot_id != self.snapshot_id

		if changed:
			self.update_snapshot(self.name, live_snapshot_id)
		return changed


	def __dict__(self) -> TrackedPlaylistType:
		return {
			'name': self.name,
			'current': self.current_uri,
			'archive': self.archive_uri,
			'snapshot_id': self.snapshot_id
		}


class TrackedPlaylists:
	""" a class that loads the tracked_playlists and updates them """
	def __init__(self, live_playlists: LivePlaylists):
		self.live_playlists = live_playlists

		# self.FILE_LOCATION = '/home/huy/repositories/spot_that_fi/data/tracked_playlists.json'
		self.FILE_LOCATION = './data/tracked_playlists.json'
		self.playlists: dict[str, TrackedPlaylist] = {}
		self.load_data()


	def get_playlist(self, name: str):
		return self.playlists[name]


	def load_data(self):
		playlists = self.read_file()

		for playlist in playlists:
			try: 
				name = playlist['name']
				current_uri = playlist['current']
				archive_uri = playlist['archive']
				self.check_existence(current_uri, name)
				self.check_existence(archive_uri, name + ' Archive')
			except ValueError as e:
				raise e

			tracked = TrackedPlaylist(playlist, self.update_snapshot)
			self.playlists[playlist['name']] = tracked


	def update_snapshot(self, playlist_name: str, snapshot_id: str):
		# TEST: if this behaves correctly
		playlist = self.playlists[playlist_name]
		playlist.snapshot_id = snapshot_id

		self.write_file()
		self.load_data()
		# TODO check if this behaves correctly
		# FIX this might be a race condition


	def write_file(self):
		data = self.convert_playlists_to_json()
		with open(self.FILE_LOCATION, 'w') as f:
			f.write(data)

	def read_file(self) -> list[TrackedPlaylistType]:
		with open(self.FILE_LOCATION) as f:
			return json.load(f)


	def check_existence(self, uri: str, name: str):
		try:
			live_playlist = self.live_playlists.get_by_uri(uri)
		except ValueError:
			raise ValueError(f'Playlist URI not found. {name}')
		else:
			if name != live_playlist.name:
				raise ValueError(f'live playlist name doesnt match json. {name}')


	def convert_playlists_to_json(self):
		# FIX theres a better way to do this
		json_list = []
		for name, tracked in self.playlists.items():
			json_list.append(tracked.__dict__())

		return json.dumps(json_list)