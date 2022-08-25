from src.types import DotDict

class TrackItem(DotDict):
	""" previously called LikedTracksItemTrack """
	album: dict
	artists: list
	available_markets: list
	disc_number: int
	duration_ms: int
	# episode: bool # playlistTrack has this field
	explicit: bool
	external_ids: dict
	external_urls: dict
	href: str
	id: str
	is_local: bool
	name: str
	popularity: int
	preview_url: str
	# track: bool # playlistTrack has this field
	track_number: int
	type: str
	uri: str


class PlaylistTrackItem(TrackItem):
	episode: bool
	track: bool


class LikedTracksItem(DotDict):
	added_at: str # TODO could be datetime
	track: TrackItem

	def __init__(self, item: dict):
		super().__init__(item)
		self.track = TrackItem(self.track)
	

class LikedTracksList(DotDict):
	href: str
	tracks: list[LikedTracksItem] # actually called items but renamed for dot notation access
	limit: int
	next: str | None
	offset: int
	previous: str | None
	total: int

	def __init__(self, item: dict):
		super().__init__(item)
		# self.tracks = [LikedTracksItem(track) for track in self.get('items')]
		# TODO check if this works
		self.tracks = [LikedTracksItem(track) for track in item['items']]


class PlaylistTracksItem(DotDict):
	added_at: str
	added_by: dict
	is_local: bool
	primary_color: None
	track: PlaylistTrackItem
	video_thumbnail: dict

	def __init__(self, item: dict):
		super().__init__(item)
		self.track = PlaylistTrackItem(self.track)

class PlaylistTracks(DotDict):
	# TODO: same as LikedTracks
	...