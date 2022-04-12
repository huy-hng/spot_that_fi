from src.types import DotDict

class LikedTracksItemTrack(DotDict):
	# TODO: might be a generic track
	album: dict
	artists: list
	available_markets: list
	disc_number: int
	duration_ms: int
	explicit: bool
	external_ids: dict
	external_urls: dict
	href: str
	id: str
	is_local: bool
	name: str
	popularity: int
	preview_url: str
	track_number: int
	type: str
	uri: str


class LikedTracksItem(DotDict):
	added_at: str # TODO could be datetime
	track: LikedTracksItemTrack

	def __init__(self, item: dict):
		super().__init__(item)
		self.track = LikedTracksItemTrack(self.track)
	

class LikedTracks(DotDict):
	href: str
	tracks: list[LikedTracksItem] # actually called items but renamed for dot notation access
	limit: int
	next: str | None
	offset: int
	previous: str | None
	total: int

	def __init__(self, item: dict):
		super().__init__(item)
		self.tracks = [LikedTracksItem(track) for track in self.get('items')]
