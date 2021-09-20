import math
from typing import Union

from src.tracks import Tracks
from src.data_types import LivePlaylistType
from src import sp

class LivePlaylist:
	""" handles crud operations of a live playlist
	the methods shouldnt be complicated
	the bulk logic should be done by the api_handler \n

	This class doesn't save state, it just performs actions
	on the playlists on spotify.
	"""
	def __init__(self, playlist: LivePlaylistType):
		self.uri = playlist['uri']
		self.snapshot_id = playlist['snapshot_id']
		self.name = playlist['name']
		self.num_tracks = playlist['tracks']['total']


	def get_latest_tracks(self, num_songs: int=100):
		""" returns the latest n songs in playlist in reverse order.
		That means the latest added song is at the beginning of the list\n
		if num_songs == None: return all songs in playlist """
		return sp.get_latest_tracks(self.uri, self.num_tracks, num_songs)

	def add_tracks_at_beginning(self, tracks: Tracks):
		sp.add_tracks_at_beginning(self.uri, tracks.ids)

	def remove_tracks(self, tracks: Tracks):
		sp.remove_tracks(self.uri, tracks.ids)

	def replace_tracks(self, tracks: Tracks):
		sp.replace_playlist_tracks(self.uri, tracks.ids)



class LivePlaylists:
	""" handles loading live playlist data and manages them """
	def __init__(self):
		self.playlists: list[LivePlaylist] = []
		self.names: dict[str, int] = {}
		self.uri: dict[str, int] = {}

		self.update_data()


	def update_data(self):
		playlists: list[LivePlaylistType] = sp.get_all_playlists()

		for index, playlist in zip(range(len(playlists)), playlists):
			self.playlists.append(LivePlaylist(playlist))
			self.names[playlist['name']] = index
			self.uri[playlist['uri']] = index

	def get_by_name(self, name: str):
		index = self.names.get(name)
		if index is None:
			raise Exception('Playlist Name does not exist.')

		return self.playlists[index]


	def get_by_uri(self, uri: str):
		index = self.uri.get(uri)
		if index is None:
			raise Exception('Playlist uri does not exist.')

		return self.playlists[index]
