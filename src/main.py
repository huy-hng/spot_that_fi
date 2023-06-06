from src.db.initializer import get_production_engine, configure_db

if __name__ == "__main__":
	engine = get_production_engine()
	configure_db(engine)
