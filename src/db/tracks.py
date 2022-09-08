from sqlalchemy.orm import Session

from src.types.playlists import TrackDict
from .tables import Track
from . import SessionMaker
from src.helpers.logger import log
from src.db import get_session, _


# region create
@get_session
def add_track(track: TrackDict, liked=False, *, session: Session = _) -> Track | None:
	""" adds a single track to db (if not already)
			and returns it """
	row = Track(track)
	if row.id is None:  # TODO whats this case?
		# this case might be when its a local song that is not on spotify servers
		# and therefore has no id
		return None

	if does_track_exist(row.id):
		try:
			row: Track = session.query(Track).get(row.id)
		except Exception as e:
			log.error(row.name)
			return None
	else:
		session.add(row)

	row.liked = liked
	return row


@get_session
def add_tracks(tracks: list[TrackDict], liked=False, *, session: Session = _):
	""" adds a (liked) track to the database (if not already) """
	for track in tracks:
		if track.is_local:
			continue

		add_track(track, liked, session=session)
# endregion create


# region read
@get_session
def get_track(track_id: str, *, session: Session = _):
	return session.query(Track).get(track_id)


@get_session
def does_track_exist(track_id: str, *, session: Session = _):
	q = session.query(Track).get(track_id)

	if q is None:
		return False
	return True


@get_session
def get_liked_tracks(*, session: Session = _) -> list[str]:
	q: list[Track] = session.query(Track).filter(Track.liked == True).all()
	return [track.id for track in q]


@get_session
def get_liked_tracks_not_in_playlists(*, session: Session = _) -> list[str]:
	""" returns a list of track ids that are liked but not in any playlist. """

	# TODO: Track.liked == True filter is not necessary if all
	# unliked tracks arent in the db
	q: list[Track] = session.query(Track).filter(
		Track.liked == True and ~Track.playlist_track_association.any()  # type: ignore
	).all()
	ids = [track.id for track in q]
	return ids


@get_session
def get_not_liked_tracks_in_playlists(*, session: Session = _) -> list[str]:
	""" returns a list of track ids that are in playlists but not liked """
	q: list[Track] = session.query(Track).filter(
		Track.liked == False and Track.playlist_track_association.any()  # type: ignore
	).all()
	ids = [track.name for track in q]
	return ids
# endregion read


# region update
# endregion update


# region delete
# endregion delete
