from src.db.helpers import does_exist
from src.db.session import _, get_session
from src.db.tables import LikedTable, TrackTable
from src.types.tracks import LikedTrackItem, LikedTrackList, TrackDict


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
def like_tracks(items: list[LikedTrackItem]):
	for item in items:
		like_track(item)


@get_session
def like_track(track: LikedTrackItem, *, session=_):
	track_id = track.track.id
	added_at = track.added_at

	if is_track_liked(track_id):
		return

	add_track(track.track)

	row = LikedTable(track_id, added_at)
	session.add(row)


@get_session
def relike_track(track: LikedTrackItem):
	track_id = track.track.id
	added_at = track.added_at

	liked = get_liked_track(track_id)
	if liked is None:
		return

	liked.added_at = added_at


@get_session
def unlike_tracks(track_ids: list[str]):
	for id in track_ids:
		unlike_track(id)


@get_session
def unlike_track(track_id: str, *, session=_):
	q = session.query(LikedTable).filter_by(track_id=track_id)
	q.delete()


@get_session
def get_liked_track(track_id: str, *, session=_) -> LikedTable:
	return session.query(LikedTable).get(track_id)


@get_session
def get_liked_tracks(*, session=_) -> list[str]:
	# order = LikedTable._added_at  # type: ignore
	order = LikedTable._added_at.desc()  # type: ignore
	order2 = LikedTable.track_id.desc()  # type: ignore
	q: list[LikedTable] = session.query(LikedTable).order_by(order, order2).all()
	return [track.track_id for track in q]
	# return [track.track.name for track in q]


# TODO
def shift_liked_tracks_index():
	pass


@get_session
def is_track_liked(track_id: str):
	liked_track = get_liked_track(track_id)
	return liked_track is not None
# region read


@get_session
def get_len_liked(*, session=_):
	# REFACTOR?
	return session.query(LikedTable).count()


@get_session
def does_track_exist(track_id: str):
	track = get_track(track_id)
	return track is not None


@get_session
def get_liked_tracks_not_in_playlists(*, session=_) -> list[str]:
	""" returns a list of track ids that are liked but not in any playlist. """

	# TODO: Track.liked == True filter is not necessary if all
	# unliked tracks arent in the db
	q: list[TrackTable] = session.query(TrackTable).filter(
		# TrackTable.liked == True and ~TrackTable.playlists.any()  # type: ignore
		~TrackTable.playlists.any()  # type: ignore
	).all()
	ids = [track.id for track in q]
	# ids = [track.name for track in q]
	return ids


@get_session
def get_not_liked_tracks_in_playlists(*, session=_) -> list[str]:
	""" returns a list of track ids that are in playlists but not liked """
	q: list[TrackTable] = session.query(TrackTable).filter(
		TrackTable.liked == False and TrackTable.playlists.any()  # type: ignore
	).all()
	ids = [track.name for track in q]
	return ids
# endregion read


# region update
# endregion update


# region delete
# endregion delete
