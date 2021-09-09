import time
# pylint: disable=logging-fstring-interpolation
from logger import log

def restore(sp):
	playlist_to_restore = 'spotify:playlist:48tPqcYezzxCJfEZdQiuEj'
	backup = 'spotify:playlist:7uuUFU3ZPeldfEjKJ94jwX'

	amount_tracks = sp.playlist_items(backup)['total']

	position = 0
	for offset in range(0, amount_tracks, 100):
		# print(offset)
		offset = amount_tracks - (offset + 100)
		if offset < 0:
			offset = 0
		print(offset)
		tracks = sp.playlist_items(backup, offset=offset, fields='items')['items']
		tracks.reverse()

		for track in tracks:
			log.debug(f"{track['track']['name']}")
			sp.playlist_add_items(playlist_to_restore, [track['track']['id']], position=position)
			position += 1
			time.sleep(1)