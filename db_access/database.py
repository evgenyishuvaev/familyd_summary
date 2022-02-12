from sqlalchemy import create_engine, MetaData
from sqlalchemy.ext.declarative import declarative_base

import databases
from config import load_config


cfg = load_config()

DATABASE_URL = f"{cfg.DB.DRIVER}://{cfg.DB.USERNAME}:{cfg.DB.PASSWORD}@{cfg.DB.ADDRESS}:{cfg.DB.PORT}/{cfg.DB.NAME}"

database = databases.Database(DATABASE_URL)

metadata = MetaData()

engine = create_engine(DATABASE_URL)