from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse
from sqlalchemy import Column, Integer, String, Float, Enum, ForeignKey, DateTime, create_engine, func
from sqlalchemy.orm import declarative_base, relationship, sessionmaker
import enum
import random
from datetime import datetime, timedelta
import uvicorn

Base = declarative_base()

# --- MODELOS ---


class ABCCategory(enum.Enum):
    A = "A_Frecuente"
    B = "B_Medio"
    C = "C_Bajo"


class Product(Base):
    __tablename__ = 'products'
    id = Column(Integer, primary_key=True)
    sku = Column(String(50), unique=True)
    name = Column(String(100))
    category_abc = Column(Enum(ABCCategory))
    base_unit = Column(String(20))
    counts = relationship("InventoryCount", back_populates="product")


class InventoryCount(Base):
    __tablename__ = 'inventory_counts'
    id = Column(Integer, primary_key=True)
    product_id = Column(Integer, ForeignKey('products.id'))
    timestamp = Column(DateTime, default=datetime.utcnow)
    physical_count = Column(Float)
    product = relationship("Product", back_populates="counts")


class MenuItem(Base):
    __tablename__ = 'menu_items'
    id = Column(Integer, primary_key=True)
    name = Column(String(100))
    ingredients = relationship("RecipeIngredient", back_populates="menu_item")


class RecipeIngredient(Base):
    __tablename__ = 'recipe_ingredients'
    id = Column(Integer, primary_key=True)
    menu_item_id = Column(Integer, ForeignKey('menu_items.id'))
    product_id = Column(Integer, ForeignKey('products.id'))
    quantity_required = Column(Float)
    menu_item = relationship("MenuItem", back_populates="ingredients")


# --- DATABASE ENGINE ---
engine = create_engine('sqlite:///inventario_cafe.db',
                       connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def boot_system():
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    insumos = [
        {"sku": "LCH-ENT", "name": "Leche Entera",
            "cat": ABCCategory.A, "unit": "ml"},
        {"sku": "PLV-MAT", "name": "Matcha", "cat": ABCCategory.B, "unit": "g"},
        {"sku": "VS-12-CAL", "name": "Vaso 12oz",
            "cat": ABCCategory.A, "unit": "pz"}
    ]
    for i in insumos:
        if not db.query(Product).filter(Product.sku == i["sku"]).first():
            db.add(Product(sku=i["sku"], name=i["name"],
                   category_abc=i["cat"], base_unit=i["unit"]))

    if not db.query(MenuItem).first():
        bebida = MenuItem(name="Latte Matcha")
        db.add(bebida)
        db.commit()
        for sku, cant in [("PLV-MAT", 15), ("LCH-ENT", 250), ("VS-12-CAL", 1)]:
            p = db.query(Product).filter(Product.sku == sku).first()
            if p:
                db.add(RecipeIngredient(menu_item_id=bebida.id,
                       product_id=p.id, quantity_required=cant))
    db.commit()
    db.close()


# --- INICIALIZACIÓN ---
boot_system()
app = FastAPI(title="Backend IA Cafetería Pro")


@app.get("/", response_class=HTMLResponse)
def dashboard():
    db = SessionLocal()
    res = db.query(Product.name, func.sum(InventoryCount.physical_count).label(
        't')).outerjoin(InventoryCount).group_by(Product.id).all()
    cards = ""
    for n, t in res:
        total = t if t else 0
        color = "#00cc66" if total > 1000 else "#ffcc00" if total > 200 else "#ff4d4d"
        cards += f"""<div style="background:white; margin:10px; padding:20px; border-radius:10px; border-left: 10px solid {color}; box-shadow: 0 2px 5px rgba(0,0,0,0.1);">
            <h2 style="margin:0;">{n}</h2><p style="margin:0;">Stock: <strong>{total}</strong></p>
        </div>"""
    db.close()
    return f"<html><body style='font-family:Arial; background:#f4f4f9; padding:20px;'><h1>🚦 IA Dashboard</h1>{cards}</body></html>"


@app.get("/home")
def home():
    return {"mensaje": "¡El Nexo de la Cafetería está activo!"}


if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)
