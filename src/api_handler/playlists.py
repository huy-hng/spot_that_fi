from typing import NamedTuple

from types.playlists import SpotifyPlaylistType
from settings.user_data import get_playlist_user_data


class SyncPairs(NamedTuple):
	main: SpotifyPlaylistType
	snippet: SpotifyPlaylistType

class Playlists:
	def __init__(self, playlists: list[SpotifyPlaylistType]):
		self.playlists = {playlist.id: playlist for playlist in playlists}

	def get_playlist_by_id(self, playlist_id: str):
		return self.playlists[playlist_id]

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
