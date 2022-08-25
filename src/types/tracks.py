from src.types import DotDict

class TrackDict(DotDict):
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


class PlaylistTrackDict(TrackDict):
	episode: bool
	track: bool


class LikedTracksItemDict(DotDict):
	added_at: str # TODO could be datetime
	track: TrackDict

	def __init__(self, item: dict):
		super().__init__(item)
		self.track = TrackDict(self.track)
	

class LikedTracksListDict(DotDict):
	href: str
	tracks: list[LikedTracksItemDict] # actually called items but renamed for dot notation access
	limit: int
	next: str | None
	offset: int
	previous: str | None
	total: int

	def __init__(self, item: dict):
		super().__init__(item)
		# self.tracks = [LikedTracksItem(track) for track in self.get('items')]
		# TODO check if this works
		self.tracks = [LikedTracksItemDict(track) for track in item['items']]


class PlaylistTracksItemDict(DotDict):
	added_at: str
	added_by: dict
	is_local: bool
	primary_color: None
	track: PlaylistTrackDict
	video_thumbnail: dict

	def __init__(self, item: dict):
		super().__init__(item)
		self.track = PlaylistTrackDict(self.track)


class PlaylistTracksListDict(DotDict):
	# TODO: same as LikedTracks
	...