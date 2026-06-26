"""
Base de datos para la Tienda de Ropa
Gestión de productos, categorías y transacciones
Engine único compartido para evitar problemas de sesiones detached
"""

from sqlalchemy import create_engine, Column, Integer, String, Float, DateTime, ForeignKey, Text, Boolean, text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from datetime import datetime
import os

Base = declarative_base()

# Engine GLOBAL compartido por toda la app
_engine = None
_DEFAULT_DB = os.environ.get("DB_PATH", "tienda.db")

def get_engine(db_path='tienda.db'):
    """Obtiene o crea el engine global (singleton por path)"""
    global _engine
    if _engine is None:
        _engine = create_engine(f'sqlite:///{db_path}', echo=False)
    return _engine

class Categoria(Base):
    __tablename__ = 'categorias'
    
    id = Column(Integer, primary_key=True)
    nombre = Column(String(100), nullable=False, unique=True)
    descripcion = Column(Text)
    fecha_creacion = Column(DateTime, default=datetime.now)
    
    productos = relationship("Producto", back_populates="categoria")
    
    def __repr__(self):
        return f"<Categoria(nombre='{self.nombre}')>"

class Producto(Base):
    __tablename__ = 'productos'
    
    id = Column(Integer, primary_key=True)
    nombre = Column(String(200), nullable=False)
    descripcion = Column(Text)
    precio_costo = Column(Float, nullable=False)
    precio_venta = Column(Float, nullable=False)
    stock = Column(Integer, default=0)
    categoria_id = Column(Integer, ForeignKey('categorias.id'))
    talla = Column(String(20))
    color = Column(String(50))
    marca = Column(String(100))
    imagen_url = Column(String(500))
    activo = Column(Boolean, default=True)
    fecha_creacion = Column(DateTime, default=datetime.now)
    fecha_actualizacion = Column(DateTime, default=datetime.now, onupdate=datetime.now)
    
    categoria = relationship("Categoria", back_populates="productos")
    
    def __repr__(self):
        return f"<Producto(nombre='{self.nombre}', precio={self.precio_venta})>"
    
    @property
    def ganancia(self):
        return self.precio_venta - self.precio_costo
    
    @property
    def margen_ganancia(self):
        if self.precio_venta > 0:
            return (self.ganancia / self.precio_venta) * 100
        return 0

class Transaccion(Base):
    __tablename__ = 'transacciones'
    
    id = Column(Integer, primary_key=True)
    tipo = Column(String(20))  # 'venta', 'compra', 'ajuste'
    producto_id = Column(Integer, ForeignKey('productos.id'))
    cantidad = Column(Integer)
    precio_unitario = Column(Float)
    total = Column(Float)
    cliente = Column(String(200))
    notas = Column(Text)
    fecha = Column(DateTime, default=datetime.now)
    
    producto = relationship("Producto")
    
    def __repr__(self):
        return f"<Transaccion(tipo='{self.tipo}', total={self.total})>"

class Configuracion(Base):
    __tablename__ = 'configuracion'
    
    id = Column(Integer, primary_key=True)
    clave = Column(String(100), unique=True)
    valor = Column(Text)
    descripcion = Column(Text)

def init_db(db_path='tienda.db'):
    """Inicializa la DB: crea todas las tablas si no existen"""
    engine = get_engine(db_path)
    Base.metadata.create_all(engine)
    # WAL mode + timeout para evitar readonly
    with engine.connect() as conn:
        conn.execute(text("PRAGMA journal_mode=WAL"))
        conn.execute(text("PRAGMA synchronous=NORMAL"))
        conn.execute(text("PRAGMA busy_timeout=10000"))
    Session = sessionmaker(bind=engine)
    return Session()

def get_session(db_path='tienda.db'):
    """
    Obtiene una sesión.
    Llama a create_all para asegurar que las tablas existen,
    incluso si init_db nunca fue llamado.
    """
    engine = get_engine(db_path)
    Base.metadata.create_all(engine)
    # WAL mode + timeout para evitar readonly
    with engine.connect() as conn:
        conn.execute(text("PRAGMA journal_mode=WAL"))
        conn.execute(text("PRAGMA synchronous=NORMAL"))
        conn.execute(text("PRAGMA busy_timeout=10000"))
    Session = sessionmaker(bind=engine)
    return Session()
