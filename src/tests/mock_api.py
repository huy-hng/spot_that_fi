from src.helpers.helpers import clamp, grouper, read_data
from src.types.playlists import PlaylistType
from src.types.tracks import LikedTrackList

def get_liked_tracks_generator():
	data = read_data('testing_data/all_liked_tracks')

	for d in data:
		yield LikedTrackList(d)
