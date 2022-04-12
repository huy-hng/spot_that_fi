from dataclasses import dataclass, field
from src.helpers.logger import log





@dataclass
class TrackedPlaylistType:
	name: str
	archive: str
	current: str
	snapshot_id: str



@dataclass
class TracksType:
	next: str
	items: list


# @dataclass
# class LikedTrack:
# 	added_at: str # TODO: could be datetime instead
# 	track: dict
