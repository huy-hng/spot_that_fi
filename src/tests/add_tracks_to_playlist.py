from src import sp
from src.playlists.live_playlists import LivePlaylists

track_id = '4mQTPwMKPNLGODbonuGCtP'
playlist_uri = 'spotify:playlist:063Tra4gBrn9kOf0kZQiIT'
playlists = LivePlaylists()
playlist = playlists.get_by_name('Archive Playlist')

sp.add_tracks_at_end(playlist.uri, [track_id], playlist.tracks_in_playlist)