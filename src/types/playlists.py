# from __future__ import annotations
from dataclasses import InitVar, dataclass, field
from src.types import init
from src.types.tracks import TrackDict


@dataclass(slots=True, frozen=True)
class PlaylistOwner:
	id: str
	display_name: str
	external_urls: str
	href: str
	type: str
	uri: str


@dataclass(slots=True, frozen=True)
class AllPlaylistsTracks:
	href: str
	total: int


@dataclass(slots=True, frozen=True)
class PlaylistTrackItem:
	"""
		api_handler.get_one_playlist.tracks.items_[0] \n
		when getting a single playlist: playlist.tracks.items[0]
	"""
	added_at: str
	added_by: dict
	is_local: bool
	primary_color: None
	track: TrackDict
	video_thumbnail: dict

	def __init__(self, d: dict) -> None:
		init(self, d)


@dataclass(slots=True, frozen=True)
class SinglePlaylistTracks:
	""" api_handler.get_one_playlist.tracks """	
	href: str
	items: list[PlaylistTrackItem]
	limit: int
	next: str
	offset: int
	previous: str
	total: int

	def __init__(self, playlist: dict) -> None:
		# items = [PlaylistTracksItem(item) for item in playlist['items']]
		init(self, playlist)


# TODO: merge with allplaylists and singleplaylist since theyre too similar
@dataclass(slots=True, frozen=True)
class AbstractPlaylistType:
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
	followers: dict | None = field(default=None)  # belongs to SinglePlaylist

	def __init__(self, playlist: dict):
		init(self, playlist)


@dataclass(slots=True, frozen=True)
class AllPlaylists(AbstractPlaylistType):
	""" sp.current_user_playlists """
	tracks: AllPlaylistsTracks
	
	def __init__(self, playlist: dict) -> None:
		init(self, playlist)
	

@dataclass(slots=True, frozen=True)
class SinglePlaylist(AbstractPlaylistType):
	""" api_handler.get_one_playlist """
	tracks: SinglePlaylistTracks

	def __init__(self, playlist: dict) -> None:
		init(self, playlist)


@dataclass(slots=True, frozen=True)
class _CurrentUserPlaylists:
	""" for reference when calling sp.current_user_playlists """
	href: str
	items: list[AbstractPlaylistType]
	limit: int
	next: str | None
	offset: int
	previous: str | None
	total: int
