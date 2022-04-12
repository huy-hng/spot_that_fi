from src.types import DotDict

class SpotifyPlaylistsOwnerType(DotDict):
	id: str
	display_name: str
	external_urls: str
	href: str
	type: str
	uri: str


class SpotifyPlaylistsTracksType(DotDict):
	href: str
	# total: int
	# limit: int
	# next: None
	# offset: int
	# previous: None
	total: int
	# type: str
	# uri: str


class SinglePlaylistTracksItemType(DotDict):
	""" when getting a single playlist: playlist.tracks.items[0] """
	added_at: str # TODO: could be datetime instead
	added_by: dict
	is_local: bool
	primary_color: None
	track: dict
	video_thumbnail: dict
# belong together
class SpotifySinglePlaylistTracksType(DotDict):
	href: str
	tracks: list[SinglePlaylistTracksItemType]
	limit: int
	next: str
	offset: int
	previous: str
	total: int

	def __init__(self, playlist: dict):
		super().__init__(playlist)
		self.tracks = [SinglePlaylistTracksItemType(track) for track in self.get('items')]


class SpotifyPlaylistType(DotDict):
	collaborative: bool
	description: str
	external_urls: dict
	# followers: dict
	href: str
	id: str
	images: list
	name: str
	owner: SpotifyPlaylistsOwnerType
	primary_color: None 
	public: bool
	snapshot_id: str
	tracks: SpotifyPlaylistsTracksType | SpotifySinglePlaylistTracksType
	# tracks: SpotifyPlaylistsTracksType
	type: str
	uri: str

	def __init__(self, playlist: dict):
		super().__init__(playlist)
		self.owner = SpotifyPlaylistsOwnerType(self.owner)
		if self.tracks.get('items') is None:
			self.tracks = SpotifyPlaylistsTracksType(self.tracks)
		else:
			self.tracks = SpotifySinglePlaylistTracksType(self.tracks)
