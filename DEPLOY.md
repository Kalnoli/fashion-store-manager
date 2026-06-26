# 🚀 Guía rápida: Montar Fashion Store Manager en un VPS

## Requisitos
- VPS con Ubuntu 22.04+ (DigitalOcean $6/mes, Hetzner ~$4/mes, Railway)
- Docker y Docker Compose instalados
- Un dominio (opcional, ~$10/año en Namecheap)

---

## Opción 1: La más rápida (Railway.app - gratis para empezar)

1. Sube el proyecto a GitHub
2. Ve a https://railway.app
3. Crea nuevo proyecto → "Deploy from GitHub repo"
4. Railway detecta el Dockerfile automáticamente
5. ✅ Listo — te da una URL tipo `fashion-store.up.railway.app`

Sin pagar un peso para empezar.

---

## Opción 2: VPS tradicional (DigitalOcean / Hetzner)

### 1. Conectarte al VPS
```bash
ssh root@tu-vps-ip
```

### 2. Instalar Docker
```bash
curl -fsSL https://get.docker.com | sh
sudo usermod -aG docker $USER
# Cierra sesión y vuelve a entrar
```

### 3. Subir la app al VPS
```bash
# Desde tu PC local:
scp -r /ruta/de/tienda_ropa_app root@tu-vps-ip:~/fashion-store
```

### 4. Arrancar
```bash
ssh root@tu-vps-ip
cd ~/fashion-store
sudo docker compose up -d --build
```

### 5. Abrir puerto en el firewall
```bash
ufw allow 8501
```

### 6. Listo 🎉
Tu app está en: `http://tu-vps-ip:8501`

---

## Opción 3: Con dominio y HTTPS (profesional)

### 1. Apunta tu dominio al VPS
En tu proveedor de dominio, crea un registro A:
- **Tipo:** A
- **Nombre:** @ (o www)
- **Valor:** IP de tu VPS

### 2. Instalar Nginx y Certbot
```bash
sudo apt install nginx certbot python3-certbot-nginx -y
```

### 3. Configurar Nginx
```bash
sudo nano /etc/nginx/sites-available/fashion-store
```
Pega el contenido de `nginx.conf` y cambia `tudominio.com` por tu dominio.

### 4. Activar sitio
```bash
sudo ln -s /etc/nginx/sites-available/fashion-store /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl reload nginx
```

### 5. SSL gratis (Let's Encrypt)
```bash
sudo certbot --nginx -d tudominio.com -d www.tudominio.com
```

### 6. Todo listo 🚀
Tu app en: **https://tudominio.com**

---

## Comandos útiles

```bash
# Ver logs
sudo docker compose logs -f

# Actualizar (después de hacer cambios)
git pull  # o scp los archivos nuevos
sudo docker compose up -d --build --force-recreate

# Detener
sudo docker compose down

# Backup de la DB
cp data/tienda.db backups/tienda_$(date +%Y%m%d).db
```

## Precios reales

| Servicio | Costo | Notas |
|---|---|---|
| VPS (DigitalOcean) | $6/mes | 1GB RAM, 25GB SSD |
| Dominio (.com) | $10/año | Namecheap |
| SSL (Let's Encrypt) | **Gratis** | Se renueva solo |
| Railway.app | **Gratis** | 500h/mes, 1GB RAM |
| **Total** | **~$5.50/mes** | Con dominio propio |

---

## ¿Cuánto cobrar?

| Modelo | Precio | Clientes necesarios |
|---|---|---|
| **Suscripción** | $15-30/mes | 3-5 clientes pagan el VPS |
| **Instalación** | $100-200 | Una sola vez |
| **Licencia** | $50-100 | Pago único por tienda |

Con **5 clientes a $20/mes** te entran **$1,200/año** — el VPS te cuesta $72/año.

¿Quieres que lo subamos a Railway ahora mismo y te dé la URL pública? 👊
