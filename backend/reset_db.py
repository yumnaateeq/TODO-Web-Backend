from src.database import engine
from src.models.models import SQLModel

def reset_db():
    print("Dropping tables...")
    SQLModel.metadata.drop_all(engine)
    print("Creating tables...")
    SQLModel.metadata.create_all(engine)
    print("Done!")

if __name__ == "__main__":
    reset_db()
