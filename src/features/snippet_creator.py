from src.playlists import Playlists
from src.data_types import TrackedPlaylistClusterType
from src.api_handler import sp

class SnippetCreator:
	"""
	This class doesnt know whether a playlist has changed or not,
	it just replaces all songs in snippet playlist with x amount from all playlist
	"""

	def __init__(self, live_playlists: Playlists,
										 cluster: TrackedPlaylistClusterType):
		self.live_playlists = live_playlists
		self.cluster = cluster
		self.snippet_uri = self.cluster['snippet']['uri']
		self.all_uri = self.cluster['all']['uri']

		self.tracks_amount = 50


	def get_tracks_from_all(self):
		return self._get_tracks_from_with_uri(self.all_uri)

	def get_tracks_from_snippet(self):
		return self._get_tracks_from_with_uri(self.snippet_uri)

	def _get_tracks_from_with_uri(self, uri: str):
		live_playlist = self.live_playlists.get_by_uri(uri)
		tracks = live_playlist.get_latest_tracks(self.tracks_amount)
		return tracks


	def replace_snippet_tracks(self):
		tracks = self.get_tracks_from_all()
		sp.replace_playlist_tracks(self.snippet_uri, tracks.ids)


	def calculate_playlist_length_with_duration(self):
		pass