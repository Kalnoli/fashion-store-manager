"""
Fashion Store Manager v2.2
Login fijo, edición con fotos, imágenes por defecto
"""
import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime
from database import init_db
from gestor import GestorProductos, GestorCategorias, GestorTransacciones
from io import BytesIO
import base64, os

st.set_page_config(page_title="Fashion Store Manager", page_icon="👗", layout="wide")

# ==== DB ====
init_db('tienda.db')

# Imágenes por defecto (Unsplash)
IMGS = {
    "Camisa Oxford Blanca": "https://images.unsplash.com/photo-1596755094514-f87e34085b2c?w=400",
    "Jeans Slim Fit": "https://images.unsplash.com/photo-1542272454315-4c01d7abdf4a?w=400",
    "Vestido Floral Verano": "https://images.unsplash.com/photo-1595777457583-95e059d581b8?w=400",
    "Zapatillas Running": "https://images.unsplash.com/photo-1542291026-7eec264c27ff?w=400",
    "Bolso de Cuero": "https://images.unsplash.com/photo-1584917865442-de89df76afd3?w=400",
}

# Seed
gc = GestorCategorias()
for n,d in [("Camisas","Blusas y camisas"),("Pantalones","Jeans, chinos"),("Vestidos","Vestidos"),("Zapatos","Calzado"),("Accesorios","Bolsos, cinturones"),("Deportivo","Ropa deportiva"),("Abrigos","Chaquetas"),("Ropa Interior","Ropa interior")]:
    try: gc.crear_categoria(n, d)
    except: pass

cats = gc.obtener_todas_categorias()
gp = GestorProductos()
if len(gp.obtener_todos_productos()) == 0 and cats:
    data = [
        ("Camisa Oxford Blanca","Clásica para oficina",25,45,50,"M","Blanco","Polo",cats[0].id),
        ("Jeans Slim Fit","Modernos corte slim",30,60,40,"32","Azul","Levi's",cats[1].id),
        ("Vestido Floral Verano","Ligero estampado floral",20,55,30,"M","Multicolor","Zara",cats[2].id),
        ("Zapatillas Running","Deportivas running",40,85,25,"42","Negro","Nike",cats[3].id),
        ("Bolso de Cuero","Elegante cuero genuino",35,75,20,"Único","Marrón","Gucci",cats[4].id),
    ]
    for d in data:
        gp.crear_producto(nombre=d[0],descripcion=d[1],precio_costo=d[2],precio_venta=d[3],stock=d[4],talla=d[5],color=d[6],marca=d[7],categoria_id=d[8],imagen_url=IMGS.get(d[0],""))

# ==== CSS ====
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600;700;800&display=swap');
*{font-family:'Poppins',sans-serif;box-sizing:border-box}

@keyframes fadeUp{from{opacity:0;transform:translateY(20px)}to{opacity:1;transform:translateY(0)}}
@keyframes fadeL{from{opacity:0;transform:translateX(-20px)}to{opacity:1;transform:translateX(0)}}
@keyframes pulseG{0%,100%{box-shadow:0 0 10px rgba(102,126,234,0.3)}50%{box-shadow:0 0 30px rgba(102,126,234,0.6)}}
@keyframes float{0%,100%{transform:translateY(0)}50%{transform:translateY(-10px)}}
@keyframes scaleIn{from{transform:scale(0.9);opacity:0}to{transform:scale(1);opacity:1}}

/* Login - Streamlit friendly */
.login-bg{
    position:fixed;top:0;left:0;right:0;bottom:0;
    background:linear-gradient(135deg,#0f0c29,#302b63,#24243e);
    z-index:-1;
}
.login-bg::before{
    content:'';position:absolute;
    width:600px;height:600px;border-radius:50%;
    background:radial-gradient(circle,rgba(102,126,234,0.15),transparent 70%);
    top:-200px;right:-200px;animation:float 6s ease-in-out infinite;
}
.login-bg::after{
    content:'';position:absolute;
    width:500px;height:500px;border-radius:50%;
    background:radial-gradient(circle,rgba(118,75,162,0.12),transparent 70%);
    bottom:-150px;left:-150px;animation:float 8s ease-in-out infinite reverse;
}
.login-card-login{
    background:rgba(255,255,255,0.06);backdrop-filter:blur(20px);
    -webkit-backdrop-filter:blur(20px);
    border:1px solid rgba(255,255,255,0.12);border-radius:28px;
    padding:40px 35px;max-width:400px;margin:10vh auto;
    text-align:center;animation:scaleIn 0.5s ease-out;
}
.login-icon{font-size:4rem;animation:float 3s ease infinite}
.login-title{font-size:1.8rem;font-weight:800;background:linear-gradient(135deg,#667eea,#a855f7,#ec4899);-webkit-background-clip:text;-webkit-text-fill-color:transparent;background-clip:text}
.login-sub{color:rgba(255,255,255,0.5);font-size:.9rem;margin-bottom:25px}
.login-card-login .stTextInput>div>div{background:rgba(255,255,255,0.08)!important;border:1px solid rgba(255,255,255,0.15)!important;border-radius:12px!important;color:white!important}
.login-card-login .stTextInput input{color:white!important}
.login-card-login .stTextInput label{color:rgba(255,255,255,0.7)!important}
.login-card-login .stButton>button{background:linear-gradient(135deg,#667eea,#764ba2)!important;color:white!important;border:none!important;border-radius:12px!important;padding:12px!important;font-weight:700!important;font-size:1rem!important;transition:all .3s!important}
.login-card-login .stButton>button:hover{transform:translateY(-2px);box-shadow:0 10px 40px rgba(102,126,234,0.5)!important}

.main>.stApp{animation:fadeUp .4s ease-out}
.stButton>button{border-radius:12px!important;font-weight:600!important;transition:all .3s!important}
.stButton>button:hover{transform:translateY(-2px)!important;box-shadow:0 8px 25px rgba(102,126,234,0.3)!important}
section[data-testid="stSidebar"]{animation:fadeL .3s ease-out}
section[data-testid="stSidebar"] .stRadio label{transition:all .2s;border-radius:10px;padding:8px 12px!important}
section[data-testid="stSidebar"] .stRadio label:hover{background:rgba(102,126,234,0.1)!important;transform:translateX(4px)}
[data-testid="metric-container"]{background:linear-gradient(135deg,#667eea,#764ba2)!important;border-radius:16px!important;padding:20px!important;color:white!important;text-align:center!important;box-shadow:0 8px 20px rgba(102,126,234,0.3)!important;animation:scaleIn .4s ease-out!important}
[data-testid="metric-container"] label{color:rgba(255,255,255,.9)!important}
[data-testid="metric-container"] [data-testid="stMetricValue"]{color:white!important;font-weight:700!important}

/* Product card with image - DARK MODE SUPPORT */
.product-card{
    background:var(--card-bg, white);border-radius:16px;overflow:hidden;
    box-shadow:0 4px 15px rgba(0,0,0,0.08);transition:all .3s;
    border:1px solid var(--border-color, #e5e7eb);animation:fadeUp .4s ease-out;
    position:relative;
}
.product-card:hover{transform:translateY(-5px);box-shadow:0 12px 35px rgba(102,126,234,0.2)}
.product-img{width:100%;height:180px;object-fit:cover;border-bottom:1px solid var(--border-color, #e5e7eb)}
.product-body{padding:16px}
.product-body h4{margin:0 0 5px;font-size:1rem;color:var(--text-color, #111827)}
.product-body p{margin:2px 0;font-size:.88rem;color:var(--text-sec, #6b7280)}
.product-body .price{font-size:1.1rem;font-weight:700;color:#059669}

.cart-item{background:linear-gradient(135deg,var(--cart-bg1, #f8f9ff),var(--cart-bg2, #eef0ff));border-radius:14px;padding:12px 18px;margin:6px 0;border-left:5px solid #667eea;animation:fadeL .3s ease-out;color:var(--text-color, #111827)}
.cart-item strong{color:var(--text-color, #111827)}
.cart-total{background:linear-gradient(135deg,#667eea,#764ba2);border-radius:16px;padding:18px;color:white;animation:pulseG 3s ease-in-out infinite}
.edit-form{background:linear-gradient(135deg,var(--edit-bg1, #f0f4ff),var(--edit-bg2, #faf5ff));border-radius:20px;padding:25px;border:2px solid rgba(102,126,234,0.2);animation:scaleIn .3s ease-out;margin:15px 0;color:var(--text-color, #111827)}
.stAlert,.stInfo,.stSuccess,.stWarning,.stError{border-radius:12px!important;animation:fadeUp .3s ease-out}
.stExpander{border-radius:12px!important;border:1px solid var(--border-color, #e5e7eb)!important;margin:8px 0!important}
.stPlotlyChart{animation:fadeUp .6s ease-out}
[data-testid="column"]{animation:fadeUp .4s ease-out}
.footer{text-align:center;color:var(--text-sec, #6b7280);padding:20px 0}

/* DARK MODE OVERRIDES */
@media (prefers-color-scheme: dark) {
    :root {
        --card-bg: #1e1e2e;
        --border-color: #313244;
        --text-color: #cdd6f4;
        --text-sec: #a6adc8;
        --cart-bg1: #1e1e2e;
        --cart-bg2: #181825;
        --edit-bg1: #1e1e2e;
        --edit-bg2: #181825;
    }
    .product-body .price{color:#a6e3a1}
    .product-card:hover{box-shadow:0 12px 35px rgba(102,126,234,0.15)}
    .product-card .product-img{border-bottom-color:#313244}
}
.stock-badge{font-size:.8rem;font-weight:400;color:var(--text-sec, #6b7280)}
.meta-info{font-size:.82rem;color:var(--text-sec, #6b7280)}
</style>
""", unsafe_allow_html=True)

# ==== LOGIN ====
if 'logged_in' not in st.session_state: st.session_state.logged_in = False
if 'cart' not in st.session_state: st.session_state.cart = []

if not st.session_state.logged_in:
    st.markdown('<div class="login-bg"></div>', unsafe_allow_html=True)
    c1, c2, c3 = st.columns([1, 2, 1])
    with c2:
        st.markdown('<div class="login-card-login">', unsafe_allow_html=True)
        st.markdown('<div class="login-icon">👗</div>', unsafe_allow_html=True)
        st.markdown('<div class="login-title">Fashion Store</div>', unsafe_allow_html=True)
        st.markdown('<div class="login-sub">Sistema de Gestión de Tienda de Ropa</div>', unsafe_allow_html=True)
        
        with st.form("login_form", clear_on_submit=False):
            usuario = st.text_input("👤 Usuario", value="admin", placeholder="admin")
            contrasena = st.text_input("🔒 Contraseña", type="password", value="admin", placeholder="•"*8)
            if st.form_submit_button("🚀 Iniciar Sesión", width='stretch', type="primary"):
                if usuario == "admin" and contrasena == "admin":
                    st.session_state.logged_in = True
                    st.rerun()
                else:
                    st.error("❌ Usuario o contraseña incorrectos")
        
        st.markdown('<p style="color:rgba(255,255,255,0.35);font-size:.8rem;margin-top:20px">Credenciales: <b style="color:rgba(255,255,255,0.6)">admin</b> / <b style="color:rgba(255,255,255,0.6)">admin</b></p>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
    st.stop()

# ==== APP ====
if 'gestor_prod' not in st.session_state:
    st.session_state.gestor_prod = GestorProductos()
    st.session_state.gestor_cat = GestorCategorias()
    st.session_state.gestor_trans = GestorTransacciones()

st.title("👗 Fashion Store Manager")
st.markdown("### *Sistema Integral de Gestión de Tienda de Ropa*")
st.markdown("---")

st.sidebar.title("🧭 Navegación")
st.sidebar.markdown("---")
opcion = st.sidebar.radio("Selecciona:", ["📊 Dashboard","📦 Catálogo","➕ Nuevo Producto","🏷️ Categorías","💰 Registrar Venta","📈 Reportes","⚙️ Configuración"])
st.sidebar.markdown("---")
st.sidebar.markdown("### 📱 Info Rápida")

prods = st.session_state.gestor_prod.obtener_todos_productos()
cats = st.session_state.gestor_cat.obtener_todas_categorias()
vi = st.session_state.gestor_trans.obtener_ventas_totales()
st.sidebar.metric("Productos", len(prods))
st.sidebar.metric("Categorías", len(cats))
st.sidebar.metric("Ventas", f"${vi.total:.2f}" if vi.total else "$0.00")
if st.sidebar.button("🚪 Salir", width='stretch'):
    st.session_state.logged_in = False; st.session_state.cart = []; st.rerun()

bajo = st.session_state.gestor_prod.obtener_productos_bajo_stock(10)
if bajo: st.sidebar.warning(f"⚠️ {len(bajo)} con stock bajo")

def mostrar_producto(p):
    """Renderiza una tarjeta de producto con imagen"""
    img = p.imagen_url or ""
    st.markdown(f"""
    <div class="product-card">
        {"<img src='"+img+"' class='product-img'>" if img else '<div class="product-img" style="background:linear-gradient(135deg,var(--card-bg,#667eea22),var(--card-bg2,#764ba222));display:flex;align-items:center;justify-content:center;font-size:3rem;border-bottom:1px solid var(--border-color,#e5e7eb)">👕</div>'}
        <div class="product-body">
            <h4>{p.nombre}</h4>
            <p>{p.descripcion[:60]}...</p>
            <p class="price">${p.precio_venta:.2f} <span class="stock-badge">Stock: {p.stock}</span></p>
            <p class="meta-info">{p.categoria.nombre if p.categoria else ''} · {p.marca or ''} · {p.talla or ''} · {p.color or ''}</p>
        </div>
    </div>
    """, unsafe_allow_html=True)

def img_to_base64(img_file):
    """Convierte imagen subida a base64"""
    if img_file:
        data = img_file.getvalue()
        b64 = base64.b64encode(data).decode()
        ext = img_file.name.split('.')[-1]
        return f"data:image/{ext};base64,{b64}"
    return ""

# ============================================================
# DASHBOARD
# ============================================================
if opcion == "📊 Dashboard":
    st.header("📊 Dashboard General")
    c1,c2,c3,c4 = st.columns(4)
    with c1: st.metric("Productos", len(prods))
    with c2: st.metric("Valor Inv.", f"${sum(p.precio_costo*p.stock for p in prods):,.2f}")
    with c3:
        tv = st.session_state.gestor_trans.obtener_ventas_totales()
        st.metric("Ventas", f"${tv.total:.2f}" if tv.total else "$0.00")
    with c4: st.metric("Stock Total", sum(p.stock for p in prods))
    
    st.markdown("---"); c1,c2 = st.columns(2)
    with c1:
        st.subheader("📦 Por Categoría")
        if cats and prods:
            cc={}
            for p in prods:
                cn=p.categoria.nombre if p.categoria else "Sin cat"
                cc[cn]=cc.get(cn,0)+1
            fig=px.pie(values=list(cc.values()),names=list(cc.keys()),hole=0.4,color_discrete_sequence=px.colors.qualitative.Set3)
            fig.update_layout(height=400); st.plotly_chart(fig, width='stretch')
    with c2:
        st.subheader("💵 Margen")
        if prods:
            df=pd.DataFrame([{'Producto':p.nombre[:20],'Margen %':p.margen_ganancia} for p in prods[:10]])
            fig=px.bar(df,x='Margen %',y='Producto',orientation='h',color='Margen %',color_continuous_scale='RdYlGn')
            fig.update_layout(height=400); st.plotly_chart(fig, width='stretch')
    if bajo:
        st.markdown("---"); st.subheader("⚠️ Stock Bajo")
        st.dataframe(pd.DataFrame([{'ID':p.id,'Producto':p.nombre,'Stock':p.stock,'Precio':f"${p.precio_venta:.2f}"} for p in bajo]), width='stretch', hide_index=True)

# ============================================================
# CATÁLOGO
# ============================================================
elif opcion == "📦 Catálogo":
    st.header("📦 Catálogo de Productos")
    
    # Editar
    if 'edit_id' in st.session_state and st.session_state.edit_id:
        pe = st.session_state.gestor_prod.obtener_producto(st.session_state.edit_id)
        if pe:
            st.markdown("---")
            st.subheader(f"✏️ {pe.nombre}")
            with st.form("edit_form"):
                c1,c2 = st.columns(2)
                with c1:
                    en = st.text_input("Nombre", value=pe.nombre)
                    ed = st.text_area("Descripción", value=pe.descripcion or "", height=80)
                    ec = st.number_input("Costo ($)", value=pe.precio_costo, step=.01, format="%.2f")
                    ev = st.number_input("Venta ($)", value=pe.precio_venta, step=.01, format="%.2f")
                with c2:
                    esk = st.number_input("Stock", value=pe.stock, step=1)
                    if cats:
                        cops = {c.nombre:c.id for c in cats}
                        ca = pe.categoria.nombre if pe.categoria else list(cops.keys())[0]
                        ecat = st.selectbox("Categoría", list(cops.keys()), index=list(cops.keys()).index(ca) if ca in cops else 0)
                    eta = st.text_input("Talla", value=pe.talla or "")
                    eco = st.text_input("Color", value=pe.color or "")
                    ema = st.text_input("Marca", value=pe.marca or "")
                    eimg = st.text_input("URL Imagen", value=pe.imagen_url or "", placeholder="https://...")
                
                st.markdown("##### 📸 Subir imagen")
                upload = st.file_uploader("O elige un archivo", type=["jpg","jpeg","png","webp"], key="edit_img_upload")
                
                cb1,cb2,cb3 = st.columns([1,2,1])
                with cb2:
                    if st.form_submit_button("💾 Guardar", width='stretch', type="primary"):
                        kwargs = {'nombre':en,'descripcion':ed,'precio_costo':ec,'precio_venta':ev,'stock':esk,'talla':eta,'color':eco,'marca':ema}
                        if cats: kwargs['categoria_id'] = cops[ecat]
                        # Priorizar imagen subida sobre URL
                        if upload: kwargs['imagen_url'] = img_to_base64(upload)
                        elif eimg: kwargs['imagen_url'] = eimg
                        st.session_state.gestor_prod.actualizar_producto(pe.id, **kwargs)
                        st.success(f"✅ '{en}' actualizado!"); st.session_state.edit_id = None; st.rerun()
                if st.form_submit_button("❌ Cancelar", width='stretch'): st.session_state.edit_id = None; st.rerun()
    
    # Filtros
    c1,c2,c3 = st.columns(3)
    with c1: busq = st.text_input("🔍 Buscar:", "")
    with c2:
        cops = {c.nombre:c.id for c in cats}
        cf = st.selectbox("Categoría:", ["Todas"] + list(cops.keys()))
    with c3: ord = st.selectbox("Orden:", ["Nombre","Precio ↑","Precio ↓","Stock"])
    
    cid = cops.get(cf) if cf != "Todas" else None
    lista = st.session_state.gestor_prod.buscar_productos(termino=busq, categoria_id=cid)
    if ord == "Nombre": lista.sort(key=lambda x: x.nombre)
    elif ord == "Precio ↑": lista.sort(key=lambda x: x.precio_venta)
    elif ord == "Precio ↓": lista.sort(key=lambda x: x.precio_venta, reverse=True)
    elif ord == "Stock": lista.sort(key=lambda x: x.stock)
    
    st.markdown(f"**{len(lista)} producto(s)**"); st.markdown("---")
    if lista:
        cols = st.columns(3)
        for i, p in enumerate(lista):
            with cols[i % 3]:
                mostrar_producto(p)
                cb1,cb2 = st.columns(2)
                with cb1:
                    if st.button("✏️", key=f"e_{p.id}", width='stretch'): st.session_state.edit_id = p.id; st.rerun()
                with cb2:
                    if st.button("🗑️", key=f"d_{p.id}", width='stretch'):
                        if st.session_state.gestor_prod.eliminar_producto(p.id): st.success(f"'{p.nombre}' eliminado"); st.rerun()
        st.markdown("---")
        df_e = pd.DataFrame([{'ID':pp.id,'Nombre':pp.nombre,'Venta':pp.precio_venta,'Stock':pp.stock,'Cat':pp.categoria.nombre if pp.categoria else '','Marca':pp.marca,'Ganancia':pp.ganancia,'Margen %':round(pp.margen_ganancia,2)} for pp in lista])
        st.download_button("📥 CSV", df_e.to_csv(index=False, encoding='utf-8-sig'), f"catalogo_{datetime.now():%Y%m%d_%H%M%S}.csv", mime="text/csv")
    else: st.info("Sin resultados")

# ============================================================
# NUEVO PRODUCTO
# ============================================================
elif opcion == "➕ Nuevo Producto":
    st.header("➕ Nuevo Producto")
    with st.form("np_form"):
        c1,c2 = st.columns(2)
        with c1:
            nom = st.text_input("Nombre *"); desc = st.text_area("Descripción", height=80)
            costo = st.number_input("Costo ($)", min_value=0., step=.01)
            vta = st.number_input("Venta ($)", min_value=0., step=.01)
        with c2:
            sk = st.number_input("Stock", min_value=0, step=1)
            if cats:
                cops = {c.nombre:c.id for c in cats}
                csel = st.selectbox("Categoría *", list(cops.keys()))
            ta = st.text_input("Talla"); co = st.text_input("Color"); ma = st.text_input("Marca")
        img_url = st.text_input("URL de imagen (opcional)", placeholder="https://...")
        img_file = st.file_uploader("O sube una imagen", type=["jpg","jpeg","png","webp"])
        
        if st.form_submit_button("💾 Guardar", width='stretch', type="primary"):
            if not nom or not csel: st.error("Nombre y categoría requeridos")
            else:
                url_final = img_to_base64(img_file) if img_file else img_url
                try:
                    np = st.session_state.gestor_prod.crear_producto(nom, desc, costo, vta, sk, cops[csel], ta, co, ma, url_final)
                    st.success(f"✅ '{nom}' creado!"); st.balloons()
                    st.write(f"**Precio:** ${np.precio_venta:.2f} · **Margen:** {np.margen_ganancia:.1f}% · **Stock:** {np.stock}")
                except Exception as e: st.error(f"Error: {e}")

# ============================================================
# CATEGORÍAS
# ============================================================
elif opcion == "🏷️ Categorías":
    st.header("🏷️ Categorías")
    c1,c2 = st.columns([1,2])
    with c1:
        st.subheader("➕ Nueva")
        with st.form("nc"):
            nc = st.text_input("Nombre *"); nd = st.text_area("Descripción")
            if st.form_submit_button("Crear", width='stretch'):
                if nc:
                    try: st.session_state.gestor_cat.crear_categoria(nc, nd); st.success(f"✅ '{nc}' creada!"); st.rerun()
                    except Exception as e: st.error(f"Error: {e}")
    with c2:
        st.subheader("📋 Existentes")
        for cat in st.session_state.gestor_cat.obtener_todas_categorias():
            with st.expander(f"📁 {cat.nombre} ({len(cat.productos)} prods)"):
                st.write(f"**ID:** {cat.id} | **Desc:** {cat.descripcion or 'N/A'}")
                if cat.productos:
                    for pr in cat.productos[:10]: st.write(f"  • {pr.nombre} - ${pr.precio_venta:.2f}")
                if st.button("🗑️ Eliminar", key=f"dc_{cat.id}"):
                    if len(cat.productos)==0 and st.session_state.gestor_cat.eliminar_categoria(cat.id): st.success("Eliminada"); st.rerun()
                    else: st.error("Tiene productos")

# ============================================================
# VENTAS CARRITO
# ============================================================
elif opcion == "💰 Registrar Venta":
    st.header("💰 Registrar Venta")
    if 'cart' not in st.session_state: st.session_state.cart = []
    disponibles = [p for p in st.session_state.gestor_prod.obtener_todos_productos() if p.stock > 0]
    
    st.subheader("🛒 Carrito")
    if st.session_state.cart:
        total=0
        for i,item in enumerate(st.session_state.cart):
            sub=item['cant']*item['precio']; total+=sub
            st.markdown(f'<div class="cart-item"><strong>{item["nombre"]}</strong> x{item["cant"]} = <strong>${sub:.2f}</strong></div>', unsafe_allow_html=True)
            if st.button("❌", key=f"rc_{i}"): st.session_state.cart.pop(i); st.rerun()
        st.markdown(f'<div class="cart-total"><h3 style="margin:0">💰 Total: ${total:.2f}</h3></div>', unsafe_allow_html=True)
        st.markdown("---")
        c1,c2 = st.columns(2)
        with c1: cli = st.text_input("Cliente (opc.)")
        with c2: met = st.selectbox("Pago", ["Efectivo","Tarjeta","Transferencia","Otro"])
        nt = st.text_area("Notas")
        if st.button("✅ Finalizar Venta", width='stretch', type="primary"):
            ok=0
            for it in st.session_state.cart:
                if st.session_state.gestor_trans.registrar_venta(it['id'], it['cant'], cli or None, f"Método:{met}. {nt}"): ok+=1
            if ok: st.success(f"✅ {ok} venta(s). Total: ${total:.2f}"); st.balloons(); st.session_state.cart = []; st.rerun()
            else: st.error("Error en ventas")
        if st.button("🗑️ Vaciar", width='stretch'): st.session_state.cart = []; st.rerun()
    else: st.info("🛒 Carrito vacío. Agrega productos abajo.")
    
    st.markdown("---"); st.subheader("📦 Agregar")
    if disponibles:
        c1,c2,c3 = st.columns([3,2,2])
        with c1:
            opts = {f"{p.nombre} - ${p.precio_venta:.2f} (Stock:{p.stock})": p for p in disponibles}
            sel = st.selectbox("Producto:", list(opts.keys()), key="ca")
        with c2:
            obj = opts[sel]
            qty = st.number_input("Cant:", min_value=1, max_value=obj.stock, value=1, step=1, key="cq")
        with c3:
            st.markdown("<br>", unsafe_allow_html=True)
            if st.button("🛒 Agregar", width='stretch'):
                st.session_state.cart.append({'id':obj.id,'nombre':obj.nombre,'precio':obj.precio_venta,'cant':qty})
                st.success(f"✅ {obj.nombre} x{qty}"); st.rerun()
    else: st.warning("⚠️ Sin stock")
    
    st.markdown("---"); st.subheader("🕐 Últimas")
    vs = [v for v in st.session_state.gestor_trans.obtener_todas_transacciones(5) if v.tipo=='venta']
    if vs:
        for v in vs: st.write(f"• {v.producto.nombre if v.producto else 'N/A'} - {abs(v.cantidad)} un. - ${abs(v.total):.2f} ({v.fecha:%d/%m %H:%M})")
    else: st.info("Sin ventas")

# ============================================================
# REPORTES
# ============================================================
elif opcion == "📈 Reportes":
    st.header("📈 Reportes")
    st.subheader("📊 KPIs")
    tp = st.session_state.gestor_prod.obtener_todos_productos()
    c1,c2,c3,c4 = st.columns(4)
    with c1: st.metric("Valor Inv.", f"${sum(p.precio_costo*p.stock for p in tp):,.2f}")
    with c2: st.metric("Potencial Venta", f"${sum(p.precio_venta*p.stock for p in tp):,.2f}")
    with c3: st.metric("Ganancia Pot.", f"${sum(p.ganancia*p.stock for p in tp):,.2f}")
    with c4: st.metric("Margen Prom.", f"{sum(p.margen_ganancia for p in tp)/len(tp):.1f}%" if tp else "0%")
    st.markdown("---"); c1,c2 = st.columns(2)
    with c1:
        st.subheader("🏆 Top Rentables")
        if tp:
            df=pd.DataFrame([{'Producto':p.nombre[:20],'Ganancia':p.ganancia} for p in tp]).sort_values('Ganancia', ascending=False).head(10)
            fig=px.bar(df,x='Ganancia',y='Producto',orientation='h',color='Ganancia',color_continuous_scale='Viridis')
            fig.update_layout(height=450); st.plotly_chart(fig, width='stretch')
    with c2:
        st.subheader("📦 Stock")
        if tp and cats:
            df=pd.DataFrame([{'Cat':p.categoria.nombre if p.categoria else 'Sin cat','Stock':p.stock} for p in tp]).groupby('Cat')['Stock'].sum().reset_index()
            fig=px.pie(df,values='Stock',names='Cat',hole=.3,color_discrete_sequence=px.colors.qualitative.Pastel)
            st.plotly_chart(fig, width='stretch')
    st.markdown("---")
    if st.button("📊 Exportar Excel"):
        df=pd.DataFrame([{'ID':p.id,'Producto':p.nombre,'Cat':p.categoria.nombre if p.categoria else '','Marca':p.marca,'Costo':p.precio_costo,'Venta':p.precio_venta,'Ganancia':p.ganancia,'Margen%':round(p.margen_ganancia,2),'Stock':p.stock,'Valor Inv':p.precio_costo*p.stock} for p in tp])
        out=BytesIO()
        with pd.ExcelWriter(out, engine='xlsxwriter') as w: df.to_excel(w, sheet_name='Reporte', index=False)
        st.download_button("📥 Descargar", out.getvalue(), f"reporte_{datetime.now():%Y%m%d_%H%M%S}.xlsx", mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")

# ============================================================
# CONFIG
# ============================================================
elif opcion == "⚙️ Configuración":
    st.header("⚙️ Configuración")
    c1,c2 = st.columns(2)
    with c1:
        st.markdown("### 💾 Datos")
        if st.button("🗑️ Limpiar DB", width='stretch'):
            if os.path.exists('tienda.db'): os.remove('tienda.db'); st.success("✅ DB limpiada"); st.balloons()
    with c2:
        st.markdown("### 📊 Info")
        st.write(f"**Fecha:** {datetime.now():%Y-%m-%d %H:%M}")
        st.write(f"**Productos:** {len(prods)} · **Cat:** {len(cats)}")
        if vi.total: st.write(f"**Ventas:** ${vi.total:.2f} · **Trans:** {vi.cantidad}")
    st.markdown("---")
    st.markdown("**Fashion Store Manager v2.2** · Login · Edición con foto · Carrito · Animaciones · Exportación")

st.markdown("---")
st.markdown('<div class="footer">Fashion Store Manager · Sistema de Gestión de Tienda de Ropa</div>', unsafe_allow_html=True)
