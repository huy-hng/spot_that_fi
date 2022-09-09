from sqlalchemy.orm import Session as Session
from src import db
from src.db import _, get_session
from src.db.tables import PlaylistAssociation, PlaylistTable
from src.helpers.exceptions import PlaylistNotFoundError
from src.helpers.logger import log
from src.types.playlists import PlaylistTrackItem, PlaylistType


@get_session
def get_playlist(playlist_id: str, *, session: Session = _) -> PlaylistTable:
	return session.query(PlaylistTable).get(playlist_id)


@get_session
def get_playlists(*, session: Session = _) -> list[PlaylistTable]:
	""" returns a list with playlist ids """
	q = session.query(PlaylistTable).all()
	return q


@get_session
def get_playlist_ids(*, session: Session = _) -> list[str]:
	""" returns a list with playlist ids """
	q = get_playlists(session=session)
	return [playlist.id for playlist in q]


@get_session
def add_playlist(playlist: PlaylistType, *, session: Session = _):
	row = PlaylistTable(playlist)
	session.add(row)


@get_session
def add_playlists(playlists: list[PlaylistType], *, session: Session = _):
	for playlist in playlists:

		row = PlaylistTable(playlist)
		session.add(row)


@get_session
def update_playlist(playlist: PlaylistType, *, session: Session = _):
	""" this function updates a playlist in the db
		it updates the playlist length, snapshot, etc """
	playlist = get_playlist(playlist.id, session=session)
	if playlist is None:
		raise PlaylistNotFoundError()
	playlist.update(playlist)


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

	playlist = session.query(PlaylistTable).filter(
		PlaylistTable.id == playlist_id)

	# if playlist is None:
	# 	return

	playlist.delete()


@get_session
def get_id_from_name(playlist_name: str, *, session: Session = _) -> str:
	playlist: PlaylistTable | None = session.query(PlaylistTable).filter(
		PlaylistTable.name == playlist_name).first()

	if playlist is None:
		raise PlaylistNotFoundError(playlist_name)

	return playlist.id


@get_session
def get_playlist_snapshot_id(playlist_id: str, *, session: Session = _):
	playlist = get_playlist(playlist_id, session=session)
	if playlist is None:
		raise PlaylistNotFoundError()
	return playlist.snapshot_id


@get_session
def does_playlist_exist(playlist_id: str, *, session: Session = _):
	playlist = get_playlist(playlist_id, session=session)
	return playlist is not None


@get_session
def add_tracks_to_playlist(playlist_id: str, tracks: list[PlaylistTrackItem], *, session: Session = _):
	playlist: PlaylistTable = session.query(PlaylistTable).get(playlist_id)

	for track in tracks:

		row = db.tracks.add_track(track.track, session=session)
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


@get_session
def get_track_ids(playlist_id: str, *, session: Session = _):
	""" returns a list with track_ids sorted by added_at (time) """
	playlist = get_playlist(playlist_id, session=session)
	if playlist is None:
		raise PlaylistNotFoundError()
	associations = playlist.tracks
	associations.sort(key=lambda x: x.added_at)

	track_ids: list[str] = [ass.track_id for ass in associations]
	return track_ids


@get_session
def get_track_names(playlist_id: str, *, session: Session = _):
	""" returns a list with track_ids sorted by added_at (time) """
	playlist = get_playlist(playlist_id, session=session)
	if playlist is None:
		raise PlaylistNotFoundError()

	associations = playlist.tracks
	associations.sort(key=lambda x: x.added_at)

	return [ass.track.name for ass in associations]


@get_session
def is_track_in_playlist(playlist_id: str, track_id: str, *, session: Session = _):
	q = get_playlist_track(playlist_id, track_id, session=session)
	return db.helpers.does_exist(q, session=session)


@get_session
def get_playlist_track(
        playlist_id: str,
        track_id: str, *, session: Session = _):

	return session.query(PlaylistAssociation).filter(
            PlaylistAssociation.track_id == track_id,
            PlaylistAssociation.playlist_id == playlist_id)


@get_session
def remove_tracks_from_playlist(playlist_id: str, items: list[str], *, session: Session = _):
	# TODO: if track has no assocation with any playlists anymore
	# and also isnt liked, delete
	for item in items:
		q = get_playlist_track(playlist_id, item, session=session)
		q.delete()
