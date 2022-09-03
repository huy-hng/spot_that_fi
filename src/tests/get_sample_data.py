from src.tests import PlaylistIDs
from src import api_handler as api
from src.api_handler import sp
from src.controller import playlist_change_detection as pcd

def get_all_playlists():
	sp.get_all_playlists()

def get_one_playlist():
	sp.get_one_playlist('2OBconDUKoGs6BoDTVMVvk')

def get_latest_tracks():
	gen = sp.get_playlist_tracks_generator(PlaylistIDs.main, 20)
	for tracks in gen:
		names = api.playlists.PlaylistHandler.get_names(tracks.items_)
		for name in names:
			print(name)
		break