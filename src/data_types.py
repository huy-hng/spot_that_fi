from typing import TypedDict

class LivePlaylistsTracksType(TypedDict):
	href: str
	total: int
	type: str
	uri: str
	limit: int
	next: None
	offset: int
	previous: None
	total: int

class LivePlaylistType(TypedDict):
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
	tracks: LivePlaylistsTracksType
	type: str
	uri: str


class TrackedPlaylistType(TypedDict):
	name: str
	archive: str
	current: str
	snapshot_id: str

class TracksType(TypedDict):
	# TODO
	next: str
	pass