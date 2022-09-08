import json
from dataclasses import dataclass
from typing import TypedDict

from src.types import init


@dataclass(slots=True, frozen=True)
class SnippetPlaylistType:
	name: str
	main_id: str	
	snippet_id: str	

	def __init__(self, d: dict) -> None:
		init(self, d)


@dataclass(slots=True, frozen=True)
class UserPlaylistType:
	snippet_playlist: list[SnippetPlaylistType]
	liked_tracks_without_playlists: str
	
	def __init__(self, d: dict) -> None:
		init(self, d)


def get_playlist_user_data():
	with open('../../user_data/playlists.json') as f:
		playlist_data: UserPlaylistType = json.load(f)
		return playlist_data


# class PlaylistData:
# 	def __init__(self):
# 		with open('../../user_data/playlists.json') as f:
# 			playlist_data: PlaylistType = json.load(f)
