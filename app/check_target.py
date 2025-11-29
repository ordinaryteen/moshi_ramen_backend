from app.core.config import settings

print("--- INSPEKSI KONEKSI ---")
print(f"Target Database: {settings.SQLALCHEMY_DATABASE_URI}")
print("------------------------")