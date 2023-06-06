from src import db, log, exceptions

from src.db import _, get_session
from src.db.tables import PlaylistTracksTable, PlaylistTable
from src.types.playlists import PlaylistTrackItem, PlaylistType


#------------------------------------------------get------------------------------------------------

@get_session
def get_playlist(playlist_id: str, *, session=_) -> PlaylistTable:
	print(session)
	return session.query(PlaylistTable).get(playlist_id)


@get_session
def get_playlists(*, session=_) -> list[PlaylistTable]:
	''' returns a list with playlist ids '''
	q = session.query(PlaylistTable).all()
	return q


@get_session
def get_playlist_ids(*, session=_) -> list[str]:
	''' returns a list with playlist ids '''
	q = get_playlists(session=session)
	return [playlist.id for playlist in q]

#------------------------------------------------add------------------------------------------------

@get_session
def add_playlist(playlist: PlaylistType, *, session=_):
	if does_playlist_exist(playlist.id):
		return
	row = PlaylistTable(playlist)
	session.add(row)
	return row


@get_session
def add_playlists(playlists: list[PlaylistType]):
	for playlist in playlists:
		add_playlist(playlist)

#----------------------------------------------update-----------------------------------------------

@get_session
def update_playlist(playlist: PlaylistType):
	'''
	this function updates a playlist in the db
	it updates the playlist length, snapshot, etc
	'''
	db_playlist: PlaylistTable = get_playlist(playlist.id)

	if db_playlist is None:
		add_playlist(playlist)
		return

	db_playlist.update(playlist)

#----------------------------------------------delete-----------------------------------------------

@get_session
def delete_playlist(playlist_id: str, *, session=_):
	q = session.query(PlaylistTable).filter_by(id=playlist_id)
	q.delete()


@get_session
def get_id_from_name(playlist_name: str, *, session=_) -> str:
	playlist: PlaylistTable | None = session.query(PlaylistTable).filter(
		PlaylistTable.name == playlist_name).first()

	if playlist is None:
		raise exceptions.PlaylistNotFoundError(playlist_name)

	return playlist.id


@get_session
def get_playlist_snapshot_id(playlist_id: str):
	playlist: PlaylistTable = get_playlist(playlist_id)
	if playlist is None:
		return None
		# raise PlaylistNotFoundError()
	return playlist.snapshot_id


@get_session
def does_playlist_exist(playlist_id: str):
	playlist = get_playlist(playlist_id)
	return playlist is not None

#------------------------------------------playlist tracks------------------------------------------

@get_session
def add_tracks_to_playlist(playlist_id: str, tracks: list[PlaylistTrackItem], *, session=_):
	playlist: PlaylistTable = session.query(PlaylistTable).get(playlist_id)

	if playlist is None:
		...


	for track in tracks:
		try:
			if is_track_in_playlist(playlist.id, track.track.id):
				log.debug(f'{track.track.name} is already in {playlist.name}')
				continue
		except Exception as e:

			log.exception(e)  # TODO find out what this error is
			log.error(f'Not sure what this error is.')
			log.error(f'{playlist}, {track}')
			continue

		row = db.tracks.add_track(track.track)
		if row is None or row.id is None:
			continue

		association = PlaylistTracksTable(track)
		association.track = row
		association.playlist = playlist
		playlist.tracks.append(association)

		session.add(association)

		log.debug(f'Adding {row.name} to {playlist.name}')


@get_session
def get_track_property(playlist_id: str, property: str) -> list[str]:
	playlist = get_playlist(playlist_id)
	if playlist is None:
		return []

	track_item = playlist.tracks
	track_item.sort(key=lambda x: x.added_at)

	filtered: list[str] = [item[property] for item in track_item]
	return filtered

@get_session
def get_track_ids(playlist_id: str) -> list[str]:
	''' returns a list with track_ids sorted by added_at (time) '''
	return get_track_property(playlist_id, 'track_id')

@get_session
def get_track_names(playlist_id: str):
	''' returns a list with track_ids sorted by added_at (time) '''
	return get_track_property(playlist_id, 'name')


@get_session
def get_playlist_track(playlist_id: str, track_id: str, *, session=_):
	return session.query(PlaylistTracksTable).filter(
            PlaylistTracksTable.track_id == track_id,
            PlaylistTracksTable.playlist_id == playlist_id)


@get_session
def is_track_in_playlist(playlist_id: str, track_id: str):
	q = get_playlist_track(playlist_id, track_id)
	return db.utils.does_exist(q)


@get_session
def remove_tracks_from_playlist(playlist_id: str, items: list[str]):
	# TODO: if track has no assocation with any playlists anymore
	# and also isnt liked, delete
	for item in items:
		q = get_playlist_track(playlist_id, item)
		q.delete()
