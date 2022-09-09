from src.db.session import _, get_session
from src.db.tables import TrackTable
from src.types.tracks import LikedTrackItem, TrackDict


@get_session
def get_track(track_id: str, *, session=_) -> TrackTable:
	""" returns db object bound to a session

		if track_id doesn't exist, None is returned """
	return session.query(TrackTable).get(track_id)


@get_session
def add_track(track: TrackDict, *, session=_) -> TrackTable | None:
	""" adds a single track to db (if not already)
			and returns it """
	if track.is_local:
		return

	t = get_track(track.id)
	if t is not None:
		return t

	row = TrackTable(track)
	if row.id is None:  # TODO whats this case?
		# this case might be when its a local song that is not on spotify servers
		# and therefore has no id
		return None

	session.add(row)
	return row


@get_session
def add_tracks(tracks: list[TrackDict]):
	""" adds a (liked) track to the database (if not already) """
	for track in tracks:
		add_track(track)


@get_session
def like_tracks(tracks: list[LikedTrackItem]):
	for track in tracks:
		like_track(track)


@get_session
def like_track(track: LikedTrackItem):
	row = add_track(track.track)
	if row is not None:
		row.liked_at = track.added_at


@get_session
def unlike_tracks(track_ids: list[str]):
	for id in track_ids:
		unlike_track(id)


@get_session
def unlike_track(track_id: str):
	row: TrackTable = get_track(track_id)
	if row is not None:
		row.liked_at = None
# region read


@get_session
def does_track_exist(track_id: str):
	track = get_track(track_id)
	return track is not None


@get_session
def get_liked_tracks(*, session=_) -> list[str]:
	q: list[TrackTable] = session.query(
		TrackTable).filter(TrackTable.liked == True).all()
	return [track.id for track in q]


@get_session
def get_liked_tracks_not_in_playlists(*, session=_) -> list[str]:
	""" returns a list of track ids that are liked but not in any playlist. """

	# TODO: Track.liked == True filter is not necessary if all
	# unliked tracks arent in the db
	q: list[TrackTable] = session.query(TrackTable).filter(
		TrackTable.liked == True and ~TrackTable.playlist_track_association.any()  # type: ignore
	).all()
	ids = [track.id for track in q]
	return ids


@get_session
def get_not_liked_tracks_in_playlists(*, session=_) -> list[str]:
	""" returns a list of track ids that are in playlists but not liked """
	q: list[TrackTable] = session.query(TrackTable).filter(
		TrackTable.liked == False and TrackTable.playlist_track_association.any()  # type: ignore
	).all()
	ids = [track.name for track in q]
	return ids
# endregion read


# region update
# endregion update


# region delete
# endregion delete
