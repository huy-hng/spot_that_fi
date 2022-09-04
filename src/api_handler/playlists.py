from typing import NamedTuple, Type, TypeGuard, TypeVar

from src.api_handler import sp
from src.types.playlists import AllPlaylists, PlaylistTracksItem, SinglePlaylist
from src.settings.user_data import get_playlist_user_data

from src.helpers.exceptions import PlaylistNotFoundError
from src.helpers.logger import log


class SyncPairs(NamedTuple):
	main: AllPlaylists
	snippet: AllPlaylists


class PlaylistsHandler:
	def __init__(self, playlists: list[AllPlaylists]):
		self.playlists = [PlaylistHandler(playlist) for playlist in playlists]

		# for easier lookup
		self.names: dict[str, int] = {}
		self.ids: dict[str, int] = {}

		for index, playlist in enumerate(self.playlists):
			self.names[playlist.name] = index
			self.ids[playlist.id] = index


	def get_by_id(self, playlist_id: str):
		index = self.ids.get(playlist_id)
		if index is None:
			raise PlaylistNotFoundError('Playlist id does not exist.')

		return self.playlists[index]


	def get_by_name(self, name: str):
		index = self.names.get(name)
		if index is None:
			raise PlaylistNotFoundError('Playlist Name does not exist.')

		return self.playlists[index]


	def get_sync_pairs(self) -> list[SyncPairs]:
		# read pairs from some file
		pairs: list[SyncPairs] = []
		playlist_data = get_playlist_user_data()

		for data in playlist_data.snippet_playlist:
			main_id = convert_playlist_uri_to_id(data.main_id)
			snippet_id = convert_playlist_uri_to_id(data.snippet_id)

			main = self.get_by_id(main_id)
			snippet = self.get_by_id(snippet_id)
			# pairs.append(SyncPairs(main.playlist_data, snippet.playlist_data))

		return pairs




class PlaylistHandler:
	""" handles crud operations of a live playlist
	the methods shouldnt be complicated
	the bulk logic should be done by the api_handler \n

	This class doesn't save state, it just performs actions
	on the playlists on spotify.
	"""
	def __init__(self, playlist: AllPlaylists | SinglePlaylist):
		self.playlist_data = playlist
		self.id = playlist.id
		self.name = playlist.name

		self.snapshot_id = playlist.snapshot_id
		self.total_tracks = playlist.tracks.total


	def _update_data(self):
		data = sp.get_one_playlist(self.id)
		self.total_tracks = data.tracks.total
		self.snapshot_id = data.snapshot_id


	def get_track_generator(self, *, limit=100):
		for items in sp.get_playlist_tracks_generator(self.id, limit=limit):
			self.total_tracks = items.total
			yield items.items_


	def get_latest_tracks(self, num_tracks: int=0) -> list[PlaylistTracksItem]:
		""" returns the latest n songs in playlist in added order.
		That means the latest added song is at the end of the list\n
		if num_songs == 0: return all songs in playlist """
		# TODO: put limit somewhere else
		LIMIT = 100

		if num_tracks == 0 or num_tracks > self.total_tracks:
			self._update_data()
			num_tracks = self.total_tracks

		saved: list[PlaylistTracksItem]  = []
		for tracks in self.get_track_generator(limit=LIMIT):
			if len(saved) + len(tracks) > num_tracks:
				rest = num_tracks % LIMIT
				saved = tracks[-rest:] + saved
				break
			saved = tracks + saved

		return saved


	def add_tracks_at_end(self,
		tracks: list[str | PlaylistTracksItem], add_duplicates: bool=False):
		""" this should behave like adding songs normally to a playlist.
			each song should be appended at the end of the playlist.

			That means, (tracks[-1]) should be the last song added.

			Or in other words the first song, that is in sorted
			by recently added.
		"""
		# TODO: use add_duplicates to control if duplicates should be added

		track_ids = self.handle_non_ids(tracks)
		self._update_data()
		sp.add_tracks_to_playlist(self.id, track_ids, self.total_tracks)


	def remove_tracks(self, tracks: list[str | PlaylistTracksItem]):
		track_ids = self.handle_non_ids(tracks)
		sp.remove_tracks(self.id, track_ids)
		self._update_data()


	def replace_tracks(self, tracks: list[str | PlaylistTracksItem]):
		track_ids = self.handle_non_ids(tracks)
		sp.replace_playlist_tracks(self.id, track_ids)
		self._update_data()


	def handle_non_ids(self, tracks: list[str | PlaylistTracksItem]) -> list[str]:
		if is_set_of(tracks, str):
			return tracks
		elif is_set_of(tracks, PlaylistTracksItem):
			return self.get_ids(tracks)
		else:
			raise


	@staticmethod
	def get_ids(tracks: list[PlaylistTracksItem]) -> list[str]:
		if not tracks: return []

		return [item.track.id for item in tracks]


	@staticmethod
	def get_names(tracks: list[PlaylistTracksItem]) -> list[str]:
		if len(tracks) == 0:
			return []

		return [item.track.name for item in tracks]


@staticmethod
def convert_playlist_uri_to_id(id: str):
	""" converts uris and urls to ids and returns it """
	type_ = 'playlist'

	error = False
	itype = None

	fields = id.split(":")
	if len(fields) >= 3:
		itype = fields[-2]
		if type_ != itype:
			error = True
		return fields[-1]

	fields = id.split("/")
	if len(fields) >= 3:
		itype = fields[-2]
		if type_ != itype:
			error = True
		return fields[-1].split("?")[0]

	if error:
		log.warning(f'Expected id of type {type_} but found type {itype}, {id}')
	return id


T = TypeVar('T')

def is_set_of(val: list[str | PlaylistTracksItem], type: Type[T]) -> TypeGuard[list[T]]:
    return all(isinstance(x, type) for x in val)