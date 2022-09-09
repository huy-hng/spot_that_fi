"""
1.	- create declarative_base (without engine)
	- create sessionmaker (without engine)
2.	import create_session, get_session
3.	import src.db files
4.	(at the latest) create engine and pass to base and sessionmaker
5.	Base.metadata stuff
"""
from sqlalchemy.orm import Session
from src.db.initializer import configure_db, delete_tables
from src.db.session import _, create_session, get_session

# delete_tables(engine)
# engine = engine.get_testing_engine()
# configure_db(engine)

from src.db import helpers, playlists, tables, tracks
