from functools import wraps

from sqlalchemy import literal
from sqlalchemy.orm import Session as sess

from src.database import Session 
from src.database.tables import Playlist, PlaylistTrack, PlaylistTracksAssociation

from src.logger import log


# def create_session(function):
# 	@wraps(function)
# 	def wrapper(*args, **kwargs):
# 		with Session.begin() as session:
# 			session: sess = session
# 			result = function(session, *args, **kwargs)
# 		return result
# 	return wrapper

def is_track_in_playlist(playlist_id: str, track_id: str):
	with Session.begin() as session:
		session: sess = session

		q = session.query(PlaylistTracksAssociation).filter(
				PlaylistTracksAssociation.c.track_id == track_id,
				PlaylistTracksAssociation.c.playlist_id == playlist_id)

		exists = session.query(literal(True)).filter(q.exists()).scalar()
		return exists if exists else False


def add_playlists(playlists: list[dict]):
	with Session.begin() as session:
		for playlist in playlists:
			row = Playlist(playlist)

			q = session.query(Playlist).filter(Playlist.id == row.id)

			if not session.query(q.exists()) and row.owner_id == 'slaybesh':
				session.add(row)


def	add_tracks_to_playlist(playlist_id: str, tracks: list[dict]):
	with Session.begin() as session:
		session: sess = session
		playlist: Playlist = session.query(Playlist).get(playlist_id)
		for track in tracks:
			row = PlaylistTrack(track)

			if not is_track_in_playlist(playlist.id, row.id):
				playlist.tracks.append(row)
				session.add(row)
				log.debug(f'Adding {row.name} to {playlist.name}')
			else:
				log.debug(f'{row.name} is already in {playlist.name}')
