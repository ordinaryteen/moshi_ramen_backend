from app.core.config import settings
import psycopg2
import sys

print("--- DEBUG START ---")
print(f"1. HOST RAW: '{settings.DB_HOST}'")
print(f"2. USER RAW: '{settings.DB_USER}'")
# Kita print panjang karakter password dan karakter awal/akhir buat ngecek spasi tersembunyi
pass_len = len(settings.DB_PASSWORD)
first_char = settings.DB_PASSWORD[0] if pass_len > 0 else "N/A"
last_char = settings.DB_PASSWORD[-1] if pass_len > 0 else "N/A"
print(f"3. PASS CHECK: Length={pass_len}, First='{first_char}', Last='{last_char}'")
print(f"4. FULL URL: {settings.SQLALCHEMY_DATABASE_URI.replace(settings.DB_PASSWORD, '******')}")

print("\n[TESTING CONNECTION...]")
try:
    # Kita paksa connect pake library raw psycopg2 (bukan SQLAlchemy)
    # Kita coba paksa IPv4 (127.0.0.1) buat bypass isu IPv6 Windows
    conn = psycopg2.connect(
        dbname=settings.DB_NAME,
        user=settings.DB_USER,
        password=settings.DB_PASSWORD,
        host="127.0.0.1", # Hardcode ke IPv4 dulu
        port=settings.DB_PORT
    )
    print("✅ SUKSES LOGIN KE DB!")
    conn.close()
except Exception as e:
    print(f"❌ GAGAL LOGIN: {e}")

print("--- DEBUG END ---")