from src import sp
from src.playlists.live_playlists import LivePlaylists

live_playlists = LivePlaylists()
archive_playlist = live_playlists.get_by_name('Playlist')

new_tracks = ["4M3wJczMgJmUsSg1Hy4p5D",
 							"4mQTPwMKPNLGODbonuGCtP",
 							"5F223mR6ZL7MQVDdt9ajdY",
 							"33Axn97y8NTI3EQfUkMtA4"]

def add_track_with_api_handler():
	sp.add_tracks_at_end_as_bulk(
		archive_playlist.uri, new_tracks, archive_playlist.tracks_in_playlist)

# track = ['5GizkpMZMIzhj2o5eK7GOD' for _ in range(10)]

# sp.replace_playlist_tracks(playlist.uri, track)


# sp.add_tracks_at_end(playlist.uri, new_tracks)

# tracks = sp.get_latest_tracks(playlist.uri, playlist.num_tracks, None)
# print(tracks.names)

