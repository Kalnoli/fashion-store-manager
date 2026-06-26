"""
Módulo de gestión de productos
CRUD completo para el catálogo de la tienda
"""

from database import get_session, Producto, Categoria, Transaccion
from datetime import datetime
from typing import List, Optional
from sqlalchemy.orm import joinedload

class GestorProductos:
    def __init__(self, db_path='tienda.db'):
        self.db_path = db_path
    
    def obtener_session(self):
        return get_session(self.db_path)
    
    def crear_producto(self, nombre, descripcion, precio_costo, precio_venta, 
                       stock, categoria_id, talla=None, color=None, 
                       marca=None, imagen_url=None):
        """Crear un nuevo producto"""
        session = self.obtener_session()
        try:
            producto = Producto(
                nombre=nombre,
                descripcion=descripcion,
                precio_costo=precio_costo,
                precio_venta=precio_venta,
                stock=stock,
                categoria_id=categoria_id,
                talla=talla,
                color=color,
                marca=marca,
                imagen_url=imagen_url
            )
            session.add(producto)
            session.commit()
            session.refresh(producto)
            return producto
        finally:
            session.close()
    
    def obtener_producto(self, producto_id):
        """Obtener un producto por ID"""
        session = self.obtener_session()
        try:
            return session.query(Producto).options(
                joinedload(Producto.categoria)
            ).filter(Producto.id == producto_id).first()
        finally:
            session.close()
    
    def obtener_todos_productos(self, activos_only=True):
        """Obtener todos los productos"""
        session = self.obtener_session()
        try:
            query = session.query(Producto).options(
                joinedload(Producto.categoria)
            ).order_by(Producto.fecha_creacion.desc())
            if activos_only:
                query = query.filter(Producto.activo == True)
            return query.all()
        finally:
            session.close()
    
    def buscar_productos(self, termino, categoria_id=None, talla=None, 
                         color=None, marca=None, min_precio=None, max_precio=None):
        """Búsqueda avanzada de productos"""
        session = self.obtener_session()
        try:
            query = session.query(Producto).options(
                joinedload(Producto.categoria)
            ).filter(Producto.activo == True)
            
            if termino:
                query = query.filter(
                    (Producto.nombre.ilike(f'%{termino}%')) |
                    (Producto.descripcion.ilike(f'%{termino}%')) |
                    (Producto.marca.ilike(f'%{termino}%'))
                )
            
            if categoria_id:
                query = query.filter(Producto.categoria_id == categoria_id)
            
            if talla:
                query = query.filter(Producto.talla == talla)
            
            if color:
                query = query.filter(Producto.color.ilike(f'%{color}%'))
            
            if marca:
                query = query.filter(Producto.marca.ilike(f'%{marca}%'))
            
            if min_precio is not None:
                query = query.filter(Producto.precio_venta >= min_precio)
            
            if max_precio is not None:
                query = query.filter(Producto.precio_venta <= max_precio)
            
            return query.all()
        finally:
            session.close()
    
    def actualizar_producto(self, producto_id, **kwargs):
        """Actualizar un producto existente"""
        session = self.obtener_session()
        try:
            producto = session.query(Producto).filter(Producto.id == producto_id).first()
            if producto:
                for key, value in kwargs.items():
                    if hasattr(producto, key):
                        setattr(producto, key, value)
                producto.fecha_actualizacion = datetime.now()
                session.commit()
                session.refresh(producto)
                return producto
            return None
        finally:
            session.close()
    
    def eliminar_producto(self, producto_id, soft_delete=True):
        """Eliminar un producto (soft delete por defecto)"""
        session = self.obtener_session()
        try:
            producto = session.query(Producto).filter(Producto.id == producto_id).first()
            if producto:
                if soft_delete:
                    producto.activo = False
                    producto.fecha_actualizacion = datetime.now()
                else:
                    session.delete(producto)
                session.commit()
                return True
            return False
        finally:
            session.close()
    
    def actualizar_stock(self, producto_id, cantidad, tipo='ajuste'):
        """Actualizar el stock de un producto"""
        session = self.obtener_session()
        try:
            producto = session.query(Producto).filter(Producto.id == producto_id).first()
            if producto:
                producto.stock += cantidad
                
                # Registrar transacción
                transaccion = Transaccion(
                    tipo=tipo,
                    producto_id=producto_id,
                    cantidad=cantidad,
                    precio_unitario=producto.precio_venta,
                    total=cantidad * producto.precio_venta,
                    fecha=datetime.now()
                )
                session.add(transaccion)
                session.commit()
                session.refresh(producto)
                return producto
            return None
        finally:
            session.close()
    
    def obtener_productos_bajo_stock(self, limite=5):
        """Obtener productos con stock bajo"""
        session = self.obtener_session()
        try:
            return session.query(Producto).options(
                joinedload(Producto.categoria)
            ).filter(
                Producto.activo == True,
                Producto.stock <= limite
            ).order_by(Producto.stock.asc()).all()
        finally:
            session.close()

class GestorCategorias:
    def __init__(self, db_path='tienda.db'):
        self.db_path = db_path
    
    def obtener_session(self):
        return get_session(self.db_path)
    
    def crear_categoria(self, nombre, descripcion=None):
        """Crear una nueva categoría"""
        session = self.obtener_session()
        try:
            categoria = Categoria(nombre=nombre, descripcion=descripcion)
            session.add(categoria)
            session.commit()
            session.refresh(categoria)
            return categoria
        finally:
            session.close()
    
    def obtener_todas_categorias(self):
        """Obtener todas las categorías"""
        session = self.obtener_session()
        try:
            return session.query(Categoria).options(
                joinedload(Categoria.productos)
            ).order_by(Categoria.nombre).all()
        finally:
            session.close()
    
    def actualizar_categoria(self, categoria_id, nombre=None, descripcion=None):
        """Actualizar una categoría"""
        session = self.obtener_session()
        try:
            categoria = session.query(Categoria).filter(Categoria.id == categoria_id).first()
            if categoria:
                if nombre:
                    categoria.nombre = nombre
                if descripcion:
                    categoria.descripcion = descripcion
                session.commit()
                session.refresh(categoria)
                return categoria
            return None
        finally:
            session.close()
    
    def eliminar_categoria(self, categoria_id):
        """Eliminar una categoría (si no tiene productos)"""
        session = self.obtener_session()
        try:
            categoria = session.query(Categoria).options(
                joinedload(Categoria.productos)
            ).filter(Categoria.id == categoria_id).first()
            if categoria:
                if len(categoria.productos) == 0:
                    session.delete(categoria)
                    session.commit()
                    return True
                else:
                    return False  # Tiene productos asociados
            return False
        finally:
            session.close()

class GestorTransacciones:
    def __init__(self, db_path='tienda.db'):
        self.db_path = db_path
    
    def obtener_session(self):
        return get_session(self.db_path)
    
    def registrar_venta(self, producto_id, cantidad, cliente=None, notas=None):
        """Registrar una venta"""
        session = self.obtener_session()
        try:
            producto = session.query(Producto).filter(Producto.id == producto_id).first()
            if producto and producto.stock >= cantidad:
                producto.stock -= cantidad
                
                transaccion = Transaccion(
                    tipo='venta',
                    producto_id=producto_id,
                    cantidad=-cantidad,
                    precio_unitario=producto.precio_venta,
                    total=cantidad * producto.precio_venta,
                    cliente=cliente,
                    notas=notas
                )
                session.add(transaccion)
                session.commit()
                session.refresh(producto)
                return transaccion
            return None
        finally:
            session.close()
    
    def obtener_todas_transacciones(self, limite=100):
        """Obtener todas las transacciones"""
        session = self.obtener_session()
        try:
            return session.query(Transaccion).options(
                joinedload(Transaccion.producto)
            ).order_by(
                Transaccion.fecha.desc()
            ).limit(limite).all()
        finally:
            session.close()
    
    def obtener_transacciones_por_fecha(self, fecha_inicio, fecha_fin):
        """Obtener transacciones en un rango de fechas"""
        session = self.obtener_session()
        try:
            return session.query(Transaccion).filter(
                Transaccion.fecha >= fecha_inicio,
                Transaccion.fecha <= fecha_fin
            ).order_by(Transaccion.fecha.desc()).all()
        finally:
            session.close()
    
    def obtener_ventas_totales(self):
        """Obtener total de ventas"""
        session = self.obtener_session()
        try:
            from sqlalchemy import func
            resultado = session.query(
                func.sum(Transaccion.total).label('total'),
                func.count(Transaccion.id).label('cantidad')
            ).filter(Transaccion.tipo == 'venta').first()
            return resultado
        finally:
            session.close()