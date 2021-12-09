from datetime import datetime
from sqlalchemy import Column, String, Integer, Boolean, DateTime
from sqlalchemy.sql.schema import ForeignKey, Table
from sqlalchemy.orm import relationship

from src.database import Base


class PlaylistTracksAssociation(Base):
	__tablename__ = 'playlist_tracks_association'

	playlist_id = Column(ForeignKey('playlist.id'), primary_key=True)
	track_id = Column(ForeignKey('track.id'), primary_key=True)
	track = relationship('Track', back_populates='playlists')
	playlist = relationship('Playlist', back_populates='tracks')

	added_by = Column(String, nullable=False)
	added_at = Column(String, nullable=False)

	def __init__(self, track):
		self.added_at = datetime.strptime(track['added_at'], '%Y-%m-%dT%H:%M:%SZ')
		self.added_by = track['added_by']['id']


class Playlist(Base):
	__tablename__ = 'playlist'

	id = Column(String, primary_key=True)
	name = Column(String, nullable=False)
	total_tracks = Column(Integer, nullable=False)
	public = Column(Boolean, nullable=False)
	snapshot_id = Column(String, nullable=False)
	owner_id = Column(String, nullable=False)

	tracks: relationship = relationship('PlaylistTracksAssociation',
			back_populates='playlist')

	def __init__(self, playlist) -> None:
		self.id = playlist['id']
		self.name = playlist['name']
		self.total_tracks = playlist['tracks']['total']
		self.public = playlist['public']
		self.snapshot_id = playlist['snapshot_id']
		self.owner_id = playlist['owner']['id']


class Track(Base):
	__tablename__ = 'track'

	id = Column(String, primary_key=True)
	name = Column(String, nullable=False)
	duration_ms = Column(Integer, nullable=False)
	popularity = Column(Integer, nullable=False)

	playlists: relationship = relationship('PlaylistTracksAssociation',
				back_populates='track')

	def __init__(self, track: dict):
		self.id = track['track']['id']
		self.name = track['track']['name']
		self.duration_ms = track['track']['duration_ms']
		self.popularity = track['track']['popularity']
