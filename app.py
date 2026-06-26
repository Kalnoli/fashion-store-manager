"""
Fashion Store Manager v3.0 - Optimizado
Cache, lazy loading, queries rápidas
"""
import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime
from io import BytesIO
import base64, os

# ==== DB INIT (una sola vez) ====
if 'db_ready' not in st.session_state:
    from database import init_db
    from gestor import GestorProductos, GestorCategorias, GestorTransacciones
    init_db('tienda.db')
    
    # Seed
    gc = GestorCategorias()
    for n,d in [("Camisas","Blusas"),("Pantalones","Jeans"),("Vestidos","Vestidos"),
                ("Zapatos","Calzado"),("Accesorios","Bolsos"),("Deportivo","Ropa dep."),
                ("Abrigos","Chaquetas"),("Ropa Interior","Ropa int.")]:
        try: gc.crear_categoria(n,d)
        except: pass
    
    cats = gc.obtener_todas_categorias()
    gp = GestorProductos()
    if len(gp.obtener_todos_productos()) == 0 and cats:
        IMGS = {
            'Camisa Oxford Blanca':'https://images.unsplash.com/photo-1596755094514-f87e34085b2c?w=400',
            'Jeans Slim Fit':'https://images.unsplash.com/photo-1542272454315-4c01d7abdf4a?w=400',
            'Vestido Floral Verano':'https://images.unsplash.com/photo-1595777457583-95e059d581b8?w=400',
            'Zapatillas Running':'https://images.unsplash.com/photo-1542291026-7eec264c27ff?w=400',
            'Bolso de Cuero':'https://images.unsplash.com/photo-1584917865442-de89df76afd3?w=400',
        }
        prods = [
            ('Camisa Oxford Blanca','Clasica',25,45,50,'M','Blanco','Polo'),
            ('Jeans Slim Fit','Modernos',30,60,40,'32','Azul',"Levi's"),
            ('Vestido Floral Verano','Ligero',20,55,30,'M','Multicolor','Zara'),
            ('Zapatillas Running','Deportivas',40,85,25,'42','Negro','Nike'),
            ('Bolso de Cuero','Elegante',35,75,20,'Unico','Marron','Gucci'),
        ]
        for idx,p in enumerate(prods):
            gp.crear_producto(nombre=p[0],descripcion=p[1],precio_costo=p[2],precio_venta=p[3],
                              stock=p[4],talla=p[5],color=p[6],marca=p[7],
                              categoria_id=cats[idx].id,imagen_url=IMGS.get(p[0],''))
    
    st.session_state.gestor_prod = gp
    st.session_state.gestor_cat = gc
    st.session_state.gestor_trans = GestorTransacciones()
    st.session_state.db_ready = True

# ==== CACHE DECORATOR para queries ====
def cached_data(func):
    """Cachea datos en session_state para no recargar en cada rerun"""
    key = f"_cache_{func.__name__}"
    if key not in st.session_state:
        st.session_state[key] = func()
    return lambda: st.session_state[key]

@cached_data
def get_productos():
    return st.session_state.gestor_prod.obtener_todos_productos()

@cached_data
def get_categorias():
    return st.session_state.gestor_cat.obtener_todas_categorias()

@cached_data
def get_ventas():
    return st.session_state.gestor_trans.obtener_ventas_totales()

@cached_data
def get_bajo_stock():
    return st.session_state.gestor_prod.obtener_productos_bajo_stock(10)

def invalidate_cache():
    for k in list(st.session_state.keys()):
        if k.startswith('_cache_'):
            del st.session_state[k]

# ==== PAGE CONFIG (rápido) ====
st.set_page_config(page_title="Fashion Store", page_icon="👗", layout="wide")

# ==== CSS MINIFICADO + DARK MODE ====
st.markdown("""<style>
@import url('https://fonts.googleapis.com/css2?family=Poppins:wght@400;600;700;800&display=swap');
*{font-family:'Poppins',sans-serif;box-sizing:border-box}
@keyframes fU{from{opacity:0;transform:translateY(15px)}to{opacity:1;transform:translateY(0)}}
@keyframes fL{from{opacity:0;transform:translateX(-15px)}to{opacity:1;transform:translateX(0)}}
@keyframes sI{from{transform:scale(.9);opacity:0}to{transform:scale(1);opacity:1}}
@keyframes pG{0%,100%{box-shadow:0 0 8px rgba(102,126,234,.3)}50%{box-shadow:0 0 25px rgba(102,126,234,.6)}}
@keyframes fl{0%,100%{transform:translateY(0)}50%{transform:translateY(-8px)}}

.login-bg{position:fixed;top:0;left:0;right:0;bottom:0;background:linear-gradient(135deg,#0f0c29,#302b63,#24243e);z-index:-1}
.login-bg::before{content:'';position:absolute;width:500px;height:500px;border-radius:50%;background:radial-gradient(circle,rgba(102,126,234,.15),transparent 70%);top:-150px;right:-150px;animation:fl 6s ease-in-out infinite}
.login-bg::after{content:'';position:absolute;width:400px;height:400px;border-radius:50%;background:radial-gradient(circle,rgba(118,75,162,.12),transparent 70%);bottom:-100px;left:-100px;animation:fl 8s ease-in-out infinite reverse}
.login-card{background:rgba(255,255,255,.06);backdrop-filter:blur(20px);-webkit-backdrop-filter:blur(20px);border:1px solid rgba(255,255,255,.12);border-radius:28px;padding:35px 30px;max-width:380px;margin:8vh auto;text-align:center;animation:sI .5s ease-out}
.login-icon{font-size:3.5rem;animation:fl 3s ease infinite}
.login-title{font-size:1.6rem;font-weight:800;background:linear-gradient(135deg,#667eea,#a855f7,#ec4899);-webkit-background-clip:text;-webkit-text-fill-color:transparent}
.login-sub{color:rgba(255,255,255,.5);font-size:.85rem;margin-bottom:20px}
.login-card .stTextInput>div>div{background:rgba(255,255,255,.08)!important;border:1px solid rgba(255,255,255,.15)!important;border-radius:12px!important}
.login-card .stTextInput input{color:#fff!important}
.login-card .stTextInput label{color:rgba(255,255,255,.7)!important}
.login-card .stButton>button{background:linear-gradient(135deg,#667eea,#764ba2)!important;color:#fff!important;border:none!important;border-radius:12px!important;padding:10px!important;font-weight:700!important}

.stButton>button{border-radius:10px!important;font-weight:600!important;transition:all .2s!important}
.stButton>button:hover{transform:translateY(-2px)!important}
section[data-testid="stSidebar"]{animation:fL .3s ease-out}
[data-testid="metric-container"]{background:linear-gradient(135deg,#667eea,#764ba2)!important;border-radius:14px!important;padding:16px!important;color:#fff!important;text-align:center!important;animation:sI .3s ease-out!important}
[data-testid="metric-container"] label{color:rgba(255,255,255,.9)!important}
[data-testid="metric-container"] [data-testid="stMetricValue"]{color:#fff!important;font-weight:700!important}

.product-card{background:var(--cb,#fff);border-radius:14px;overflow:hidden;box-shadow:0 3px 12px rgba(0,0,0,.08);transition:all .25s;border:1px solid var(--bd,#e5e7eb);animation:fU .3s ease-out}
.product-card:hover{transform:translateY(-4px);box-shadow:0 10px 25px rgba(102,126,234,.2)}
.product-img{width:100%;height:160px;object-fit:cover;border-bottom:1px solid var(--bd,#e5e7eb)}
.product-body{padding:14px}
.product-body h4{margin:0 0 3px;font-size:.95rem;color:var(--tc,#111827)}
.product-body p{margin:2px 0;font-size:.85rem;color:var(--ts,#6b7280)}
.price{font-size:1.05rem;font-weight:700;color:#059669}
.stock-badge{font-size:.78rem;font-weight:400;color:var(--ts,#6b7280)}
.meta-info{font-size:.8rem;color:var(--ts,#6b7280)}

.cart-item{background:linear-gradient(135deg,var(--c1,#f8f9ff),var(--c2,#eef0ff));border-radius:12px;padding:10px 16px;margin:5px 0;border-left:4px solid #667eea;animation:fL .3s ease-out;color:var(--tc,#111827)}
.cart-total{background:linear-gradient(135deg,#667eea,#764ba2);border-radius:14px;padding:16px;color:#fff;animation:pG 3s ease-in-out infinite}
.edit-form{background:linear-gradient(135deg,var(--e1,#f0f4ff),var(--e2,#faf5ff));border-radius:16px;padding:20px;border:2px solid rgba(102,126,234,.2);animation:sI .25s ease-out;margin:12px 0;color:var(--tc,#111827)}
.stAlert,.stSuccess,.stWarning,.stError{border-radius:10px!important;animation:fU .25s ease-out!important}
.stExpander{border-radius:10px!important}
.stPlotlyChart{animation:fU .4s ease-out}
.footer{text-align:center;color:var(--ts,#6b7280);padding:15px 0}

@media(prefers-color-scheme:dark){
    :root{--cb:#1e1e2e;--bd:#313244;--tc:#cdd6f4;--ts:#a6adc8;--c1:#1e1e2e;--c2:#181825;--e1:#1e1e2e;--e2:#181825}
    .price{color:#a6e3a1}
}</style>""", unsafe_allow_html=True)

# ==== LOGIN ====
if 'logged_in' not in st.session_state: st.session_state.logged_in = False
if 'cart' not in st.session_state: st.session_state.cart = []

if not st.session_state.logged_in:
    st.markdown('<div class="login-bg"></div>', unsafe_allow_html=True)
    _,c2,_ = st.columns([1,2,1])
    with c2:
        st.markdown('<div class="login-card">', unsafe_allow_html=True)
        st.markdown('<div class="login-icon">👗</div><div class="login-title">Fashion Store</div><div class="login-sub">Gestión de Tienda de Ropa</div>', unsafe_allow_html=True)
        with st.form("lf"):
            st.text_input("👤 Usuario", value="admin", key="lu")
            st.text_input("🔒 Contraseña", type="password", value="admin", key="lp")
            if st.form_submit_button("🚀 Iniciar Sesión", width='stretch', type="primary"):
                if st.session_state.lu == "admin" and st.session_state.lp == "admin":
                    st.session_state.logged_in = True; st.rerun()
                else: st.error("❌ Incorrecto")
        st.markdown('<p style="color:rgba(255,255,255,.35);font-size:.78rem;margin-top:15px">admin / admin</p>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
    st.stop()

# ==== APP ====
st.title("👗 Fashion Store Manager")
st.markdown("### *Sistema de Gestión de Tienda de Ropa*")
st.markdown("---")

# Sidebar
st.sidebar.title("🧭 Navegación")
st.sidebar.markdown("---")
opcion = st.sidebar.radio("Selecciona:", ["📊 Dashboard","📦 Catálogo","➕ Nuevo","🏷️ Cats","💰 Venta","📈 Reportes","⚙️ Config"], key="nav")
st.sidebar.markdown("---")
st.sidebar.markdown("### 📱 Info")

# Datos cacheados
prods = get_productos()
cats = get_categorias()
vi = get_ventas()

st.sidebar.metric("Productos", len(prods))
st.sidebar.metric("Categorías", len(cats))
st.sidebar.metric("Ventas", f"${vi.total:.2f}" if vi.total else "$0.00")
if st.sidebar.button("🚪 Salir", width='stretch'):
    st.session_state.logged_in = False; st.session_state.cart = []; st.rerun()

bajo = get_bajo_stock()
if bajo: st.sidebar.warning(f"⚠️ {len(bajo)} bajo stock")

def mostrar_producto(p):
    img = p.imagen_url or ""
    st.markdown(f"""
    <div class="product-card">
        {"<img src='"+img+"' class='product-img'>" if img else '<div class="product-img" style="background:linear-gradient(135deg,var(--cb,#667eea22),var(--cb2,#764ba222));display:flex;align-items:center;justify-content:center;font-size:2.5rem;border-bottom:1px solid var(--bd,#e5e7eb)">👕</div>'}
        <div class="product-body">
            <h4>{p.nombre}</h4>
            <p>{p.descripcion[:50]}...</p>
            <p class="price">${p.precio_venta:.2f} <span class="stock-badge">Stock: {p.stock}</span></p>
            <p class="meta-info">{p.categoria.nombre if p.categoria else ''} · {p.marca or ''} · {p.talla or ''}</p>
        </div>
    </div>""", unsafe_allow_html=True)

def img_to_base64(f):
    if f: d=f.getvalue(); return f"data:image/{f.name.split('.')[-1]};base64,{base64.b64encode(d).decode()}"
    return ""

# ============================================================
# DASHBOARD
# ============================================================
if opcion == "📊 Dashboard":
    st.header("📊 Dashboard")
    c1,c2,c3,c4 = st.columns(4)
    with c1: st.metric("Productos", len(prods))
    with c2: st.metric("Valor Inv.", f"${sum(p.precio_costo*p.stock for p in prods):,.2f}")
    with c3: st.metric("Ventas", f"${vi.total:.2f}" if vi.total else "$0.00")
    with c4: st.metric("Stock Total", sum(p.stock for p in prods))
    
    st.markdown("---"); c1,c2 = st.columns(2)
    with c1:
        st.subheader("📦 Por Categoría")
        if cats and prods:
            cc={}
            for p in prods:
                cn=p.categoria.nombre if p.categoria else "Sin cat"
                cc[cn]=cc.get(cn,0)+1
            fig=px.pie(values=list(cc.values()),names=list(cc.keys()),hole=.4,color_discrete_sequence=px.colors.qualitative.Set3)
            fig.update_layout(height=350,margin=dict(l=20,r=20,t=30,b=20))
            st.plotly_chart(fig, width='stretch')
    with c2:
        st.subheader("💵 Margen")
        if prods:
            df=pd.DataFrame([{'Producto':p.nombre[:18],'Margen %':p.margen_ganancia} for p in prods[:8]])
            fig=px.bar(df,x='Margen %',y='Producto',orientation='h',color='Margen %',color_continuous_scale='RdYlGn')
            fig.update_layout(height=350,margin=dict(l=20,r=20,t=30,b=20))
            st.plotly_chart(fig, width='stretch')
    if bajo:
        st.markdown("---"); st.subheader("⚠️ Stock Bajo")
        st.dataframe(pd.DataFrame([{'ID':p.id,'Producto':p.nombre,'Stock':p.stock} for p in bajo]), width='stretch', hide_index=True)

# ============================================================
# CATÁLOGO
# ============================================================
elif opcion == "📦 Catálogo":
    st.header("📦 Catálogo")
    
    if 'edit_id' in st.session_state and st.session_state.edit_id:
        pe = st.session_state.gestor_prod.obtener_producto(st.session_state.edit_id)
        if pe:
            st.markdown("---"); st.subheader(f"✏️ {pe.nombre}")
            with st.form("ef"):
                c1,c2 = st.columns(2)
                with c1:
                    en=st.text_input("Nombre",value=pe.nombre)
                    ed=st.text_area("Descripción",value=pe.descripcion or "",height=70)
                    ec=st.number_input("Costo ($)",value=pe.precio_costo,step=.01,format="%.2f")
                    ev=st.number_input("Venta ($)",value=pe.precio_venta,step=.01,format="%.2f")
                with c2:
                    esk=st.number_input("Stock",value=pe.stock,step=1)
                    if cats:
                        cops={c.nombre:c.id for c in cats}
                        ca=pe.categoria.nombre if pe.categoria else list(cops.keys())[0]
                        ecat=st.selectbox("Categoría",list(cops.keys()),index=list(cops.keys()).index(ca) if ca in cops else 0)
                    eta=st.text_input("Talla",value=pe.talla or "")
                    eco=st.text_input("Color",value=pe.color or "")
                    ema=st.text_input("Marca",value=pe.marca or "")
                    eimg=st.text_input("URL Imagen",value=pe.imagen_url or "",placeholder="https://...")
                upload=st.file_uploader("📸 Subir",type=["jpg","jpeg","png","webp"],key="eiu")
                if st.form_submit_button("💾 Guardar",width='stretch',type="primary"):
                    kw={'nombre':en,'descripcion':ed,'precio_costo':ec,'precio_venta':ev,'stock':esk,'talla':eta,'color':eco,'marca':ema}
                    if cats: kw['categoria_id']=cops[ecat]
                    kw['imagen_url']=img_to_base64(upload) if upload else eimg
                    st.session_state.gestor_prod.actualizar_producto(pe.id,**kw)
                    invalidate_cache(); st.success(f"✅ '{en}' actualizado!"); st.session_state.edit_id=None; st.rerun()
                if st.form_submit_button("❌ Cancelar",width='stretch'): st.session_state.edit_id=None; st.rerun()
    
    c1,c2,c3 = st.columns(3)
    with c1: busq=st.text_input("🔍","",key="bq")
    with c2:
        cops={c.nombre:c.id for c in cats}
        cf=st.selectbox("Cat:",["Todas"]+list(cops.keys()),key="cf")
    with c3: ord=st.selectbox("Ord:",["Nombre","Precio ↑","Precio ↓","Stock"],key="or")
    
    cid = cops.get(cf) if cf!="Todas" else None
    lista=st.session_state.gestor_prod.buscar_productos(termino=busq,categoria_id=cid)
    if ord=="Nombre": lista.sort(key=lambda x:x.nombre)
    elif ord=="Precio ↑": lista.sort(key=lambda x:x.precio_venta)
    elif ord=="Precio ↓": lista.sort(key=lambda x:x.precio_venta,reverse=True)
    elif ord=="Stock": lista.sort(key=lambda x:x.stock)
    
    st.markdown(f"**{len(lista)} prod.**"); st.markdown("---")
    if lista:
        cols=st.columns(3)
        for i,p in enumerate(lista):
            with cols[i%3]:
                mostrar_producto(p)
                cb1,cb2=st.columns(2)
                with cb1:
                    if st.button("✏️",key=f"e{p.id}",width='stretch'): st.session_state.edit_id=p.id; st.rerun()
                with cb2:
                    if st.button("🗑️",key=f"d{p.id}",width='stretch'):
                        if st.session_state.gestor_prod.eliminar_producto(p.id): invalidate_cache(); st.success("Eliminado"); st.rerun()
        st.markdown("---")
        df_e=pd.DataFrame([{'ID':pp.id,'Nombre':pp.nombre,'Venta':pp.precio_venta,'Stock':pp.stock,'Cat':pp.categoria.nombre if pp.categoria else ''} for pp in lista])
        st.download_button("📥 CSV", df_e.to_csv(index=False,encoding='utf-8-sig'), f"catalogo_{datetime.now():%Y%m%d_%H%M%S}.csv", mime="text/csv")
    else: st.info("Sin resultados")

# ============================================================
# NUEVO PRODUCTO
# ============================================================
elif opcion == "➕ Nuevo":
    st.header("➕ Nuevo Producto")
    with st.form("np"):
        c1,c2=st.columns(2)
        with c1: nom=st.text_input("Nombre *"); desc=st.text_area("Descripción",height=70); costo=st.number_input("Costo ($)",min_value=0.,step=.01); vta=st.number_input("Venta ($)",min_value=0.,step=.01)
        with c2:
            sk=st.number_input("Stock",min_value=0,step=1)
            if cats: cops={c.nombre:c.id for c in cats}; csel=st.selectbox("Categoría *",list(cops.keys()))
            ta=st.text_input("Talla"); co=st.text_input("Color"); ma=st.text_input("Marca")
        img_url=st.text_input("URL imagen",placeholder="https://...")
        img_f=st.file_uploader("O sube",type=["jpg","jpeg","png","webp"])
        if st.form_submit_button("💾 Guardar",width='stretch',type="primary"):
            if not nom: st.error("Nombre requerido")
            else:
                try:
                    url=img_to_base64(img_f) if img_f else img_url
                    st.session_state.gestor_prod.crear_producto(nom,desc,costo,vta,sk,cops[csel],ta,co,ma,url)
                    invalidate_cache(); st.success(f"✅ '{nom}' creado!"); st.balloons()
                except Exception as e: st.error(f"Error: {e}")

# ============================================================
# CATEGORÍAS
# ============================================================
elif opcion == "🏷️ Cats":
    st.header("🏷️ Categorías")
    c1,c2=st.columns([1,2])
    with c1:
        st.subheader("➕ Nueva")
        with st.form("nc"):
            nc=st.text_input("Nombre *"); nd=st.text_area("Descripción")
            if st.form_submit_button("Crear",width='stretch'):
                if nc:
                    try: st.session_state.gestor_cat.crear_categoria(nc,nd); invalidate_cache(); st.success(f"✅ '{nc}'"); st.rerun()
                    except Exception as e: st.error(f"Error: {e}")
    with c2:
        st.subheader("📋 Existentes")
        for cat in st.session_state.gestor_cat.obtener_todas_categorias():
            with st.expander(f"📁 {cat.nombre} ({len(cat.productos)})"):
                st.write(f"**ID:** {cat.id} | {cat.descripcion or ''}")
                if cat.productos:
                    for pr in cat.productos[:8]: st.write(f"  • {pr.nombre} - ${pr.precio_venta:.2f}")
                if st.button("🗑️",key=f"dc{cat.id}"):
                    if len(cat.productos)==0 and st.session_state.gestor_cat.eliminar_categoria(cat.id): invalidate_cache(); st.success("Eliminada"); st.rerun()
                    else: st.error("Tiene productos")

# ============================================================
# VENTAS
# ============================================================
elif opcion == "💰 Venta":
    st.header("💰 Registrar Venta")
    if 'cart' not in st.session_state: st.session_state.cart=[]
    disp=[p for p in get_productos() if p.stock>0]
    
    st.subheader("🛒 Carrito")
    if st.session_state.cart:
        total=0
        for i,it in enumerate(st.session_state.cart):
            sub=it['cant']*it['precio']; total+=sub
            st.markdown(f'<div class="cart-item"><strong>{it["nombre"]}</strong> x{it["cant"]} = <strong>${sub:.2f}</strong></div>',unsafe_allow_html=True)
            if st.button("❌",key=f"rc{i}"): st.session_state.cart.pop(i); st.rerun()
        st.markdown(f'<div class="cart-total"><h3 style="margin:0">💰 Total: ${total:.2f}</h3></div>',unsafe_allow_html=True)
        st.markdown("---")
        c1,c2=st.columns(2)
        with c1: cli=st.text_input("Cliente")
        with c2: met=st.selectbox("Pago",["Efectivo","Tarjeta","Transferencia","Otro"])
        nt=st.text_area("Notas")
        if st.button("✅ Finalizar",width='stretch',type="primary"):
            ok=0
            for it in st.session_state.cart:
                if st.session_state.gestor_trans.registrar_venta(it['id'],it['cant'],cli or None,f"Método:{met}. {nt}"): ok+=1
            if ok: invalidate_cache(); st.success(f"✅ {ok} venta(s). Total: ${total:.2f}"); st.balloons(); st.session_state.cart=[]; st.rerun()
            else: st.error("Error en ventas")
        if st.button("🗑️ Vaciar",width='stretch'): st.session_state.cart=[]; st.rerun()
    else: st.info("🛒 Vacío")
    
    st.markdown("---"); st.subheader("📦 Agregar")
    if disp:
        c1,c2,c3=st.columns([3,2,2])
        with c1: opts={f"{p.nombre} - ${p.precio_venta:.2f} (S:{p.stock})":p for p in disp}; sel=st.selectbox("",list(opts.keys()),key="ca")
        with c2: obj=opts[sel]; qty=st.number_input("Cant:",min_value=1,max_value=obj.stock,value=1,step=1,key="cq")
        with c3: st.markdown("<br>",unsafe_allow_html=True)
        if st.button("🛒 Agregar",width='stretch'): st.session_state.cart.append({'id':obj.id,'nombre':obj.nombre,'precio':obj.precio_venta,'cant':qty}); st.success(f"✅ {obj.nombre}"); st.rerun()
    else: st.warning("⚠️ Sin stock")
    
    st.markdown("---"); st.subheader("🕐 Últimas")
    vs=[v for v in st.session_state.gestor_trans.obtener_todas_transacciones(5) if v.tipo=='venta']
    if vs:
        for v in vs: st.write(f"• {v.producto.nombre if v.producto else 'N/A'} - {abs(v.cantidad)} un. - ${abs(v.total):.2f}")
    else: st.info("Sin ventas")

# ============================================================
# REPORTES
# ============================================================
elif opcion == "📈 Reportes":
    st.header("📈 Reportes")
    st.subheader("📊 KPIs")
    tp=get_productos()
    c1,c2,c3,c4=st.columns(4)
    with c1: st.metric("Valor Inv.", f"${sum(p.precio_costo*p.stock for p in tp):,.2f}")
    with c2: st.metric("Potencial", f"${sum(p.precio_venta*p.stock for p in tp):,.2f}")
    with c3: st.metric("Ganancia Pot.", f"${sum(p.ganancia*p.stock for p in tp):,.2f}")
    with c4: st.metric("Margen Prom.", f"{sum(p.margen_ganancia for p in tp)/len(tp):.1f}%" if tp else "0%")
    
    st.markdown("---"); c1,c2=st.columns(2)
    with c1:
        st.subheader("🏆 Top")
        if tp:
            df=pd.DataFrame([{'Producto':p.nombre[:18],'Ganancia':p.ganancia} for p in tp]).sort_values('Ganancia',ascending=False).head(8)
            fig=px.bar(df,x='Ganancia',y='Producto',orientation='h',color='Ganancia',color_continuous_scale='Viridis')
            fig.update_layout(height=400,margin=dict(l=20,r=20,t=30,b=20))
            st.plotly_chart(fig, width='stretch')
    with c2:
        st.subheader("📦 Stock")
        if tp and cats:
            df=pd.DataFrame([{'Cat':p.categoria.nombre if p.categoria else 'Sin','Stock':p.stock} for p in tp]).groupby('Cat')['Stock'].sum().reset_index()
            fig=px.pie(df,values='Stock',names='Cat',hole=.3,color_discrete_sequence=px.colors.qualitative.Pastel)
            st.plotly_chart(fig, width='stretch')
    st.markdown("---")
    if st.button("📊 Excel"):
        df=pd.DataFrame([{'ID':p.id,'Nombre':p.nombre,'Cat':p.categoria.nombre if p.categoria else '','Venta':p.precio_venta,'Ganancia':p.ganancia,'Margen%':round(p.margen_ganancia,2),'Stock':p.stock} for p in tp])
        out=BytesIO()
        with pd.ExcelWriter(out,engine='xlsxwriter') as w: df.to_excel(w,sheet_name='Reporte',index=False)
        st.download_button("📥 Descargar",out.getvalue(),f"reporte_{datetime.now():%Y%m%d_%H%M%S}.xlsx",mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")

# ============================================================
# CONFIG
# ============================================================
elif opcion == "⚙️ Config":
    st.header("⚙️ Configuración")
    c1,c2=st.columns(2)
    with c1:
        st.markdown("### 💾 Datos")
        if st.button("🗑️ Limpiar DB",width='stretch'):
            if os.path.exists('tienda.db'): os.remove('tienda.db'); invalidate_cache(); st.success("✅ DB limpia"); st.balloons()
    with c2:
        st.markdown("### 📊 Info")
        st.write(f"**Fecha:** {datetime.now():%Y-%m-%d %H:%M}")
        st.write(f"**Productos:** {len(prods)} · **Cat:** {len(cats)}")
        if vi.total: st.write(f"**Ventas:** ${vi.total:.2f}")
    st.markdown("---")
    st.markdown("**v3.0** · Caché · Streamlit · Docker · Dark mode · Multi-carrito")

st.markdown("---")
st.markdown('<div class="footer">Fashion Store Manager</div>', unsafe_allow_html=True)
