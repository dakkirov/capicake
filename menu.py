# capicake_menu.py
import os
import streamlit as st
from urllib.parse import quote_plus
from datetime import date, time

# =========================
# CONFIG
# =========================
BUSINESS_PHONE = "5491162107712"   # WhatsApp Business CapiCake
CURRENCY = "ARS $"

# Bases (RU -> ES AR)
BASES_CUPCAKE = [
    "Red velvet (terciopelo rojo)",
    "Chocolate",
    "Vainilla",
    "Frutilla",
]

# Rellenos
BASE_FILLINGS = ["Frutilla", "Frambuesa", "Dulce de leche"]
EXTRA_FILLINGS = ["Pistacho", "Caramelo", "Chocolate", "Arándano"]
FILLINGS = BASE_FILLINGS + EXTRA_FILLINGS

MENU_ITEMS = [
    {
        "id": "joya_rosa",
        "name": "Joya Rosa",
        "price": 2700,
        "desc": "Vainilla con corazón de frutilla y frosting rosa-violeta con perlas doradas.",
        "image": "images/joya_rosa.png",  # PNG
        "fillings": FILLINGS,
        "bases": BASES_CUPCAKE,
    },
    {
        "id": "flor_encanto",
        "name": "Flor de Encanto",
        "price": 2900,
        "desc": "Frosting rosa + crema, pétalos cristalizados y flor violeta.",
        "image": None,
        "fillings": FILLINGS,
        "bases": BASES_CUPCAKE,
    },
]

# =========================
# HELPERS
# =========================
def ars(n: float) -> str:
    return f"{CURRENCY}{n:,.0f}".replace(",", ".")

def init_state():
    if "cart" not in st.session_state:
        # cart key: item_id||base||filling||pack -> qty
        st.session_state.cart = {}
    if "cart_open" not in st.session_state:
        st.session_state.cart_open = False

def cart_key(item_id: str, base: str, filling: str, pack: str) -> str:
    return f"{item_id}||{base}||{filling}||{pack}"

def parse_key(key: str):
    parts = key.split("||")
    parts += ["", "", "", ""]
    return parts[0], parts[1], parts[2], parts[3]

def add_to_cart(key: str, qty: int):
    if qty > 0:
        st.session_state.cart[key] = st.session_state.cart.get(key, 0) + qty

def remove_from_cart(key: str):
    if key in st.session_state.cart:
        del st.session_state.cart[key]

def build_message(cart_lines, subtotal, buyer, modality, when_txt, address, notes, custom_pack_flag):
    lines = ["Hola CapiCake! Quiero hacer este pedido:", ""]
    lines += cart_lines
    lines += ["", f"Subtotal: {ars(subtotal)}" + (" (no incluye packaging personalizado)" if custom_pack_flag else "")]
    lines += [f"Modalidad: {modality}"]
    if when_txt: lines.append(f"Para: {when_txt}")
    if address and modality == "Delivery": lines.append(f"Dirección: {address}")
    if buyer: lines.append(f"Nombre: {buyer}")
    if notes: lines += ["", f"Notas: {notes}"]
    if custom_pack_flag:
        lines += ["", "⚠️ Elegí *Packaging personalizado* en algunos ítems. El costo extra se define por WhatsApp según el diseño."]
    lines += ["", "¿Me confirmás disponibilidad y total? ¡Gracias! 🧁"]
    return "\n".join(lines)

def whatsapp_url(message: str) -> str:
    return f"https://wa.me/{BUSINESS_PHONE}?text={quote_plus(message)}"

# =========================
# UI SETUP
# =========================
st.set_page_config(page_title="CapiCake Menu", page_icon="🧁", layout="wide")
init_state()

# Toast de agregado
if "_last_added" in st.session_state:
    name, q = st.session_state.pop("_last_added")
    try:
        st.toast(f"Agregado: {name} x{q}", icon="🧁")
    except Exception:
        pass

# -------- Estilos light --------
st.markdown("""
<style>
  :root{
    --cap-pink:#FF5CA8;
    --cap-pink-100:#FFE5F2;
    --cap-bg:#FFF7FB;
    --cap-card:#FFFFFF;
    --cap-text:#2C2C2C;
    --cap-border:rgba(0,0,0,.12);
  }
  .stApp, body { background: var(--cap-bg) !important; color: var(--cap-text) !important; }
  .block-container{ max-width: 1600px; padding-top: .5rem; }

  /* Header spacing */
  .cap-header h1{ margin:0; padding:0; font-weight:900; }

  /* Botones siempre con texto blanco */
  .stButton>button{
     background: var(--cap-pink) !important;
     border:0 !important; padding:.62rem 1rem !important;
     border-radius:14px !important; font-weight:700 !important;
     box-shadow: 0 2px 10px rgba(255,92,168,.25) !important;
     color:#fff !important;
  }
  .stButton>button *{ color:#fff !important; }

  /* Inputs */
  .stTextInput>div>div>input, .stTextArea textarea,
  .stDateInput>div>div input, .stTimeInput>div>div input, .stNumberInput input,
  .stSelectbox div[data-baseweb="select"] input{
     background:#FFFFFF !important; color:#2C2C2C !important;
  }
  .stTextInput>div>div, .stTextArea>div>div,
  .stDateInput>div>div, .stTimeInput>div>div, .stNumberInput>div>div,
  .stSelectbox>div>div{
     border:1px solid var(--cap-border) !important; border-radius:12px !important;
     background:#FFFFFF !important;
  }
  input::placeholder, textarea::placeholder{ color:#9A9A9A !important; opacity:1 !important; }
  .stTextInput>div>div:focus-within,
  .stTextArea>div>div:focus-within,
  .stDateInput>div>div:focus-within,
  .stTimeInput>div>div:focus-within,
  .stNumberInput>div>div:focus-within,
  .stSelectbox>div>div:focus-within{
     border-color: var(--cap-pink) !important;
     box-shadow: 0 0 0 3px rgba(255,92,168,.18) !important;
  }

  /* Subtotal como botón grande */
  .subtotal-btn .stButton > button{
    background: var(--cap-pink) !important;
    border-radius: 20px !important;
    box-shadow: 0 8px 24px rgba(255,92,168,.25) !important;
    padding: 1.1rem 1.4rem !important;
    display:flex; justify-content:space-between; align-items:center;
    color:#fff !important;
    font-size:1.6rem !important; font-weight:900 !important;
  }

  /* Sticky cart */
  .cart-panel{ position: sticky; top: 1rem; }

  /* Nota mini */
  .cap-mini-note{ font-size:.85rem; color:#7A7A7A; margin-top:.25rem; }
</style>
""", unsafe_allow_html=True)

# ---------- Header with logo ----------
h1, h2 = st.columns([0.09, 0.91], gap="small")
with h1:
    st.title("")
    st.image("images/logo.png", use_container_width=True)
with h2:
    st.title("")
    st.markdown("<div class='cap-header'><h1>Menú & Pedido</h1></div>", unsafe_allow_html=True)
    st.caption("Elegí tus cupcakes, armá el carrito y enviá el pedido por WhatsApp en 1 click.")

# =========================
# LAYOUT: menú (izq) | carrito (der)
# =========================
left, right = st.columns([3, 1], gap="large")

# -------- RIGHT: CARRITO --------
with right:
    st.markdown("### 🛒 Tu Carrito")

    subtotal = 0
    items_count = 0
    custom_pack_flag = False
    cart_lines = []

    for key, qty in st.session_state.cart.items():
        item_id, base, filling, pack = parse_key(key)
        item = next((x for x in MENU_ITEMS if x["id"] == item_id), None)
        if not item:
            continue
        line_total = item["price"] * qty
        subtotal += line_total
        items_count += qty
        if pack == "Personalizado":
            custom_pack_flag = True
        pack_txt = "Estándar" if pack == "Estandar" else "Personalizado"
        cart_lines.append(f"- {item['name']} · Base: {base} · Relleno: {filling} · Pack: {pack_txt} · x{qty} = {ars(line_total)}")

    if not cart_lines:
        st.info("Tu carrito está vacío.")
    else:
        arrow = "▾" if not st.session_state.cart_open else "▴"
        label = f"Subtotal: {ars(subtotal)} • {items_count} ítem" + ("s" if items_count != 1 else "") + f"  {arrow}"
        st.markdown('<div class="subtotal-btn">', unsafe_allow_html=True)
        if st.button(label, key="toggle_cart", use_container_width=True):
            st.session_state.cart_open = not st.session_state.cart_open
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)

        if st.session_state.cart_open:
            for key, qty in list(st.session_state.cart.items()):
                item_id, base, filling, pack = parse_key(key)
                item = next((x for x in MENU_ITEMS if x["id"] == item_id), None)
                if not item:
                    continue
                c1, c2 = st.columns([3, 2], gap="large")  # one nesting level
                with c1:
                    if item.get("image") and os.path.exists(item["image"]):
                        st.image(item["image"], use_container_width=True)
                with c2:
                    st.write(f"**{item['name']}** · x{qty}")
                    st.caption(f"Base: {base} · Relleno: {filling} · Pack: {'Estándar' if pack=='Estandar' else 'Personalizado'}")
                    if pack == "Personalizado":
                        st.caption("Costo a convenir!", help="Packaging personalizado: costo adicional a definir por WhatsApp según el diseño.")
                    st.write(f"Total ítem: **{ars(item['price'] * qty)}**")
                    if st.button("Quitar", key=f"rm_{key}"):
                        remove_from_cart(key)
                        st.rerun()

            st.divider()
            if st.button("Vaciar carrito"):
                st.session_state.cart = {}
                st.rerun()

    # Formulario de pedido
    st.divider()
    st.markdown("#### Datos para el pedido")
    buyer = st.text_input("Nombre", placeholder="Tu nombre")
    modality = st.radio("Modalidad", ["Retiro por Palermo", "Delivery"], index=0, horizontal=True)

    col_dt1, col_dt2 = st.columns(2)
    with col_dt1:
        use_date = st.checkbox("Elegir fecha/hora")
    if use_date:
        with col_dt1: d = st.date_input("Fecha", value=date.today())
        with col_dt2: t = st.time_input("Hora", value=time(18, 0))
        when_txt = f"{d.strftime('%d/%m/%Y')} {t.strftime('%H:%M')}"
    else:
        when_txt = ""
    address = st.text_input("Dirección (si es delivery)", placeholder="Calle, número, piso…")
    notes = st.text_area("Notas (sabores, dedicatoria, etc.)", placeholder="Ej: Sin frutos secos")

    st.divider()
    if cart_lines:
        msg = build_message(cart_lines, subtotal, buyer, modality, when_txt, address, notes, custom_pack_flag)
        st.markdown(
            f"<a href='{whatsapp_url(msg)}' target='_blank' "
            "style='background:#25D366;color:#fff;font-weight:800;"
            "padding:.8rem 1.2rem;border-radius:14px;box-shadow:0 2px 10px rgba(37,211,102,.25); text-decoration:none;'>"
            "📲 Enviar pedido por WhatsApp</a>",
            unsafe_allow_html=True
        )
    else:
        st.button("📲 Enviar pedido por WhatsApp", disabled=True)

# -------- LEFT: MENÚ — 1 producto por fila (3 columnas: foto | base+relleno | packaging+cantidad+botón) --------
with left:
    
    st.header("Cupcakes")
    for item in MENU_ITEMS:
        st.subheader(item["name"])
        st.caption(item["desc"])

        col_img, col_opts, col_action = st.columns([1, 1.2, 1.1], gap="large")

        # Col 1 — Foto
        with col_img:
            if item.get("image") and os.path.exists(item["image"]):
                st.image(item["image"], use_container_width=True)
            else:
                st.markdown("🧁")

        # Col 2 — Base + Relleno
        with col_opts:
            base_val = st.selectbox("Base (bizcochuelo)", item.get("bases", BASES_CUPCAKE), key=f"base_{item['id']}")
            fill_val = st.selectbox("Relleno", item.get("fillings", FILLINGS), key=f"fill_{item['id']}")

        # Col 3 — Packaging + Cantidad + Botón
        with col_action:
            pack_val = st.radio("Packaging", ["Estandar", "Personalizado"], index=0, horizontal=True, key=f"pack_{item['id']}")
            if pack_val == "Personalizado":
                st.caption("Costo a convenir!", help="Packaging personalizado: costo adicional a definir por WhatsApp según el diseño.", unsafe_allow_html=False)
            qty_val = st.number_input("Cantidad (mín. 6)", min_value=6, value=6, step=1, key=f"qty_{item['id']}")
            st.write(f"**{ars(item['price'])}** por unidad")
            if st.button("Agregar al carrito", key=f"add_{item['id']}"):
                key = cart_key(item["id"], base_val, fill_val, pack_val)
                add_to_cart(key, qty_val)
                st.session_state._last_added = (item["name"], qty_val)
                st.rerun()

        st.divider()
