from src.api_handler import sp
from src.helpers.logger import log
from src.helpers.helpers import write_dict_to_file, read_dict_from_file


def test_get_tracks():
	gen = sp.get_playlist_tracks_generator('2OBconDUKoGs6BoDTVMVvk')
	for batch in gen:
		log.info(batch)