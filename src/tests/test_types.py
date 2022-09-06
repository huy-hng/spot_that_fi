import json

from src.types import playlists
from src.types import tracks

def get_file(path: str):
	with open(f'data/{path}') as f:
		return json.load(f)

def test_parse_liked_tracks():
	data = get_file('liked_tracks.json')

	liked_tracks: list[dict] = data['items']
	parsed = tracks.LikedTrackItem(liked_tracks[0])
	
	print(parsed.track.episode)
	print(parsed.raw_track)
	print(parsed.added_at)

def test_parse_playlist_track():
	data = get_file('temp.json')

	playlist_tracks: list[dict] = data['tracks']['items']
	parsed = playlists.PlaylistTrackItem(playlist_tracks[0])
	print(parsed.track.name)

def test_parse_all_playlists():
	data = get_file('api_data/current_user_playlist_items.json')
	# parsed = playlists.AbstractPlaylistType(data[0])
	parsed = playlists.PlaylistType(data[0])
	print(parsed.tracks.total)
	print(parsed.owner.display_name)
	print(parsed.tracks.items)

	# print(parsed.track.name)

def test_parse_one_playlist():
	
	data = get_file('api_data/get_one_playlist.json')
	parsed = playlists.PlaylistType(data)
	print(parsed.tracks.total)
	print(parsed.tracks.items[0].track.name)
