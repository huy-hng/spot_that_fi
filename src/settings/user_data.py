import json
from typing import Type, TypedDict

class SnippetPlaylistType(TypedDict):
	name: str
	main_uri: str	
	snippet_uri: str	


class PlaylistType(TypedDict):
	snippet_playlist: list[SnippetPlaylistType]
	liked_tracks_without_playlists: str


def get_playlist_user_data():
	with open('../../user_data/playlists.json') as f:
		playlist_data: PlaylistType = json.load(f)
		return playlist_data

# class PlaylistData:
# 	def __init__(self):
# 		with open('../../user_data/playlists.json') as f:
# 			playlist_data: PlaylistType = json.load(f)
