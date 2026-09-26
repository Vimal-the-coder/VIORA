from database.database import engine, Base
from database.models import Conversation


Base.metadata.create_all(bind=engine)

print("VIORA database and tables created successfully!")