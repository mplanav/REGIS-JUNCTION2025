from db.session import Base, engine
from db.models.document import Document
from db.models.chunk import Chunk
from db.models.requirement_pair import RequirementPair

def init_db():
    print("Creating tables...")
    Base.metadata.create_all(bind=engine)
    print("Database ready!")

if __name__ == "__main__":
    init_db()
