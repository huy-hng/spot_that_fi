from dataclasses import InitVar, dataclass, field
from src.types import init

		
@dataclass(slots=True, frozen=True)
class TrackDict:
	""" previously called LikedTracksItemTrack """
	album: dict = field(repr=False)
	artists: list = field(repr=False)
	available_markets: list = field(repr=False)
	disc_number: int = field(repr=False)
	duration_ms: int = field(repr=False)
	# episode: bool # playlistTrack has this field
	explicit: bool = field(repr=False)
	external_ids: dict = field(repr=False)
	external_urls: dict = field(repr=False)
	href: str = field(repr=False)
	id: str
	is_local: bool = field(repr=False)
	name: str
	popularity: int = field(repr=False)
	preview_url: str = field(repr=False)
	# track: bool # playlistTrack has this field
	track_number: int = field(repr=False)
	type: str = field(repr=False)
	uri: str = field(repr=False)

	episode: bool | None = field(default=None, repr=False) # playlistTrack has this field
	track: bool | None = field(default=None, repr=False)  # playlistTrack has this field

		
@dataclass(slots=True, frozen=True)
class LikedTrackItem:

	added_at: str # TODO could be datetime
	track: TrackDict

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

	@property
	def tracks(self):
		return [item.track for item in self.items]
