#%%
from src import sp
from src.playlists.live_playlists import LivePlaylists
from src.features.backup import backup_all_playlists

live_playlists = LivePlaylists()
# backup_all_playlists(live_playlists)


playlist = live_playlists.get_by_name('Playlist')
tracks = playlist.get_latest_tracks()
print(tracks)
track = ['5GizkpMZMIzhj2o5eK7GOD' for _ in range(10)]

sp.replace_playlist_tracks(playlist.uri, track)

new_tracks = ["4M3wJczMgJmUsSg1Hy4p5D",
 							"3tGqIP81Ha5lyDOLWemQ78",
 							"5F223mR6ZL7MQVDdt9ajdY",
 							"33Axn97y8NTI3EQfUkMtA4"]

sp.add_tracks_at_beginning(playlist.uri, new_tracks)

# tracks = sp.get_latest_tracks(playlist.uri, playlist.num_tracks, None)
# print(tracks.names)
