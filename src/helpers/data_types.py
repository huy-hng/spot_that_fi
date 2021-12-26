from dataclasses import dataclass

@dataclass
class LivePlaylistsTracksType:
	href: str
	total: int
	type: str
	uri: str
	limit: int
	next: None
	offset: int
	previous: None
	total: int

@dataclass
class LivePlaylistType:
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

	def __init__(self, **kwargs):
		self.tracks = LivePlaylistsTracksType(**kwargs['tracks'])

@dataclass
class TrackedPlaylistType:
	name: str
	archive: str
	current: str
	snapshot_id: str

@dataclass
class TracksType:
	# TODO
	next: str
	items: list
