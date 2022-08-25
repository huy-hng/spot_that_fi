from sqlalchemy.orm import Session

from src import types
from .tables import Track
from . import SessionMaker
from src.helpers.logger import log
from . import get_session


#region create
def add_track(session: Session, track: dict, liked=False) -> Track | None:
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


def add_tracks(tracks: list[types.tracks.TrackDict], liked=False):
	with SessionMaker.begin() as session:
		""" adds a (liked) track to the database (if not already) """
		for track in tracks:
			if track['is_local']:
				continue

			add_track(session, track, liked)
#endregion create


#region read
def get_track(session: Session, track_id: str):
	return session.query(Track).get(track_id)


def does_track_exist(session:Session, track_id: str):
	with SessionMaker.begin() as session:
		q = session.query(Track).get(track_id)

		if q is None:
			return False
		return True


def get_liked_tracks_not_in_playlists(session: Session) -> list[str]:
	with SessionMaker.begin() as session:
		""" returns a list of track ids that are liked but not in any playlist"""
		q = session.query(Track).filter(~Track.playlist_track_association.any()).all()
		ids = [track.id for track in q]
		return ids


def get_not_liked_tracks_in_playlists(session: Session) -> list[str]:
	with SessionMaker.begin() as session:
		""" returns a list of track ids that are in playlists but not liked """
		q = session.query(Track).filter(Track.liked == False).all()
		ids = [track.name for track in q]
		return ids
#endregion read


#region update
#endregion update


#region delete
#endregion delete