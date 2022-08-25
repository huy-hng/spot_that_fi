from sqlalchemy.orm import Session as sess

from src import types
from .tables import Track
from . import Session 
from src.helpers.logger import log
from . import get_session


#region create
def add_track(session: sess, track: dict, liked=False) -> Track | None:
	""" adds a single track to db (if not already)
			and returns it """
	row = Track(track)
	if row.id is None: # TODO whats this case?
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
def add_tracks(session: sess, tracks: list[types.tracks.Track], liked=False):
	""" adds a (liked) track to the database (if not already) """
	for track in tracks:
		if track['is_local']:
			continue

		add_track(session, track, liked)
#endregion create


#region read
def get_track(session: sess, track_id: str):
	return session.query(Track).get(track_id)


@get_session
def does_track_exist(session:sess, track_id: str):
	q = session.query(Track).get(track_id)

	if q is None:
		return False
	return True


@get_session
def get_liked_tracks_not_in_playlists(session: sess) -> list[str]:
	""" returns a list of track ids that are liked but not in any playlist"""
	q = session.query(Track).filter(~Track.playlist_track_association.any()).all()
	ids = [track.id for track in q]
	return ids


@get_session
def get_not_liked_tracks_in_playlists(session: sess) -> list[str]:
	""" returns a list of track ids that are in playlists but not liked """
	q = session.query(Track).filter(Track.liked == False).all()
	ids = [track.name for track in q]
	return ids
#endregion read


#region update
#endregion update


#region delete
#endregion delete