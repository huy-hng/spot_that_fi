from datetime import datetime, timedelta

from sqlalchemy.orm import Session
from src.db import _, get_session
from src.db.tables import PlaylistTable

@get_session
def get_latest_tracks_added_to_playlists(days_old=14, *, session: Session = _):
	""" returns a list with track_ids that
		have been recently added to playlists """

	playlists = session.query(PlaylistTable).all()
	# playlists = 

	latest_tracks: list[str] = []  # list with track_ids
	oldest_time = datetime.now() - timedelta(days=days_old)
	for playlist in playlists:
		tracks = playlist.playlist_track_association
		for track in tracks:
			if track.added_at > oldest_time:
				latest_tracks.append(track.track.id)

	return latest_tracks


@get_session
def remove_unliked_tracks_not_in_playlists(*, session: Session = _):
	""" remove tracks from db that aren't liked and
		also don't belong to any playlists. """
