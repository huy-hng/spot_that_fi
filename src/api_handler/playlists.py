from typing import NamedTuple

from src.api_handler import sp
from src.types.playlists import AllPlaylists, PlaylistTracksItem
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

class LivePlaylist:
	""" handles crud operations of a live playlist
	the methods shouldnt be complicated
	the bulk logic should be done by the api_handler \n

	This class doesn't save state, it just performs actions
	on the playlists on spotify.
	"""
	def __init__(self, playlist: AllPlaylists):
		self.uri = playlist.uri
		self.snapshot_id = playlist.snapshot_id
		self.name = playlist.name
		self._last_total_tracks = playlist.tracks.total

	@property
	def total_tracks(self):
		data = sp.get_one_playlist(self.uri)
		total_tracks = data.tracks.total
		self._last_total_tracks = total_tracks
		return total_tracks


	def get_latest_tracks(self, num_tracks: int=0) -> list[PlaylistTracksItem]:
		""" returns the latest n songs in playlist in added order.
		That means the latest added song is at the end of the list\n
		if num_songs == 0: return all songs in playlist """

		if num_tracks == 0 or num_tracks > self._last_total_tracks:
			num_tracks = self.total_tracks

		tracks: list[PlaylistTracksItem]  = []
		for playlist_tracks in sp.get_playlist_tracks_generator(self.uri):
			if len(tracks) + len(playlist_tracks.items_) > num_tracks:
				# TODO: remove hardcoded 100 below
				rest = num_tracks % 100
				tracks = playlist_tracks[rest:] + tracks
				break
			tracks = playlist_tracks.items_ + tracks

		return tracks

	def add_tracks_at_beginning(self, tracks: list[PlaylistTracksItem]):
		track_ids = self.get_ids(tracks)
		sp.add_tracks_at_beginning(self.uri, track_ids)

	def add_tracks_at_end(self, tracks: list[PlaylistTracksItem],
															add_duplicates: bool = False):
		""" this should behave like adding songs normally to a playlist.
				each song should be appended at the end of the playlist.\n
				That means, (tracks[-1]) should be the last song added.\n
				Or in other words the first song, that is in sorted
				by recently added."""

		# TODO: use add_duplicates to control if duplicates should be added

		track_ids = self.get_ids(tracks)
		sp.add_tracks_at_end(self.uri, track_ids, self.total_tracks)

	def remove_tracks(self, tracks: list[PlaylistTracksItem]):
		track_ids = self.get_ids(tracks)
		sp.remove_tracks(self.uri, track_ids)

	def replace_tracks(self, tracks: list[PlaylistTracksItem]):
		track_ids = self.get_ids(tracks)
		sp.replace_playlist_tracks(self.uri, track_ids)

	@staticmethod
	def get_ids(tracks: list[PlaylistTracksItem]) -> list[str]:
		if len(tracks) == 0:
			return []

		return [item.track.id for item in tracks]