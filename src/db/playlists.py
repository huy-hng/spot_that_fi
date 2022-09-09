from sqlalchemy.orm import Session as Session
from src.types.playlists import PlaylistType, PlaylistTrackItem, PlaylistType

from src.helpers.exceptions import PlaylistNotFoundError
from .helpers import does_exist
from .tracks import add_track
from .tables import Playlist, PlaylistAssociation
from src.db import tables, get_session, _

from src.helpers.logger import log


@get_session
def nested_session(playlist, *, session: Session = _):
	""" returns a list with playlist ids """

	add_playlist(playlist)

	q = session.query(tables.Playlist).all()
	ids = [playlist.id for playlist in q]
	assert playlist.id in ids

	q = get_playlist(playlist.id, session=session)
	assert playlist.id == q.id


@get_session
def get_playlist(playlist_id: str, *, session: Session = _):
	playlist: tables.Playlist = session.query(tables.Playlist).get(playlist_id)

	if playlist is None:
		raise PlaylistNotFoundError(playlist_id)

	return playlist


@get_session
def get_playlists(*, session: Session = _) -> list[tables.Playlist]:
	""" returns a list with playlist ids """
	q = session.query(tables.Playlist).all()
	return q


@get_session
def get_playlist_ids(*, session: Session = _) -> list[str]:
	""" returns a list with playlist ids """
	q = session.query(tables.Playlist).all()
	return [playlist.id for playlist in q]


@get_session
def add_playlist(playlist: PlaylistType, *, session: Session = _):
	row = tables.Playlist(playlist)
	session.add(row)


@get_session
def add_playlists(playlists: list[PlaylistType], *, session: Session = _):
	for playlist in playlists:
		row = tables.Playlist(playlist)
		session.add(row)


@get_session
def update_playlist(playlist: PlaylistType, *, session: Session = _):
	""" this function updates a playlist in the db
		it updates the playlist length, snapshot, etc """
	db_playlist = get_playlist(playlist.id, session=session)
	db_playlist.update(playlist)


@get_session
def update_playlists(playlists: list[PlaylistType], *, session: Session = _):
	""" adds or updates spotify playlist in db """
	for playlist in playlists:
		# FIX: remove hardcoded name below
		if playlist.owner.id != 'slaybesh':
			log.debug(f'Playlist {playlist.name} belong to you.')

		elif does_playlist_exist(playlist.id):
			log.info(f'Updating playlist: {playlist.name}')
			update_playlist(playlist, session=session)

		else:
			log.info(f'Adding playlist: {playlist.name}')
			add_playlist(playlist)


@get_session
def delete_playlist(playlist_id: str, *, session: Session = _):

	playlist = session.query(tables.Playlist).filter(Playlist.id == playlist_id)

	# if playlist is None:
	# 	return

	playlist.delete()


@get_session
def get_id_from_name(playlist_name: str, *, session: Session = _) -> str:
	playlist: tables.Playlist | None = session.query(tables.Playlist).filter(
		tables.Playlist.name == playlist_name).first()

	if playlist is None:
		raise PlaylistNotFoundError(playlist_name)

	return playlist.id


@get_session
def get_playlist_snapshot_id(playlist_id: str, *, session: Session = _):
	playlist = get_playlist(playlist_id, session=session)
	return playlist.snapshot_id


@get_session
def does_playlist_exist(playlist_id: str, *, session: Session = _):
	try:
		get_playlist(playlist_id, session=session)
	except PlaylistNotFoundError:
		return False
	return True


# endregion playlist functions


# region tracks functions

# creates
@get_session
def add_tracks_to_playlist(playlist_id: str, tracks: list[PlaylistTrackItem], *, session: Session = _):
	playlist: tables.Playlist = session.query(tables.Playlist).get(playlist_id)

	for track in tracks:

		row = add_track(track.track, session=session)
		if row is None or row.id is None:
			continue

		try:
			if is_track_in_playlist(playlist.id, row.id, session=session):
				log.debug(f'{row.name} is already in {playlist.name}')
				continue
		except Exception as e:
			log.exception(e)  # TODO find out what this error is
			log.error(f'Not sure what this error is.')
			continue

		association = PlaylistAssociation(track)
		association.track = row
		association.playlist = playlist
		playlist.tracks.append(association)

		session.add(association)

		log.debug(f'Adding {row.name} to {playlist.name}')

# reads


@get_session
def get_track_ids(playlist_id: str, *, session: Session = _):
	""" returns a list with track_ids sorted by added_at (time) """
	playlist = get_playlist(playlist_id, session=session)
	associations = playlist.tracks
	associations.sort(key=lambda x: x.added_at)

	track_ids: list[str] = [ass.track_id for ass in associations]
	return track_ids


@get_session
def get_track_names(playlist_id: str, *, session: Session = _):
	""" returns a list with track_ids sorted by added_at (time) """
	playlist = get_playlist(playlist_id, session=session)
	
	associations = playlist.tracks
	associations.sort(key=lambda x: x.added_at)

	return [ass.track.name for ass in associations]


@get_session
def is_track_in_playlist(playlist_id: str, track_id: str, *, session: Session = _):
	q = get_playlist_tracks(playlist_id, track_id, session=session)
	return does_exist(q, session=session)


@get_session
def get_playlist_tracks(
        playlist_id: str,
        track_id: str, *, session: Session = _):

	return session.query(PlaylistAssociation).filter(
            PlaylistAssociation.track_id == track_id,
            PlaylistAssociation.playlist_id == playlist_id)


# deletes
@get_session
def remove_tracks_from_playlist(playlist_id: str, items: list[str], *, session: Session = _):
	# TODO: if track has no assocation with any playlists anymore
	# and also isnt liked, delete
	for item in items:
		q = get_playlist_tracks(playlist_id, item, session=session)
		q.delete()
# endregion tracks functions
