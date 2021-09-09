from typing import TypedDict

class PlaylistsTracksType(TypedDict):
	href: str
	total: int
	type: str
	uri: str
	limit: int
	next: None
	offset: int
	previous: None
	total: int

class PlaylistType(TypedDict):
	collaborative: bool
	description: str
	external_urls: dict
	href: str
	id: str
	images: list
	name: str
	owner: dict
	primary_color: None
	public: bool
	snapshot_id: str
	tracks: PlaylistsTracksType
	type: str
	uri: str


class TrackedPlaylistsTypeHelper(TypedDict):
	uri: str
	snapshot_id: str
class TrackedPlaylistsType(TypedDict):
	name: str
	all: TrackedPlaylistsTypeHelper
	snippet: TrackedPlaylistsTypeHelper

