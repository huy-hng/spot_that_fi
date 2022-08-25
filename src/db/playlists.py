from sqlalchemy import delete
from sqlalchemy.orm import Session as sess
# from src.helpers.data_types import SpotifyPlaylistType
from src.types.playlists import SpotifyPlaylistType

from src.helpers.exceptions import PlaylistNotFoundError
from .helpers import does_exist
from .tracks import add_track
from .tables import Playlist, PlaylistTracksAssociation
from src.db import tables, get_session
# from . import Session 

from src.helpers.logger import log

#region playlist functions

# creates
@get_session
def add_playlists(session: sess, playlists: list[SpotifyPlaylistType]):
	""" adds spotify playlist to db
			if playlists already exist, skip """
	for playlist in playlists:
		row = tables.Playlist(playlist)

		if not does_playlist_exist(row.id) and row.owner_id == 'slaybesh':
			log.info(f'Adding playlist: {row.name}')
			session.add(row)
		else:
			log.debug(f'Playlist {row.name} already exists or doesnt belong to you.')


# reads
@get_session
def get_all_playlists(session: sess) -> list[str]: 
	""" returns a list with playlist ids """
	q = session.query(tables.Playlist).all()
	return [playlist.id for playlist in q]


def get_playlist(session: sess, playlist_id: str):
	playlist = session.query(tables.Playlist).get(playlist_id)
	
	if playlist is None:
		raise PlaylistNotFoundError(playlist_id)

	return playlist


@get_session
def get_id_from_name(session: sess, playlist_name: str) -> str:
	# playlist: tables.Playlist = session.query(tables.Playlist).filter(tables.Playlist.name == playlist_name).first()
	playlist = session.query(tables.Playlist).filter(tables.Playlist.name == playlist_name).first()
	
	if playlist is None:
		raise PlaylistNotFoundError(playlist_name)

	return playlist.id


@get_session
def get_playlist_snapshot_id(session: sess, playlist_id: str):
	playlist = get_playlist(session, playlist_id)
	return playlist.snapshot_id


@get_session
def does_playlist_exist(session: sess,playlist_id: str):
	q = session.query(tables.Playlist).get(playlist_id)
	if q is None:
		return False
	return True


# updates
@get_session
def update_playlist(session: sess, live_playlist: SpotifyPlaylistType):
	""" this function updates a playlist in the db
			it updates the playlist length, snapshot, etc """
	db_playlist = get_playlist(session, live_playlist.id)
	db_playlist.update(live_playlist) # TODO: check if this actually updates


""" def update_playlist_snapshot(playlist_id: str, snapshot_id: str):
	with Session.begin() as session:
		playlist = get_playlist(session, playlist_id)
		playlist.snapshot_id = snapshot_id """
#endregion playlist functions


#region tracks functions

# creates
@get_session
def	add_tracks_to_playlist(session: sess, playlist_id: str, tracks: list[dict]):
	playlist: tables.Playlist = session.query(tables.Playlist).get(playlist_id)

	for track in tracks:

		row = add_track(session, track)
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
@get_session
def get_track_ids(session: sess, playlist_id: str):
	""" returns a list with track_ids sorted by added_at (time) """
	playlist = get_playlist(session, playlist_id)

	associations = playlist.playlist_track_association
	associations.sort(key=lambda x: x.added_at)

	track_ids: list[str] = [ass.track_id for ass in associations]
	return track_ids


@get_session
def get_track_names(session: sess, playlist_id: str):
	""" returns a list with track_ids sorted by added_at (time) """
	playlist = get_playlist(session, playlist_id)
	associations = playlist.playlist_track_association
	associations.sort(key=lambda x: x.added_at)
	track_names: list[str] = []
	for ass in associations:
		track_names.append(ass.track.name)
	return track_names


def is_track_in_playlist(session: sess, playlist_id: str, track_id: str):
	q = session.query(PlaylistTracksAssociation).filter(
										PlaylistTracksAssociation.track_id == track_id,
										PlaylistTracksAssociation.playlist_id == playlist_id)
	return does_exist(q)


# deletes
@get_session
def remove_tracks_from_playlist(session: sess, playlist_id: str, tracks: list[str]):
	# with Session.begin() as session:
	# TODO: if track has no assocation with any playlists anymore 
	# and also isnt liked, delete
	for track_id in tracks:
		session.query(PlaylistTracksAssociation).filter(
				PlaylistTracksAssociation.track_id == track_id,
				PlaylistTracksAssociation.playlist_id == playlist_id).delete()
#endregion tracks functions

