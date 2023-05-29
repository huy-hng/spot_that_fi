from __future__ import annotations

from datetime import datetime

from sqlalchemy import Boolean, Column, DateTime, Integer, String
from sqlalchemy.orm import relationship, backref
from sqlalchemy.sql.schema import ForeignKey

from src.db.initializer import Base
from src.helpers.helpers import parse_time
from src.types.playlists import PlaylistTrackItem, PlaylistType, TrackDict


class PlaylistAssociation(Base):
	__tablename__ = 'playlist_association'

	# REFACTOR?: use back_ref
	playlist_id: str = Column(ForeignKey('playlist_table.id'), primary_key=True)  # type: ignore
	playlist: PlaylistTable = relationship('PlaylistTable', back_populates='tracks')

	track_id: str = Column(ForeignKey('track_table.id'), primary_key=True)  # type: ignore
	track: TrackTable = relationship('TrackTable', back_populates='playlists')

	# TODO: implement default order of playlist
	order: int = Column(Integer)  # type: ignore
	
	added_by: str = Column(String, nullable=False)  # type: ignore
	added_at: datetime = Column(DateTime, nullable=False)  # type: ignore

	def __init__(self, track: PlaylistTrackItem):
		self.added_at = parse_time(track.added_at)
		self.added_by = track.added_by['id']


class PlaylistTable(Base):
	__tablename__ = 'playlist_table'


	id: str = Column(String, primary_key=True)			# type: ignore
	total_tracks: int = Column(Integer, nullable=False)	# type: ignore
	public: bool = Column(Boolean, nullable=False)		# type: ignore
	name: str = Column(String, nullable=False)			# type: ignore
	owner_id: str = Column(String, nullable=False)		# type: ignore
	snapshot_id: str = Column(String, nullable=False)	# type: ignore

	tracks: list[PlaylistAssociation] = relationship(
            'PlaylistAssociation', back_populates='playlist')

	def __init__(self, playlist: PlaylistType) -> None:
		self.id = playlist.id
		self.update(playlist)

	def update(self, playlist: PlaylistType) -> None:
		self.name = playlist.name
		self.total_tracks = playlist.tracks.total
		self.public = playlist.public
		self.snapshot_id = playlist.snapshot_id
		self.owner_id = playlist.owner.id


class TrackTable(Base):
	__tablename__ = 'track_table'

	id: str = Column(String, primary_key=True)  # type: ignore
	name: str = Column(String, nullable=False)  # type: ignore
	duration_ms: int = Column(Integer, nullable=False)  # type: ignore
	popularity: int = Column(Integer, nullable=False)  # type: ignore

	liked: LikedTable  # relationship

	playlists: list[PlaylistAssociation] = relationship(
            'PlaylistAssociation', back_populates='track')

	def __init__(self, track: TrackDict):
		self.id = track.id
		self.name = track.name
		self.duration_ms = track.duration_ms
		self.popularity = track.popularity
		# self.is_local = track.is_local

	def __repr__(self):
		return f'{self.id=}\n{self.name=}'


class LikedTable(Base):
	__tablename__ = 'liked_table'

	# FIX? smaller datetime, since resolution is seconds
	_added_at: datetime = Column('added_at', DateTime, nullable=False)  # type: ignore

	track_id: str = Column(ForeignKey('track_table.id'), primary_key=True)  # type:ignore
	track: TrackTable = relationship('TrackTable', backref=backref('liked', uselist=False))

	def __init__(self, track_id: str, added_at: str):
		self.track_id = track_id
		self.added_at = added_at
		
	@property
	def added_at(self):
		return self._added_at

	@added_at.setter
	def added_at(self, added_at: str):
		self._added_at = parse_time(added_at)


# class TestTable(Base):
# 	__tablename__ = 'test_table'

# 	# typ = Integer
# 	# typ = String
# 	primary = Column(String, primary_key=True)  # type: ignore
# 	secondary = Column(Integer)  # type: ignore

# 	def __init__(self, prim: int):
# 		self.primary = str(prim)
