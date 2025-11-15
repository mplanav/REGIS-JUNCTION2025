from app.db.database import Base, engine
from app.db.models import Document, Chunk, RequirementPair, Requirement, RequirementEmbedding

def init_db():
    print("Creating tables...")
    Base.metadata.create_all(bind=engine)
    print("Database ready!")

if __name__ == "__main__":
    init_db()
