from src.db.initializer import get_production_engine, configure_db
from src.controller.update_db import update_db_liked_tracks

engine = get_production_engine()
configure_db(engine)
update_db_liked_tracks()
