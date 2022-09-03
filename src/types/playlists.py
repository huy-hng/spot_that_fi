from __future__ import annotations
from src.types import DotDict
from src.types.tracks import TrackDict

class _CurrentUserPlaylists(DotDict):
	""" for reference when calling sp.current_user_playlists """
	href: str
	items: list[AbstractPlaylistType]
	limit: int
	next: str | None
	offset: int
	previous: str | None
	total: int


# TODO: turn this into an ABC or protocol
class AbstractPlaylistType(DotDict):
	collaborative: bool
	description: str
	external_urls: dict
	href: str
	id: str
	images: list
	name: str
	owner: PlaylistOwner
	primary_color: None 
	public: bool
	snapshot_id: str
	tracks: AllPlaylistsTracks | SinglePlaylistTracks
	type: str
	uri: str

	def __init__(self, playlist: dict):
		super().__init__(playlist)
		self.owner = PlaylistOwner(self.owner)


class AllPlaylists(AbstractPlaylistType):
	""" sp.current_user_playlists """
	tracks: AllPlaylistsTracks
	def __init__(self, playlist: dict):
		super().__init__(playlist)
		self.tracks = AllPlaylistsTracks(self.tracks)
	

class AllPlaylistsTracks(DotDict):
	href: str
	total: int


class SinglePlaylist(AbstractPlaylistType):
	""" api_handler.get_one_playlist """
	followers: dict
	tracks: SinglePlaylistTracks
	def __init__(self, playlist: dict):
		super().__init__(playlist)
		self.tracks = SinglePlaylistTracks(self.tracks)


class SinglePlaylistTracks(DotDict):
	""" api_handler.get_one_playlist.tracks """	
	href: str
	items_: list[PlaylistTracksItem]
	limit: int
	next: str
	offset: int
	previous: str
	total: int

	def __init__(self, playlist: dict):
		super().__init__(playlist)
		self.items_ = [PlaylistTracksItem(item) for item in playlist['items']]


class PlaylistTracksItem(DotDict):
	"""
		api_handler.get_one_playlist.tracks.items_[0] \n
		when getting a single playlist: playlist.tracks.items[0]
	"""
	added_at: str
	added_by: dict
	is_local: bool
	primary_color: None
	track: PlaylistTrackDict
	video_thumbnail: dict

	def __init__(self, item: dict):
		super().__init__(item)
		self.track = PlaylistTrackDict(self.track)


# REFACTOR: move back to types.tracks
class PlaylistTrackDict(TrackDict):
	episode: bool
	track: bool


# region Sub Dicts
class PlaylistOwner(DotDict):
	id: str
	display_name: str
	external_urls: str
	href: str
	type: str
	uri: str
# endregion