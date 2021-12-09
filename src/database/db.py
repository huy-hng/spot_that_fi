from functools import wraps

from sqlalchemy import literal
from sqlalchemy.orm import Session as sess
from sqlalchemy.orm.query import Query

from src.database import Session 
from src.database.tables import Playlist, Track, PlaylistTracksAssociation

from src.logger import log


# def create_session(function):
# 	@wraps(function)
# 	def wrapper(*args, **kwargs):
# 		with Session.begin() as session:
# 			session: sess = session
# 			result = function(session, *args, **kwargs)
# 		return result
# 	return wrapper

def does_exist(query: Query):
	with Session.begin() as session:
		exists = session.query(literal(True)).filter(query.exists()).scalar()
		return exists if exists else False


def is_track_in_playlist(playlist_id: str, track_id: str):
	with Session.begin() as session:
		session: sess = session

		q = session.query(PlaylistTracksAssociation).filter(
				PlaylistTracksAssociation.track_id == track_id,
				PlaylistTracksAssociation.playlist_id == playlist_id)

		return does_exist(q)


def does_track_exist(track_id: str):
	with Session.begin() as session:
		q = session.query(Track).filter(Track.id == track_id)
		return does_exist(q)


def does_playlist_exist(playlist_id: str):
	with Session.begin() as session:
		q = session.query(Playlist).filter(Playlist.id == playlist_id)
		return does_exist(q)


def add_playlists(playlists: list[dict]):
	with Session.begin() as session:
		for playlist in playlists:
			row = Playlist(playlist)

			if not does_playlist_exist(row.id) and row.owner_id == 'slaybesh':
				log.info(f'Adding playlist: {row.name}')
				session.add(row)
			else:
				log.debug(f'Playlist {row.name} already exists or doesnt belong to me')


def	add_tracks_to_playlist(playlist_id: str, tracks: list[dict]):
	with Session.begin() as session:
		session: sess = session
		playlist: Playlist = session.query(Playlist).get(playlist_id)
		for track in tracks:
			row = Track(track)

			if does_track_exist(row.id):
				row = session.query(Track).get(row.id)
			else:
				session.add(row)

			if is_track_in_playlist(playlist.id, row.id):
				log.debug(f'{row.name} is already in {playlist.name}')
				return

			association = PlaylistTracksAssociation(track)
			association.track = row
			association.playlist = playlist
			playlist.tracks.append(association)

			session.add(association)

			log.debug(f'Adding {row.name} to {playlist.name}')


def add_tracks(tracks: list[dict]):
	with Session.begin() as session:
		session: sess = session
		for track in tracks:
			row = Track(track)

			if not does_track_exist(row.id):
				session.add(row)


def get_liked_tracks_not_in_playlists():
	with Session.begin() as session:
		session: sess = session
		for track, association in session.query(Track, PlaylistTracksAssociation).filter(
			Track.id == PlaylistTracksAssociation.track_id).all():
			print(track.name, association)

