import time
from typing import NamedTuple, Type, TypeGuard, TypeVar

from src import utils
from src import types
from src import log

from src.api.connection import spotify
from src import exceptions 
from src.settings import user_data

'''
This is a barebones wrapper around the spotipy module
to give it more convenience features
'''


def like_tracks(track_ids: list[str]):
	spotify.current_user_saved_tracks_add(track_ids)

def get_liked_tracks_generator(limit=50):
	'''
	returns a generator that loops over liked tracks
	in reverse chronological order.

	First item in first iteration
	is the most recently liked track.
	'''
	offset = 0
	limit = utils.clamp(limit, 1, 50)

	while True:
		items = spotify.current_user_saved_tracks(limit, offset)
		if items is None: continue
		offset += limit

		yield items

		if not items.next:
			break


#------------------------------------------Playlists stuff------------------------------------------

class SyncPairs(NamedTuple):
	main: types.PlaylistType
	snippet:types.PlaylistType 

class PlaylistsManager:
	'''
	Easy access to user playlists
	'''
	def __init__(self, playlists: list[types.PlaylistType] | None = None):
		self.playlists: list[types.PlaylistType]
		self.fetch_playlists(playlists)

		# for easier lookup
		self.names: dict[str, int] = {}
		self.ids: dict[str, int] = {}

		for index, playlist in enumerate(self.playlists):
			self.names[playlist.name] = index
			self.ids[playlist.id] = index

	def fetch_playlists(self, playlists: list[types.PlaylistType] | None = None):
		if playlists is None:
			playlists = get_all_playlists()

		self.playlists = playlists

	def get_by_id(self, playlist_id: str):
		index = self.ids.get(playlist_id)
		if index is None:
			raise exceptions.PlaylistNotFoundError('Playlist id does not exist.')

		return self.playlists[index]

	def get_by_name(self, name: str):
		index = self.names.get(name)
		if index is None:
			raise exceptions.PlaylistNotFoundError('Playlist Name does not exist.')

		return self.playlists[index]

	def get_sync_pairs(self):
		# read pairs from some file
		pairs: list[SyncPairs] = []
		playlist_data = user_data.get_playlist_user_data()

		for data in playlist_data.snippet_playlist:
			main_id = convert_playlist_uri_to_id(data.main_id)
			snippet_id = convert_playlist_uri_to_id(data.snippet_id)

			main = self.get_by_id(main_id)
			snippet = self.get_by_id(snippet_id)
			pairs.append(SyncPairs(main, snippet))

		return pairs


def get_playlist(playlist_id: str):
	'''
	should accept argument as uri, url and id

	Returns
	---
	`types.PlaylistType` or `None` if not found
	'''

	if res := spotify.playlist(playlist_id):
		return types.PlaylistType(res)


def get_all_playlists() -> list[types.PlaylistType]:
	'''
	api call expense: 50 playlists = 1 call

	if one has 60 playlists in their spotify,
	this functions would do 2 api calls
	'''

	all_playlists: list[dict] = []
	offset = 0

	while True:
		playlists: dict | None = spotify.current_user_playlists(offset=offset)

		if playlists is None:
			return []

		all_playlists += playlists['items']
		if playlists['next'] is None:
			break

		offset += 50

	parsed_playlists = [
		types.PlaylistType(playlist)
		for playlist in all_playlists
	]

	return parsed_playlists


#---------------------------------------playlist manipulation---------------------------------------

def get_playlist_track_generator(playlist: types.PlaylistType, *, limit=100):
	'''
	Get latest tracks until total_tracks has been reached
	or no tracks are left.

	Parameters:
		`total_tracks`: total tracks in playlist. Use this to save an api call
		`limit`: amount of tracks to get at once
		`raw`: get PlaylistTracks

	The order is the same as in spotify without any sorting.
	The first returned item is the most recently added tracks

	the section that is returned first are the items that have been
	added last

	so if my playlist is [0,1,2,3,4] and 0 is the first track 
	that has been added and my limit is 2, then the first yield is
	[3,4], then comes [1,2] and at last [0],
	where the generator terminates

	# Note
	Since on spotify new tracks are by default added to 'the bottom'
	of the playlist it appears that playlists are chronologically
	sorted from first added to last added
	'''

	def calc_limit():
		return utils.clamp(limit, 1, 100)
		
	limit = calc_limit()
	total_tracks = playlist.tracks.total

	offset = max(0, total_tracks - limit)
	while items := spotify.playlist_items(playlist.id, limit=calc_limit(), offset=offset):
		if items is None:
			break

		parsed = types.PlaylistTracks(items)
		if total_tracks != parsed.total:  # fixes wrong total_tracks input
			total_tracks = parsed.total
			offset = max(0, total_tracks - limit)
			continue

		offset = parsed.offset
		offset -= limit

		if offset < 0:
			limit += offset
			offset = 0

		yield parsed.items

		if not parsed.previous:
			break


def get_latest_playlist_tracks(playlist: types.PlaylistType,
							   amount_tracks: int = 0,
							   limit=100) -> list[types.PlaylistTrackItem]:
	'''
	returns the latest n songs in playlist in added order.
	That means the latest added song is at the end of the list\n
	if num_songs == 0: return all songs in playlist
	'''

	amount_tracks = utils.clamp(amount_tracks, 0, playlist.total_tracks)
	if amount_tracks == 0: amount_tracks = playlist.total_tracks

	saved: list[types.PlaylistTrackItem] = []
	for tracks in get_playlist_track_generator(playlist, limit=limit):
		if len(saved) + len(tracks) > amount_tracks:
			# only get the specified amount of tracks
			rest = amount_tracks % limit
			saved = tracks[-rest:] + saved
			break
		saved = tracks + saved

	return saved


def add_tracks_at_end_of_playlist(playlist_id,
								  tracks: list[types.PlaylistTrackItem] | list[str],
								  position: int = -1,
								  group_size: int = 1,
								  add_duplicates: bool = False):
	'''
	Adds tracks to playlist. 

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
	'''

	# TODO: use add_duplicates to control if duplicates should be added

	track_ids = convert_track_items_to_ids(tracks)

	group_size = max(0, group_size)

	if position == -1:
		playlist = get_playlist(playlist_id)
		if not playlist: return 

		position = playlist.tracks.total

	curr_position = position

	groups = utils.grouper(track_ids, group_size)
	for group in groups:
		spotify.playlist_add_items(playlist_id, group, curr_position)
		curr_position += group_size
		time.sleep(0.5)


def remove_tracks_from_playlist(playlist: str | types.PlaylistType,
				  tracks: list[types.PlaylistTrackItem] | list[str]):
	'''
	Returns the sum of two decimal numbers in binary digits.
	Removes tracks from a playlist

		Parameters:
			`playlist`: playlist id as a string or `PlaylistType` instance
			`tracks`: list of PlaylistTrackItem or list of track ids (str)
	'''

	if isinstance(playlist, types.PlaylistType):
		playlist = playlist.id

	track_ids = convert_track_items_to_ids(tracks)
	spotify.playlist_remove_all_occurrences_of_items(playlist, track_ids)


def replace_playlist_tracks(playlist: str | types.PlaylistType,
				   tracks: list[types.PlaylistTrackItem] | list[str]):
	'''
	Replaces all tracks in playlist.

	Current Problems:
	---
	Adding multiple tracks that aren't already in the playlist
	results in wonky order.
	Not sorting the playlist in spotify shows the correct order,
	but when sorted by date added, it is scrambled.
	The reason for that is probably date_added attribute is all the same.
	'''

	if isinstance(playlist, types.PlaylistType):
		playlist = playlist.id

	track_ids = convert_track_items_to_ids(tracks)
	spotify.playlist_replace_items(playlist, track_ids)


#------------------------------------------util functions-------------------------------------------

def get_track_ids_from_playlist(tracks: list[types.PlaylistTrackItem]) -> list[str]:
	if not tracks:
		return []
	return [item.track.id for item in tracks]


def get_track_names_from_playlist(tracks: list[types.PlaylistTrackItem]) -> list[str]:
	if len(tracks) == 0:
		return []
	return [item.track.name for item in tracks]


def convert_playlist_uri_to_id(id: str):
	''' converts uris and urls to ids and returns it '''
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


def convert_track_items_to_ids(tracks: list[types.PlaylistTrackItem] | list[str]) -> list[str]:
	if is_set_of(tracks, str):
		return tracks
	elif is_set_of(tracks, types.PlaylistTrackItem):
		return get_track_ids_from_playlist(tracks)

	assert False


T = TypeVar('T')
def is_set_of(val: list[types.PlaylistTrackItem] | list[str], type_: Type[T]) -> TypeGuard[list[T]]:
    return all(isinstance(x, type_) for x in val)
