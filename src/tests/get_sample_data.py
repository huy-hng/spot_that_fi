from src.tests import PlaylistIDs
from src import api
from src.api import api
from src.controller import playlist_change_detection as pcd

def get_all_playlists():
	api.get_all_playlists()

def get_one_playlist():
	api.get_one_playlist('2OBconDUKoGs6BoDTVMVvk')

def get_latest_tracks():
	gen = api.get_playlist_tracks_generator(PlaylistIDs.main, 20)
	for tracks in gen:
		names = api.PlaylistHandler.get_names(tracks.items_)
		for name in names:
			print(name)
		break