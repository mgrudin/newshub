from app import models
from app.db import Base, engine

Base.metadata.create_all(engine)
print("Database created successfully")
