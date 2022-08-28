from src.types import DotDict
from types.tracks import TrackDict

class SpotifyPlaylistsOwnerType(DotDict):
	id: str
	display_name: str
	external_urls: str
	href: str
	type: str
	uri: str


class SpotifySinglePlaylistTracksType(DotDict):
	href: str
	# total: int
	# limit: int
	# next: None
	# offset: int
	# previous: None
	total: int
	# type: str
	# uri: str


class PlaylistTrackDict(TrackDict):
	episode: bool
	track: bool


class PlaylistTracksItem(DotDict):
	""" when getting a single playlist: playlist.tracks.items[0] """
	added_at: str
	added_by: dict
	is_local: bool
	primary_color: None
	track: PlaylistTrackDict
	video_thumbnail: dict

	def __init__(self, item: dict):
		super().__init__(item)
		self.track = PlaylistTrackDict(self.track)
# belong together
class SpotifySinglePlaylistTracksType(DotDict):
	href: str
	items_: list[PlaylistTracksItem]
	limit: int
	next: str
	offset: int
	previous: str
	total: int

	def __init__(self, playlist: dict):
		super().__init__(playlist)
		# TODO check if this works
		self.items_ = [
			PlaylistTracksItem(item)
			for item in playlist['items']
		]
		# self.tracks = [SinglePlaylistTracksItemType(track) for track in self.get('items')]


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
	tracks: SpotifySinglePlaylistTracksType | SpotifySinglePlaylistTracksType
	# tracks: SpotifyPlaylistsTracksType
	type: str
	uri: str

	def __init__(self, playlist: dict):
		super().__init__(playlist)
		self.owner = SpotifyPlaylistsOwnerType(self.owner)
		if self.tracks.get('items') is None:
			self.tracks = SpotifySinglePlaylistTracksType(self.tracks)
		else:
			self.tracks = SpotifySinglePlaylistTracksType(self.tracks)
