# scripts/create_tables.py

from app.core.database import Base, engine
from app.models import RawMarketData

print("📦 Creating all tables...")
Base.metadata.create_all(bind=engine)
print("✅ Tables created.")
