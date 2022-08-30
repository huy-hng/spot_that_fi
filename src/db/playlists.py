from sqlalchemy.orm import Session as Session
from src.types.playlists import AllPlaylists, PlaylistTracksItem, SinglePlaylist

from src.helpers.exceptions import PlaylistNotFoundError
from .helpers import does_exist
from .tracks import add_track
from .tables import Playlist, PlaylistTracksAssociation
from src.db import tables, engine
# from . import Session 

from src.helpers.logger import log

#region playlist functions

# creates
def _get_playlist(session: Session, playlist_id: str):
	playlist: tables.Playlist = session.query(tables.Playlist).get(playlist_id)
	
	if playlist is None:
		raise PlaylistNotFoundError(playlist_id)

	return playlist

def _add_playlist(session: Session, playlist: AllPlaylists | SinglePlaylist):
	row = tables.Playlist(playlist)
	session.add(row)

def _update_playlist(session: Session, playlist: AllPlaylists | SinglePlaylist):
	""" this function updates a playlist in the db
			it updates the playlist length, snapshot, etc """
	db_playlist = _get_playlist(session, playlist.id)
	db_playlist.update(playlist) # TODO: check if this actually updates


def update_playlists(playlists: list[AllPlaylists]):
	""" adds or updates spotify playlist in db """
	with Session(engine) as session:
		for playlist in playlists:
			if playlist.owner.id != 'slaybesh':
				log.debug(f'Playlist {playlist.name} belong to you.')

			elif does_playlist_exist(playlist.id):
				log.info(f'Updating playlist: {playlist.name}')
				_update_playlist(session, playlist)

			else:
				log.info(f'Adding playlist: {playlist.name}')
				_add_playlist(session, playlist)


# reads
def get_all_playlists() -> list[str]: 
	""" returns a list with playlist ids """
	with Session(engine) as session:
		q = session.query(tables.Playlist).all()
		return [playlist.id for playlist in q]



def get_id_from_name(playlist_name: str) -> str:
	with Session(engine) as session:
		playlist: tables.Playlist | None = session.query(tables.Playlist).filter(
			tables.Playlist.name == playlist_name).first()

		if playlist is None:
			raise PlaylistNotFoundError(playlist_name)

		return playlist.id


def get_playlist_snapshot_id(playlist_id: str):
	with Session(engine) as session:
		playlist = _get_playlist(session, playlist_id)
		return playlist.snapshot_id


def does_playlist_exist(playlist_id: str):
	with Session(engine) as session:
		try:
			_get_playlist(session, playlist_id)
		except PlaylistNotFoundError:
			return False
		return True



""" def update_playlist_snapshot(playlist_id: str, snapshot_id: str):
	with Session.begin() as session:
		playlist = get_playlist(session, playlist_id)
		playlist.snapshot_id = snapshot_id """
#endregion playlist functions


#region tracks functions

# creates
def	add_tracks_to_playlist(playlist_id: str, tracks: list[PlaylistTracksItem]):
	with Session(engine) as session:
		playlist: tables.Playlist = session.query(tables.Playlist).get(playlist_id)

		for track in tracks:

			row = add_track(session, track.track)
			if row is None or row.id is None:
				continue

			try:
				if is_track_in_playlist(session, playlist.id, row.id):
					log.debug(f'{row.name} is already in {playlist.name}')
					continue
			except Exception as e:
				log.exception(e) # TODO find out what this error is
				log.error(f'Not sure what this error is.')
				continue

			association = PlaylistTracksAssociation(track)
			association.track = row
			association.playlist = playlist
			playlist.playlist_track_association.append(association)

			session.add(association)

			log.debug(f'Adding {row.name} to {playlist.name}')

# reads
def get_track_ids(playlist_id: str):
	""" returns a list with track_ids sorted by added_at (time) """
	with Session(engine) as session:
		playlist = _get_playlist(session, playlist_id)

		associations = playlist.playlist_track_association
		associations.sort(key=lambda x: x.added_at)

		track_ids: list[str] = [ass.track_id for ass in associations]
		return track_ids


def get_track_names(playlist_id: str):
	""" returns a list with track_ids sorted by added_at (time) """
	with Session(engine) as session:
		playlist = _get_playlist(session, playlist_id)
		associations = playlist.playlist_track_association
		associations.sort(key=lambda x: x.added_at)
		track_names: list[str] = []
		for ass in associations:
			track_names.append(ass.track.name)
		return track_names


def is_track_in_playlist(session: Session, playlist_id: str, track_id: str):
	q = get_PlaylistTracksAssociation(session, playlist_id, track_id)
	return does_exist(q)

def get_PlaylistTracksAssociation(
		session: Session,
		playlist_id: str,
		track_id: str):

	return session.query(PlaylistTracksAssociation).filter(
			PlaylistTracksAssociation.track_id == track_id,
			PlaylistTracksAssociation.playlist_id == playlist_id)


# deletes
def remove_tracks_from_playlist(playlist_id: str, items: list[PlaylistTracksItem]):
	with Session(engine) as session:
		# TODO: if track has no assocation with any playlists anymore 
		# and also isnt liked, delete
		for item in items:
			q = get_PlaylistTracksAssociation(session, playlist_id, item.track.id)
			q.delete()
#endregion tracks functions

