from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

# engine = create_engine('sqlite:///:memory:')
engine = create_engine('sqlite:///src/database/SpotifyData.db')
Session = sessionmaker(bind=engine)
Base = declarative_base(bind=engine)

from .tables import *
# Base.metadata.drop_all(bind=engine)
Base.metadata.create_all(bind=engine)