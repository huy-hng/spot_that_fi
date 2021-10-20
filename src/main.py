from src import sp
from src.playlists.live_playlists import LivePlaylists
from src.tracks import Tracks

live_playlists = LivePlaylists()
calm = live_playlists.get_by_name('Calm All')
new_data = sp.get_one_playlist(calm.uri)
print(new_data)

# tracks = calm.get_latest_tracks(None)
# track_ids = Tracks.get_ids(tracks)
# print(track_ids)