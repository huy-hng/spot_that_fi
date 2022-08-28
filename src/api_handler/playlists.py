from typing import NamedTuple

from src.types.playlists import AllPlaylists
from src.settings.user_data import get_playlist_user_data


class SyncPairs(NamedTuple):
	main: AllPlaylists
	snippet: AllPlaylists


class Playlists:
	def __init__(self, playlists: list[AllPlaylists]):
		self.playlists = playlists

		# for easier lookup
		self.names: dict[str, int] = {}
		self.ids: dict[str, int] = {}

		for index, playlist in enumerate(playlists):
			self.names[playlist.name] = index
			self.ids[playlist.id] = index


	def get_playlist_by_id(self, playlist_id: str):
		index = self.ids.get(playlist_id)
		if index is None:
			raise ValueError('Playlist id does not exist.')

		return self.playlists[index]


	def get_by_name(self, name: str):
		index = self.names.get(name)
		if index is None:
			raise Exception('Playlist Name does not exist.')

		return self.playlists[index]


	def get_sync_pairs(self) -> list[SyncPairs]:
		# read pairs from some file
		pairs: list[SyncPairs] = []
		playlist_data = get_playlist_user_data()
		snippet_data = playlist_data['snippet_playlist']

		for data in snippet_data:
			"""
			TODO: data['main_uri'] needs some type checking, wether its a uri
			or id. Also think about if I want to have it checked before hand
			so its garantueed.
			"""
			main_playlist = self.get_playlist_by_id(data['main_uri'])
			snippet_playlist = self.get_playlist_by_id(data['snippet_uri'])
			pair = SyncPairs(main_playlist, snippet_playlist)
			pairs.append(pair)

		return pairs
