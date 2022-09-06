# from __future__ import annotations
from dataclasses import InitVar, dataclass, field
from src.types import init
from src.types.tracks import TrackDict


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
		init(self, playlist)


class PlaylistOwner:
	id: str = field(repr=False)
	display_name: str = field(repr=False)
	external_urls: str = field(repr=False)
	href: str = field(repr=False)
	type: str = field(repr=False)
	uri: str = field(repr=False)


@dataclass(slots=True, frozen=True)
class PlaylistTracks:
	""" api_handler.get_one_playlist.tracks """
	href: str = field(repr=False)
	total: int

	# PlaylistTypeTracks
	items: list[PlaylistTrackItem] = field(default_factory=list, repr=False)
	limit: int | None = field(default=None, repr=False)
	next: str | None = field(default=None, repr=False)
	offset: int | None = field(default=None, repr=False)
	previous: str | None = field(default=None, repr=False)

	def __init__(self, playlist: dict) -> None:
		init(self, playlist)


@dataclass(slots=True, frozen=True)
class PlaylistType:
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
	tracks: PlaylistTracks
	type: str
	uri: str
	followers: dict | None = field(default=None)  # belongs to SinglePlaylist

	def __init__(self, playlist: dict):
		init(self, playlist)


@dataclass(slots=True, frozen=True)
class AllPlaylists(PlaylistType):
	""" sp.current_user_playlists """
	tracks: AllPlaylistsTracks

	def __init__(self, playlist: dict) -> None:
		init(self, playlist)


@dataclass(slots=True, frozen=True)
class SinglePlaylist(PlaylistType):
	""" api_handler.get_one_playlist """
	tracks: SinglePlaylistTracks

	def __init__(self, playlist: dict) -> None:
		init(self, playlist)


@dataclass(slots=True, frozen=True)
class _CurrentUserPlaylists:
	""" for reference when calling sp.current_user_playlists """
	href: str
	items: list[PlaylistType]
	limit: int
	next: str | None
	offset: int
	previous: str | None
	total: int
