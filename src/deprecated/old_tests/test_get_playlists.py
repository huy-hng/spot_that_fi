from os import read
from src import api
from src.helpers.logger import log
from src.helpers.helpers import write_dict_to_file, read_dict_from_file
from src.types.playlists import PlaylistType


def test_get_playlists():
	# playlists = sp.get_all_playlists()
	playlists = read_dict_from_file('playlists')
	playlists = [PlaylistType(playlist) for playlist in playlists]

	for playlist in playlists:
		if playlist.owner.id == 'slaybesh':
			log.info(playlist.name)
			log.info(playlist.tracks.href)
			break


def test_get_single_playlist():
	playlist = api.get_one_playlist('2OBconDUKoGs6BoDTVMVvk')
	log.info(playlist.tracks.items[0].added_at)
	# write_dict_to_file('temp', playlist)