from src.backup import backup_all_playlists
from src.playlist_handler import Playlists

playlists = Playlists()
calm = playlists.get_by_name('Calm')

tracks = calm.get_latest_tracks(None)
print(tracks.duration)
# backup_all_playlists(playlists)

# print(f'api calls: {sp.api_calls}')
 