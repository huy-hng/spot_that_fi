from src.db.initializer import get_production_engine, configure_db
from src.controller import update_db
from src.controller import features

engine = get_production_engine()
configure_db(engine)


# update_db.update_all_playlist_tracks_in_db()

# update_db_liked_tracks()
features.collect_liked_tracks_without_playlist()

