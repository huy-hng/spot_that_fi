from sqlalchemy.orm import Session as sess

from .db_helpers import does_exist
from .tables import Track
from . import Session 


#region create
def add_track(session: Session, track: dict):
	""" adds a single track to db (if not already)
			and returns it """
	row = Track(track)

	if does_track_exist(row.id):
		row: Track = session.query(Track).get(row.id)
	else:
		session.add(row)

	return row


def add_tracks(tracks: list[dict], liked=False) -> Track:
	""" adds a (liked) track to the database (if not already) """
	with Session.begin() as session:
		session: sess = session
		for track in tracks:
			row = add_track(session, track)
			row.liked = liked
#endregion create


#region read
def does_track_exist(track_id: str):
	with Session.begin() as session:
		q = session.query(Track).filter(Track.id == track_id)
		return does_exist(q)


def get_liked_tracks_not_in_playlists() -> list[str]:
	""" returns a list of track ids """
	with Session.begin() as session:
		session: sess = session

		q = session.query(Track).filter(~Track.playlists.any()).all()
		ids = [track.id for track in q]
		return ids


def get_not_liked_tracks() -> list[str]:
	""" returns a list of track ids """
	with Session.begin() as session:
		session: sess = session

		q = session.query(Track).filter(Track.liked == False).all()
		ids = [track.name for track in q]
		return ids
#endregion read


#region update
#endregion update


#region delete
#endregion delete