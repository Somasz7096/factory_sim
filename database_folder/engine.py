from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


engine = create_engine(
    "sqlite:///database_folder/database.db",
    echo=True,
)



SessionLocal = sessionmaker(engine)