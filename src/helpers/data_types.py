from dataclasses import dataclass, field
from typing import Optional

@dataclass
class SpotifyPlaylistsOwnerType:
	id: str
	display_name: str
	external_urls: str
	href: str
	type: str
	uri: str

@dataclass
class SpotifyPlaylistsTracksType:
	href: str
	total: int
	limit: int
	next: None
	offset: int
	previous: None
	total: int
	type: str
	uri: str


@dataclass
class SpotifySinglePlaylistTracksType:
	href: str
	items: list
	limit: int
	total: int
	offset: int
	next: str
	previous: str

@dataclass
class SpotifyPlaylistType:
	collaborative: bool
	description: str
	external_urls: dict
	followers: dict
	href: str
	id: str
	images: list
	name: str
	owner: SpotifyPlaylistsOwnerType
	primary_color: None 
	public: bool
	snapshot_id: str
	tracks: SpotifyPlaylistsTracksType
	type: str
	uri: str

	def __post_init__(self):
		self.owner = SpotifyPlaylistsOwnerType(**self.owner)
		if self.tracks.get('items') is None:
			self.tracks = SpotifyPlaylistsTracksType(**self.tracks)
		else:
			self.tracks = SpotifySinglePlaylistTracksType(**self.tracks)

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
