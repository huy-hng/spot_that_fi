from src.api import sp
from src.helpers.logger import log
from src.helpers.helpers import write_dict_to_file


def test_get_liked_tracks():
	gen = sp.get_liked_tracks_generator()
	for batch in gen:
		log.info(batch.items_[0].track.name)
		# write_dict_to_file('liked_tracks', batch)
		# log.debug(batch)
		break