import json
import math
from dataclasses import dataclass
from data_types import PlaylistType

from main import sp


@dataclass
class Playlist:
	tracks: list	
	snapshot_id: str
	uri: str
	name: str
	num_tracks: int

	def __init__(self, playlist: PlaylistType):
		self.uri = playlist['uri']
		self.snapshot_id = playlist['snapshot_id']
		self.name = playlist['name']
		self.num_tracks = playlist['tracks']['total']

	def get_tracks(self, num_songs=100):
		# TODO if limit == None: return all songs

		if num_songs < 100:
			limit = 100

		offset = self.num_tracks
		num_batches = math.ceil(limit / 100)
		tracks = []
		for i in range(num_batches):
			if i == num_batches-1:
				offset -= limit % 100 # TODO test this logic
			else:
				offset -= 100

			if offset < 0: offset = 0

			tracks += self._get_tracks()
		tracks.reverse() # TODO think about order
		return tracks	

	def _get_tracks(self, limit=100, offset=0):
		return sp.playlist_items(
			self.uri, fields='items', limit=limit, offset=offset)['items']

class Playlists:
	def __init__(self, playlists: dict):
		self.playlists: dict[str, Playlist] = {}

		for playlist in playlists['items']:
			self.playlists[playlist['name']] = Playlist(playlist)


def create_data_class(data: dict):
	for k,v in data.items():
		print(f'{k}: {type(v).__name__}')
		type_ = type(v).__name__
		if type_ == 'list':
			print('=============')
			create_data_class(v[0])
		elif type_ == 'dict':
			print('=============')
			create_data_class(v)

if __name__ == '__main__':
	with open('../data/playlists.json') as f:
		playlists = f.read()
	playlists = json.loads(playlists)
	create_data_class(playlists)
	