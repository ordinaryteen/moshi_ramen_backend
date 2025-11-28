from app.core.database import SessionLocal, engine, Base
from app.models.product import Category, Product
from app.models.user import User, Role
# TAMBAHAN PENTING: Import Order biar ikut kehapus
from app.models.order import Order, OrderItem 
from app.core.security import get_password_hash
from decimal import Decimal

db = SessionLocal()

def seed():
    print("☢️  MENGHANCURKAN DATABASE LAMA (DROP ALL)...")
    # Sekarang karena Order sudah diimport, dia bakal dihapus duluan sebelum User
    Base.metadata.drop_all(bind=engine) 
    
    print("🏗️  MEMBANGUN ULANG TABEL (CREATE ALL)...")
    Base.metadata.create_all(bind=engine)

    print("🌱 Mulai menanam benih data...")

    # --- 1. SETUP USER & ROLE ---
    role_admin = Role(role_name="admin")
    role_cashier = Role(role_name="cashier")
    role_kitchen = Role(role_name="kitchen")
    db.add_all([role_admin, role_cashier, role_kitchen])
    db.commit()

    # User Ami (Kasir)
    user_ami = User(
        username="ami", 
        email="ami@moshi.com",
        hashed_password=get_password_hash("123456"),
        role_id=role_cashier.id,
        is_active=True
    )
    db.add(user_ami)
    db.commit()
    print("✅ User 'ami' (pass: 123456) berhasil dibuat.")

    # --- 2. SETUP MENU ---
    cat_makanan = Category(name="Signature Ramen")
    cat_snack = Category(name="Snacks & Sides")
    cat_minuman = Category(name="Refreshments")

    db.add_all([cat_makanan, cat_snack, cat_minuman])
    db.commit()
    
    db.refresh(cat_makanan)
    db.refresh(cat_snack)
    db.refresh(cat_minuman)

    # Produk dengan Gambar HD
    products = [
        Product(
            name="Spicy Beef Ramen", 
            description="Kuah kaldu sapi pedas 12 jam dengan chili oil.",
            unit_price=Decimal("35000"), 
            stock=50, 
            category_id=cat_makanan.id,
            image_url="https://images.unsplash.com/photo-1591814468924-caf88d1232e1?q=80&w=1000&auto=format&fit=crop"
        ),
        Product(
            name="Chicken Miso Ramen", 
            description="Miso Jepang klasik dengan kaldu ayam kampung.",
            unit_price=Decimal("32000"), 
            stock=45, 
            category_id=cat_makanan.id,
            image_url="https://images.unsplash.com/photo-1623341214823-67e2831a6602?q=80&w=1000&auto=format&fit=crop"
        ),
        Product(
            name="Ultimate Dry Ramen", 
            description="Ramen tanpa kuah dengan topping daging cincang.",
            unit_price=Decimal("38000"), 
            stock=30, 
            category_id=cat_makanan.id,
            image_url="https://images.unsplash.com/photo-1569718212165-3a8278d5f624?q=80&w=1000&auto=format&fit=crop"
        ),
        Product(
            name="Gyoza Panggang", 
            description="Dumpling ayam udang, kulit crispy.",
            unit_price=Decimal("25000"), 
            stock=100, 
            category_id=cat_snack.id,
            image_url="https://images.unsplash.com/photo-1626805820626-4ae1d596cb62?q=80&w=1000&auto=format&fit=crop"
        ),
        Product(
            name="Chicken Karaage", 
            description="Ayam goreng tepung Jepang + lemon.",
            unit_price=Decimal("28000"), 
            stock=80, 
            category_id=cat_snack.id,
            image_url="https://images.unsplash.com/photo-1621070766841-6e63462f2f09?q=80&w=1000&auto=format&fit=crop"
        ),
        Product(
            name="Ocha (Refill)", 
            description="Teh hijau Jepang dingin/panas.",
            unit_price=Decimal("10000"), 
            stock=999, 
            category_id=cat_minuman.id,
            image_url="https://images.unsplash.com/photo-1627435601361-ec25f5b1d0e5?q=80&w=1000&auto=format&fit=crop"
        ),
        Product(
            name="Ice Lemon Tea", 
            description="Teh segar dengan lemon asli.",
            unit_price=Decimal("15000"), 
            stock=100, 
            category_id=cat_minuman.id,
            image_url="https://images.unsplash.com/photo-1513558161293-cdaf765ed2fd?q=80&w=1000&auto=format&fit=crop"
        ),
    ]

    db.add_all(products)
    db.commit()
    print("🚀 Database Reset & Seeded Successfully!")

if __name__ == "__main__":
    seed()