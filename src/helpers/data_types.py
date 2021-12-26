from dataclasses import dataclass

@dataclass
class SpotifyPlaylistsTracksType:
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
class SpotifyPlaylistType:
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
	tracks: SpotifyPlaylistsTracksType
	type: str
	uri: str

	def __init__(self, **kwargs):
		self.tracks = SpotifyPlaylistsTracksType(**kwargs['tracks'])

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
