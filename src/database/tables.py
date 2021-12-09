from datetime import datetime
from sqlalchemy import Column, String, Integer, Boolean, DateTime
from sqlalchemy.sql.schema import ForeignKey, Table
from sqlalchemy.orm import relationship

from src.database import Base


PlaylistTracksRelation = Table('PlaylistTracksRelation', Base.metadata,
    Column('playlist_id', ForeignKey('Playlist.id'), primary_key=True),
    Column('track_id', ForeignKey('PlaylistTrack.id'), primary_key=True)
)
# class PlaylistTracksRelation(Base):
# 	__tablename__ = 'PlaylistTracksRelation'
# 	playlist_id = Column('playlist_id', ForeignKey('Playlist.id'), primary_key=True),
# 	track_id = Column('track_id', ForeignKey('PlaylistTrack.id'), primary_key=True)


class Playlist(Base):
	__tablename__ = 'Playlist'

	id = Column(String, primary_key=True)
	name = Column(String, nullable=False)
	total_tracks = Column(Integer, nullable=False)
	public = Column(Boolean, nullable=False)
	snapshot_id = Column(String, nullable=False)
	owner_id = Column(String, nullable=False)

	tracks: relationship = relationship('PlaylistTrack',
			secondary=PlaylistTracksRelation,
			backref='Playlists')

	def __init__(self, playlist) -> None:
		self.id = playlist['id']
		self.name = playlist['name']
		self.total_tracks = playlist['tracks']['total']
		self.public = playlist['public']
		self.snapshot_id = playlist['snapshot_id']
		self.owner_id = playlist['owner']['id']


class PlaylistTrack(Base):
	__tablename__ = 'PlaylistTrack'

	id = Column(String, primary_key=True)
	name = Column(String, nullable=False)
	added_at = Column(DateTime, nullable=False)
	added_by = Column(String, nullable=False)
	duration_ms = Column(Integer, nullable=False)
	popularity = Column(Integer, nullable=False)

	def __init__(self, track: dict):
		self.id = track['track']['id']
		self.name = track['track']['name']
		self.duration_ms = track['track']['duration_ms']
		self.popularity = track['track']['popularity']
		self.added_at = datetime.strptime(track['added_at'], '%Y-%m-%dT%H:%M:%SZ')
		self.added_by = track['added_by']['id']


# class LikedTrack(Base):
# 	__tablename__ = 'LikedTrack'

# 	id = Column(String, primary_key=True)
# 	name = Column(String, nullable=False)
# 	added_at = Column(DateTime, nullable=False)
# 	added_by = Column(String, nullable=False)
# 	duration_ms = Column(Integer, nullable=False)
# 	popularity = Column(Integer, nullable=False)

# 	def __init__(self, track: dict):
# 		self.id = track['track']['id']
# 		self.name = track['track']['name']
# 		self.duration_ms = track['track']['duration_ms']
# 		self.popularity = track['track']['popularity']
# 		self.added_at = track['added_at']
