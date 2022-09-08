from __future__ import annotations
import time
from typing import NamedTuple, Type, TypeGuard, TypeVar

from src import api
from src.api import spotify
from src.types.playlists import PlaylistType, PlaylistTrackItem, PlaylistType, PlaylistTracks
from src.settings.user_data import get_playlist_user_data

from src.helpers.helpers import grouper
from src.helpers.exceptions import PlaylistNotFoundError
from src.helpers.logger import log


class SyncPairs(NamedTuple):
	main: PlaylistHandler
	snippet: PlaylistHandler



class PlaylistsHandler:
	def __init__(self):
		self.playlists: list[PlaylistHandler]
		self.fetch_playlists()

		# for easier lookup
		self.names: dict[str, int] = {}
		self.ids: dict[str, int] = {}

		for index, playlist in enumerate(self.playlists):
			self.names[playlist.name] = index
			self.ids[playlist.id] = index


	def fetch_playlists(self):
		playlists = api.get_all_playlists()
		self.playlists = [PlaylistHandler(playlist) for playlist in playlists]


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


	def get_sync_pairs(self):
		# read pairs from some file
		pairs: list[SyncPairs] = []
		playlist_data = get_playlist_user_data()

		for data in playlist_data.snippet_playlist:
			main_id = convert_playlist_uri_to_id(data.main_id)
			snippet_id = convert_playlist_uri_to_id(data.snippet_id)

			main = self.get_by_id(main_id)
			snippet = self.get_by_id(snippet_id)
			pairs.append(SyncPairs(main, snippet))

		return pairs


# REFACTOR: either use this class exclusively and inherit/merge from/with PlaylistType
	# merging could cause problems with the hacky way PlaylistType instantiation works
# REFACTOR: or delete this class and move its method to src.api
class PlaylistHandler:
	""" handles crud operations of a live playlist
	the methods shouldnt be complicated
	the bulk logic should be done by the api_handler \n

	This class doesn't save state, it just performs actions
	on the playlists on spotify.
	"""
	def __init__(self, playlist: PlaylistType):
		self.playlist_data = playlist
		self.id = playlist.id
		self.name = playlist.name

		self.snapshot_id = playlist.snapshot_id
		self.total_tracks = playlist.tracks.total

	@classmethod
	def create_from_id(cls, playlist_id: str):
		playlist = api.get_one_playlist(playlist_id)
		return cls(playlist)

	def _update_data(self):
		data = api.get_one_playlist(self.id)
		self.total_tracks = data.tracks.total
		self.snapshot_id = data.snapshot_id


	def get_track_generator(self, *, limit=100, raw=False):
		""" Get latest tracks until total_tracks has been reached
			or no tracks are left.

			Args:
				total_tracks: total_tracks in playlist. Use this to save an api call
				limit: amount of tracks to get at once
				raw: get PlaylistTracks

			The order is the same as in spotify without any sorting.
			The first returned item is the most recently added tracks
			
			the section that is returned first are the items that have been
			added last
			
			so if my playlist is [0,1,2,3,4] and 0 is the first track 
			that has been added and my limit is 2, then the first yield is
			[3,4], then comes [1,2] and at last [0],
			where the generator terminates

			### Note
			Since on spotify new tracks are by default added to 'the bottom'
			of the playlist it appears that playlists are chronologically
			sorted from first added to last added
		"""

		clamp_limit = lambda limit: max(1, min(100, limit))
		limit = clamp_limit(limit)

		offset = max(0, self.total_tracks - limit)
		while items := spotify.playlist_items(self.id, limit=clamp_limit(limit), offset=offset):
			if items is None: break

			parsed = PlaylistTracks(items)
			if self.total_tracks != parsed.total: # fixes wrong self.total_tracks input
				self.total_tracks = parsed.total
				offset = max(0, self.total_tracks - limit)
				continue

			offset = parsed.offset
			offset -= limit

			if offset < 0:
				limit += offset
				offset = 0

			yield parsed.items

			if not parsed.previous:
				break


	def get_latest_tracks(self, num_tracks: int=0) -> list[PlaylistTrackItem]:
		""" returns the latest n songs in playlist in added order.
		That means the latest added song is at the end of the list\n
		if num_songs == 0: return all songs in playlist """
		# TODO: put limit somewhere else
		LIMIT = 100

		if num_tracks == 0 or num_tracks > self.total_tracks:
			self._update_data()
			num_tracks = self.total_tracks

		saved: list[PlaylistTrackItem]  = []
		for tracks in self.get_track_generator(limit=LIMIT):
			if len(saved) + len(tracks) > num_tracks:
				rest = num_tracks % LIMIT
				saved = tracks[-rest:] + saved
				break
			saved = tracks + saved

		return saved


	def add_tracks_at_end(self,
		tracks: list[PlaylistTrackItem] | list[str],
		position: int=-1,
		group_size: int=1,
		add_duplicates: bool=False
	):
		""" Adds tracks to playlist. 

			Args:
				playlist_id:
					the id or uri of the playlist to add tracks to
				track_ids:
					a list of track ids to add to the playlist
				position:
					the position to add the tracks to
					if position == -1: add at the end
				group_size:
					optional argument for batching tracks (to save on rate limiting)
					if group_size <= 0: add all tracks at once
					if group_size == 1: add one track at a time
					if group_size > 1: add {group_size} tracks at once


			this should behave like adding songs normally to a playlist.
			each song should be appended at the end of the playlist.

			That means, (tracks[-1]) should be the last song added.

			Or in other words the first song, that is in sorted
			by recently added.
		"""
		# TODO: use add_duplicates to control if duplicates should be added

		track_ids = handle_non_ids(tracks)

		group_size = max(0, group_size)

		if position == -1:
			position = api.get_one_playlist(self.id).tracks.total

		curr_position = position

		groups = grouper(track_ids, group_size)
		for group in groups:
			spotify.playlist_add_items(self.id, group, curr_position)
			curr_position += group_size
			time.sleep(0.5)

		self._update_data()


	def remove_tracks(self, tracks: list[PlaylistTrackItem] | list[str]):
		track_ids = handle_non_ids(tracks)
		spotify.playlist_remove_all_occurrences_of_items(self.id, track_ids)
		self._update_data()


	def replace_tracks(self, tracks: list[PlaylistTrackItem] | list[str]):
		""" Replaces all tracks in playlist.

			Adding multiple tracks that aren't already in the playlist
			results in wonky order.
			Not sorting the playlist in spotify shows
			the correct order, but when sorted by date added, it is scrambled.
			The reason for that is probably date_added attribute is all the same.
		"""
		track_ids = handle_non_ids(tracks)
		spotify.playlist_replace_items(self.id, track_ids)
		self._update_data()


def get_ids(tracks: list[PlaylistTrackItem]) -> list[str]:
	if not tracks: return []

	return [item.track.id for item in tracks]


def get_names(tracks: list[PlaylistTrackItem]) -> list[str]:
	if len(tracks) == 0:
		return []

	return [item.track.name for item in tracks]


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

def handle_non_ids(tracks: list[PlaylistTrackItem] | list[str]) -> list[str]:
	if is_set_of(tracks, str):
		return tracks
	elif is_set_of(tracks, PlaylistTrackItem):
		return get_ids(tracks)

	assert False


def is_set_of(val: list[PlaylistTrackItem] | list[str], type_: Type[T]) -> TypeGuard[list[T]]:
    return all(isinstance(x, type_) for x in val)