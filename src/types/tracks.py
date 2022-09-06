from dataclasses import InitVar, dataclass, field
from src.types import init

		
@dataclass(slots=True, frozen=True)
class TrackDict:
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

	episode: bool | None = field(default=None) # playlistTrack has this field
	track: bool | None = field(default=None)  # playlistTrack has this field

		
@dataclass(slots=True, frozen=True)
class LikedTrackItem:

	added_at: str # TODO could be datetime
	track: TrackDict
	raw_track: TrackDict | None = field(default=None)

	def __init__(self, item: dict) -> None:
		init(self, item)


@dataclass(slots=True, frozen=True)
class LikedTrackList:
	href: str
	items: list[LikedTrackItem]
	limit: int
	next: str | None
	offset: int
	previous: str | None
	total: int

	def __init__(self, d: dict) -> None:
		init(self, d)

	# def __init__(self, item: dict):
	# 	super().__init__(item)
	# 	# self.tracks = [LikedTracksItem(track) for track in self.get('items')]
	# 	# TODO check if this works
	# 	self.items_ = [LikedItemDict(track) for track in item['items']]

	@property
	def tracks(self):
		return [item.track for item in self.items]
