import math
from typing import Union

from src.tracks import Tracks
from src.data_types import LivePlaylistType, TracksType
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
		self.tracks_in_playlist = playlist['tracks']['total']


	def get_latest_tracks(self, num_tracks: int):
		""" returns the latest n songs in playlist in reverse order.
		That means the latest added song is at the beginning of the list\n
		if num_songs == None: return all songs in playlist """
		generator = sp.get_tracks_generator(self.uri, self.tracks_in_playlist)
		tracks = []
		for t in generator:
			if len(tracks) + len(t) > num_tracks:
				# TODO add the last few t to tracks
				return tracks
			tracks += t


	def add_tracks_at_beginning(self, tracks: list[TracksType]):
		sp.add_tracks_at_beginning(self.uri, tracks)

	def add_tracks_at_end(self, tracks: list[TracksType],
															add_duplicates: bool = False):
		""" this should behave like adding songs normally to a playlist.
				each song should be appended at the end of the playlist.\n
				That means, (tracks[-1]) should be the last song added.\n
				Or in other words the first song, that is in sorted
				by recently added."""

		# TODO: use add_duplicates to control if duplicates should be added
		sp.add_tracks_and_end(self.uri, tracks, self.tracks_in_playlist)

	def remove_tracks(self, tracks: list[TracksType]):
		sp.remove_tracks(self.uri, tracks)

	def replace_tracks(self, tracks: list[TracksType]):
		sp.replace_playlist_tracks(self.uri, tracks)



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
