# capicake_menu.py
import os
import streamlit as st
from urllib.parse import quote_plus
from datetime import date, time

# =========================
# CONFIG
# =========================
st.set_page_config(page_title="Capicake — Menú & Pedido", page_icon="🧁", layout="wide")

BUSINESS_PHONE = "5491162107712"   # WhatsApp Business CapiCake
CURRENCY = "ARS $"

# =========================
# LANGUAGE / I18N
# =========================
if "lang" not in st.session_state:
    st.session_state.lang = "es"  # default: Español (AR)

LANGS = {
    "es": "🇦🇷 Español (AR)",
    "en": "🇬🇧 English",
    "ru": "🇷🇺 Русский"
}

TR = {
    "es": {
        "title": "Menú & Pedido",
        "subtitle": "Elegí tus cupcakes, armá el carrito y enviá el pedido por WhatsApp en 1 click.",
        "cart": "Tu Carrito",
        "empty_cart": "Tu carrito está vacío.",
        "subtotal_btn": "Subtotal: {subtotal} • {items} ítem{plural}",
        "order_details": "Datos para el pedido",
        "name": "Nombre",
        "mode": "Modalidad",
        "pickup": "Retiro por Palermo",
        "delivery": "Delivery",
        "choose_dt": "Elegir fecha/hora",
        "date": "Fecha",
        "time": "Hora",
        "address": "Dirección (si es delivery)",
        "notes": "Notas (sabores, dedicatoria, etc.)",
        "wa_send": "📲 Enviar pedido por WhatsApp",
        "remove": "Quitar",
        "empty": "Vaciar carrito",
        "unit_price": "por unidad",
        "item_total": "Total ítem",
        "base": "Base (bizcochuelo)",
        "filling": "Relleno",
        "packaging": "Packaging",
        "qty6": "Cantidad (mín. 6)",
        "add_to_cart": "Agregar al carrito",
        "pack_note": "Packaging personalizado: costo adicional a definir por WhatsApp según el diseño.",
        "msg_hi": "Hola CapiCake! Quiero hacer este pedido:",
        "msg_subtotal": "Subtotal: {subtotal}",
        "msg_subtotal_no_custom": "Subtotal: {subtotal} (no incluye packaging personalizado)",
        "msg_mode": "Modalidad: {mode}",
        "msg_when": "Para: {when}",
        "msg_addr": "Dirección: {addr}",
        "msg_name": "Nombre: {name}",
        "msg_notes": "Notas: {notes}",
        "msg_warn": "⚠️ Elegí Packaging personalizado en algunos ítems. El costo extra se define por WhatsApp según el diseño.",
        "msg_end": "¿Me confirmás disponibilidad y total? ¡Gracias! 🧁",
        "notice_title": "ℹ️ Diseño artesanal: puede variar",
    },
    "en": {
        "title": "Menu & Order",
        "subtitle": "Pick your cupcakes, build the cart and send your order via WhatsApp in 1 click.",
        "cart": "Your Cart",
        "empty_cart": "Your cart is empty.",
        "subtotal_btn": "Subtotal: {subtotal} • {items} item{plural}",
        "order_details": "Order details",
        "name": "Name",
        "mode": "Mode",
        "pickup": "Pickup in Palermo",
        "delivery": "Delivery",
        "choose_dt": "Choose date/time",
        "date": "Date",
        "time": "Time",
        "address": "Address (if delivery)",
        "notes": "Notes (flavors, dedication, etc.)",
        "wa_send": "📲 Send order via WhatsApp",
        "remove": "Remove",
        "empty": "Empty cart",
        "unit_price": "per unit",
        "item_total": "Item total",
        "base": "Base (cake)",
        "filling": "Filling",
        "packaging": "Packaging",
        "qty6": "Quantity (min. 6)",
        "add_to_cart": "Add to cart",
        "pack_note": "Custom packaging: extra cost to be agreed on WhatsApp depending on the design.",
        "msg_hi": "Hi CapiCake! I'd like to place this order:",
        "msg_subtotal": "Subtotal: {subtotal}",
        "msg_subtotal_no_custom": "Subtotal: {subtotal} (custom packaging not included)",
        "msg_mode": "Mode: {mode}",
        "msg_when": "For: {when}",
        "msg_addr": "Address: {addr}",
        "msg_name": "Name: {name}",
        "msg_notes": "Notes: {notes}",
        "msg_warn": "⚠️ I chose custom packaging in some items. Extra cost will be agreed on WhatsApp.",
        "msg_end": "Could you confirm availability and total? Thanks! 🧁",
        "notice_title": "ℹ️ Handmade design: variations may occur",
    },
    "ru": {
    "title": "Меню и заказ",
    "subtitle": "Выберите капкейки, соберите корзину и отправьте заказ в WhatsApp в один клик.",
    "cart": "Ваша корзина",
    "empty_cart": "Ваша корзина пуста.",
    # You can ignore {plural} for RU; it will be passed but not used
    "subtotal_btn": "Итого: {subtotal} • {items} шт.",
    "order_details": "Данные заказа",
    "name": "Имя",
    "mode": "Способ",
    "pickup": "Самовывоз из Палермо",
    "delivery": "Доставка",
    "choose_dt": "Выбрать дату/время",
    "date": "Дата",
    "time": "Время",
    "address": "Адрес (если доставка)",
    "notes": "Примечания (вкусы, пожелания и т. п.)",
    "wa_send": "📲 Отправить заказ в WhatsApp",
    "remove": "Удалить",
    "empty": "Очистить корзину",
    "unit_price": "за штуку",
    "item_total": "Итого по позиции",
    "base": "Основа (бисквит)",
    "filling": "Начинка",
    "packaging": "Упаковка",
    "qty6": "Количество (мин. 6)",
    "add_to_cart": "Добавить в корзину",
    "pack_note": "Индивидуальная упаковка: доп. стоимость согласовывается в WhatsApp в зависимости от дизайна.",
    "msg_hi": "Здравствуйте, CapiCake! Хочу оформить заказ:",
    "msg_subtotal": "Итого: {subtotal}",
    "msg_subtotal_no_custom": "Итого: {subtotal} (индивидуальная упаковка не включена)",
    "msg_mode": "Способ: {mode}",
    "msg_when": "На дату/время: {when}",
    "msg_addr": "Адрес: {addr}",
    "msg_name": "Имя: {name}",
    "msg_notes": "Примечания: {notes}",
    "msg_warn": "⚠️ Я выбрал(а) индивидуальную упаковку для некоторых позиций. Доп. стоимость согласуем в WhatsApp.",
    "msg_end": "Подтвердите, пожалуйста, доступность и итоговую стоимость. Спасибо! 🧁",
    "notice_title": "ℹ️ Ручная работа: возможны отличия",
    },
}

# BASES
# бисквит: ванильный, шоколадный, морковный, ред вельвет, лимонный
BASES = [
    ("red_velvet", {"es": "Red velvet", "en": "Red velvet", "ru": "Красный бархат"}),
    ("chocolate",  {"es": "Chocolate", "en": "Chocolate", "ru": "Шоколадный"}),
    ("vanilla",    {"es": "Vainilla", "en": "Vanilla",   "ru": "Ванильный"}),
    ("carrot",     {"es": "Carrot cake", "en": "Carrot",   "ru": "Морковный"}),
    ("lemon",      {"es": "Limón",     "en": "Lemon",    "ru": "Лимонный"})
]

# FILLINGS
# начинка клубничное конфи, малиновое, дульсе де лече, шоколадное пралине, маракуйя, лимонный курд, капучино
FILLINGS = [
    ("strawberry_confit", {"es": "Confit de frutilla", "en": "Strawberry confit", "ru": "Клубничное конфи"}),
    ("berry",             {"es": "Frutos rojos",        "en": "Berry mix",        "ru": "Ягодная"}),
    ("dulce",             {"es": "Dulce de leche",     "en": "Dulce de leche",   "ru": "Дульсе де лече"}),
    ("chocolate_praline", {"es": "Praliné de chocolate","en": "Chocolate praline","ru": "Шоколадное пралине"}),
    ("passionfruit",      {"es": "Maracuyá",           "en": "Passion fruit",    "ru": "Маракуйя"}),
    ("lemon_curd",        {"es": "Curd de limón",      "en": "Lemon curd",       "ru": "Лимонный курд"}),
    ("cappuccino",        {"es": "Capuchino",          "en": "Cappuccino",       "ru": "Капучино"})
]

# PACKAGING
PACK_LABELS = {
    "standard": {"es": "Estandar", "en": "Standard",     "ru": "Стандартная"},
    "custom":   {"es": "Personalizado", "en": "Custom",  "ru": "Индивидуальная"},
}

def lang() -> str:
    return st.session_state.get("lang", "es")

def t(key: str, **kw) -> str:
    s = TR.get(lang(), {}).get(key, TR["es"].get(key, key))
    return s.format(**kw) if kw else s

def opt_label(options, code: str) -> str:
    for c, labels in options:
        if c == code:
            return labels.get(lang(), labels["es"])
    return code

# =========================
# DATA
# =========================
MENU_ITEMS = [
    {
        "id": "carrot_charm",
        "name": "Carrot Charm",
        "price": 7500,
        # "desc": {
        #     "es": "Cremoso frosting naranja con frambuesa fresca, notas cítricas y perlas brillantes.",
        #     "en": "Creamy orange frosting with fresh raspberry, citrus notes and shiny pearls.",
        #     "ru": "Крем насыщенного оранжевого цвета с малиной, цитрусовыми нотами и блестящими шариками.",
        # },
        "image": "images/orange.png",
        "default_base": "carrot",
        "default_filling": "passionfruit",
    },
    {
        "id": "lemon_bliss",
        "name": "Lemon Bliss",
        "price": 7500,
        # "desc": {
        #     "es": "Base de vainilla con frosting amarillo, frutilla fresca y flores soleadas.",
        #     "en": "Vanilla base with yellow frosting, fresh strawberry and sunny flowers.",
        #     "ru": "Ванильный капкейк с жёлтым кремом, свежей клубникой и солнечным цветком.",
        # },
        "image": "images/yellow.png",
        "default_base": "lemon",
        "default_filling": "lemon_curd",
    },
    {
        "id": "velvet_bloom",
        "name": "Velvet Bloom",
        "price": 7500,
        # "desc": {
        #     "es": "Red velvet con frosting violeta intenso, flores brillantes y toque elegante.",
        #     "en": "Red velvet with deep violet frosting, shiny flowers and elegant finish.",
        #     "ru": "Ред велвет с насыщенным фиолетовым кремом, блестящим цветком и утончённым декором.",
        # },
        "image": "images/velvet.png",
        "default_base": "red_velvet",
        "default_filling": "berry",
    },
    {
        "id": "pink_dream",
        "name": "Pink Dream",
        "price": 7500,
        # "desc": {
        #     "es": "Frosting rosa pastel, frutilla fresca y flor en tonos rojos y blancos.",
        #     "en": "Pastel pink frosting, fresh strawberry and red-white flower decoration.",
        #     "ru": "Пастельно-розовый крем, свежая клубника и цветок в красно-белых тонах.",
        # },
        "image": "images/rose.png",
        "default_base": "vanilla",
        "default_filling": "strawberry_confit",
    },
    {
        "id": "blue_dream",
        "name": "Blue Dream",
        "price": 7500,
        # "desc": {
        #     "es": "Base vainilla con frosting celeste, arándanos frescos y flores perladas.",
        #     "en": "Vanilla base with sky-blue frosting, fresh blueberries and pearled flowers.",
        #     "ru": "Ванильный капкейк с небесно-голубым кремом, свежими черникой и украшением из жемчужных цветов.",
        # },
        "image": "images/blue.png",
        "default_base": "vanilla",
        "default_filling": "strawberry_confit",
    },
    {
        "id": "romance",
        "name": "Romance",
        "price": 7500,
        # "desc": {
        #     "es": "Vainilla con corazón de frutilla y frosting rosa-violeta con perlas doradas.",
        #     "en": "Vanilla with strawberry heart and pink-violet frosting with golden pearls.",
        #     "ru": "Ванильный капкейк с клубничной начинкой и розово-фиолетовым кремом, украшен золотыми шариками.",
        # },
        "image": "images/joya_rosa.png",
        "default_base": "vanilla",
        "default_filling": "strawberry_confit",
    },
]

# =========================
# HELPERS
# =========================
def ensure_default(key, default_code, options):
    # only set if the widget has never been initialized
    if key not in st.session_state:
        st.session_state[key] = default_code if default_code in options else options[0]

def ars(n: float) -> str:
    return f"{CURRENCY}{n:,.0f}".replace(",", ".")

def init_state():
    if "cart" not in st.session_state:
        # key: item_id||base_code||filling_code||pack_code -> qty
        st.session_state.cart = {}
    if "cart_open" not in st.session_state:
        st.session_state.cart_open = False

def cart_key(item_id: str, base_code: str, filling_code: str, pack_code: str) -> str:
    return f"{item_id}||{base_code}||{filling_code}||{pack_code}"

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

def build_message(cart_lines, subtotal, buyer, modality_label, when_txt, address, notes, custom_pack_flag):
    lines = [t("msg_hi"), ""]
    lines += cart_lines
    if custom_pack_flag:
        lines += ["", t("msg_subtotal_no_custom", subtotal=ars(subtotal))]
    else:
        lines += ["", t("msg_subtotal", subtotal=ars(subtotal))]
    lines += [t("msg_mode", mode=modality_label)]
    if when_txt: lines.append(t("msg_when", when=when_txt))
    if address and modality_label.lower().startswith(("deliv","deli","delivery","entrega","del")):
        lines.append(t("msg_addr", addr=address))
    if buyer: lines.append(t("msg_name", name=buyer))
    if notes: lines += ["", t("msg_notes", notes=notes)]
    if custom_pack_flag: lines += ["", t("msg_warn")]
    lines += ["", t("msg_end")]
    return "\n".join(lines)

def whatsapp_url(message: str) -> str:
    return f"https://wa.me/{BUSINESS_PHONE}?text={quote_plus(message)}"

def code_index(options, code, fallback_code=None):
    codes = [c for c, _ in options]
    if code in codes:
        return codes.index(code)
    if fallback_code and fallback_code in codes:
        return codes.index(fallback_code)
    return 0

def init_item_defaults_once():
    if not st.session_state.get("_defaults_seeded", False):
        for it in MENU_ITEMS:
            st.session_state.setdefault(f"base_{it['id']}", it.get("default_base", BASES[0][0]))
            st.session_state.setdefault(f"fill_{it['id']}", it.get("default_filling", FILLINGS[0][0]))
        st.session_state["_defaults_seeded"] = True

# =========================
# STYLES (Light look + white text buttons + big subtotal)
# =========================
st.markdown("""
<style>
  :root{
    --cap-pink:#FF5CA8;
    --cap-bg:#FFF7FB;
    --cap-card:#FFFFFF;
    --cap-text:#2C2C2C;
    --cap-border:rgba(0,0,0,.12);
  }
  .stApp, body { background: var(--cap-bg) !important; color: var(--cap-text) !important; }
  .block-container{ max-width: 1600px; padding-top: .5rem; }

  /* Buttons — force white text */
  .stButton>button{
     background: var(--cap-pink) !important;
     border:0 !important; padding:.62rem 1rem !important;
     border-radius:14px !important; font-weight:700 !important;
     box-shadow: 0 2px 10px rgba(255,92,168,.25) !important;
     color:#fff !important;
  }
  .stButton>button *{ color:#fff !important; }
  .stButton>button:hover{ filter:brightness(0.97); }

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

  /* Subtotal (big) */
  .subtotal-btn .stButton > button{
    background: var(--cap-pink) !important;
    border-radius: 20px !important;
    box-shadow: 0 8px 24px rgba(255,92,168,.25) !important;
    padding: 1.1rem 1.4rem !important;
    display:flex; justify-content:space-between; align-items:center;
    color:#fff !important;
    font-size:1.6rem !important; font-weight:900 !important;
  }

  /* Sticky cart panel */
  .cart-panel{ position: sticky; top: 1rem; }

  /* Small note */
  .cap-mini-note{ font-size:.85rem; color:#7A7A7A; margin-top:.25rem; }

  /* Make per-card columns responsive without changing Python ratios */
  .cap-card [data-testid="column"] { transition: all .12s ease; }

  /* Mobile override: first column (image) at 20% */
  @media (max-width: 768px){
   .cap-card [data-testid="column"]:nth-child(1){ flex: 0 0 20% !important; max-width:20% !important; }
   .cap-card [data-testid="column"]:nth-child(2){ flex: 0 0 43% !important; max-width:43% !important; } /* ~1.4 / (1.4+1.2) of remaining */
   .cap-card [data-testid="column"]:nth-child(3){ flex: 0 0 37% !important; max-width:37% !important; } /* ~1.2 / (1.4+1.2) of remaining */

   /* If you use the image frame, let it fill the column nicely */
   .cap-img-frame{ width:100%; aspect-ratio: 4 / 3; }
   .cap-img-frame img{ object-fit: cover; }

   /* --- Responsive override for product rows in LEFT panel --- */
    @media (max-width: 1024px){
      /* Target any 3-column horizontal row that appears AFTER the anchor */
      #menu-list-anchor ~ div [data-testid="stHorizontalBlock"] > div:nth-child(1){
        flex: 0 0 20% !important; max-width:20% !important;
      }
      #menu-list-anchor ~ div [data-testid="stHorizontalBlock"] > div:nth-child(2){
        flex: 0 0 43% !important; max-width:43% !important;
      }
      #menu-list-anchor ~ div [data-testid="stHorizontalBlock"] > div:nth-child(3){
        flex: 0 0 37% !important; max-width:37% !important;
      }
    
      /* Optional: if your Streamlit version uses inline widths, enforce flex layout */
      #menu-list-anchor ~ div [data-testid="stHorizontalBlock"]{
        display: flex !important;
        gap: var(--content-gap, 1rem);
        flex-wrap: nowrap;
      }
    }
}

</style>
""", unsafe_allow_html=True)

# =========================
# STATE INIT & TOAST
# =========================
init_state()
init_item_defaults_once() 

if "_last_added" in st.session_state:
    name, q = st.session_state.pop("_last_added")
    try:
        st.toast((f"Agregado: {name} x{q}" if lang()=="es" else f"Added: {name} x{q}"), icon="🧁")
    except Exception:
        pass

# =========================
# HEADER with Logo + Title + Language selector
# =========================
h1, h2, h3 = st.columns([0.08, 0.70, 0.22], gap="small")
with h1:
    st.title("")
    st.image("images/logo.png", use_container_width=True)
with h2:
    st.title("")
    st.markdown(f"<h1 style='margin:0'>{t('title')}</h1>", unsafe_allow_html=True)
    st.caption(t("subtitle"))
with h3:
    st.title("")
    st.selectbox("Language / Idioma", options=list(LANGS.keys()),
                 index=list(LANGS.keys()).index(lang()),
                 format_func=lambda k: LANGS[k],
                 key="lang")

st.divider()

# =========================
# LAYOUT: Menu (left) | Cart (right)
# =========================
left, right = st.columns([3, 1], gap="large")

# -------- RIGHT: CART --------
with right:
    st.markdown(f"### 🛒 {t('cart')}")
    subtotal = 0
    items_count = 0
    custom_pack_flag = False
    cart_lines = []

    # Build summary lines from current cart
    for key, qty in st.session_state.cart.items():
        item_id, base_code, fill_code, pack_code = parse_key(key)
        item = next((x for x in MENU_ITEMS if x["id"] == item_id), None)
        if not item:
            continue
        line_total = item["price"] * qty
        subtotal += line_total
        items_count += qty
        if pack_code == "custom":
            custom_pack_flag = True
        base_label = opt_label(BASES, base_code)
        fill_label = opt_label(FILLINGS, fill_code)
        pack_label = PACK_LABELS[pack_code][lang()]
        cart_lines.append(
            f"- {item['name']} · {t('base').split('(')[0].strip()}: {base_label} · "
            f"{t('filling')}: {fill_label} · {t('packaging')}: {pack_label} · "
            f"x{qty} = {ars(line_total)}"
        )

    if not cart_lines:
        st.info(t("empty_cart"))
    else:
        arrow = "▾" if not st.session_state.cart_open else "▴"
        plural = "" if (lang()=="en" and items_count==1) else ("s" if lang()=="en" else "")
        label = t("subtotal_btn", subtotal=ars(subtotal), items=items_count, plural=plural) + f"  {arrow}"
        st.markdown('<div class="subtotal-btn">', unsafe_allow_html=True)
        if st.button(label, key="toggle_cart", use_container_width=True):
            st.session_state.cart_open = not st.session_state.cart_open
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)

        if st.session_state.cart_open:
            for key, qty in list(st.session_state.cart.items()):
                item_id, base_code, fill_code, pack_code = parse_key(key)
                item = next((x for x in MENU_ITEMS if x["id"] == item_id), None)
                if not item:
                    continue
                base_label = opt_label(BASES, base_code)
                fill_label = opt_label(FILLINGS, fill_code)
                pack_label = PACK_LABELS[pack_code][lang()]

                c1, c2 = st.columns([1, 2], gap="large")  # single nesting level
                with c1:
                    if item.get("image") and os.path.exists(item["image"]):
                        st.image(item["image"], use_container_width=True)
                with c2:
                    st.write(f"**{item['name']}** · x{qty}")
                    st.caption(f"{t('base')}: {base_label} · {t('filling')}: {fill_label} · {t('packaging')}: {pack_label}")
                    if pack_code == "custom":
                        st.caption(t("pack_note"))
                    st.write(f"{t('item_total')}: **{ars(item['price'] * qty)}**")
                    if st.button(t("remove"), key=f"rm_{key}"):
                        remove_from_cart(key)
                        st.rerun()

            st.divider()
            if st.button(t("empty")):
                st.session_state.cart = {}
                st.rerun()

    # Order form
    st.divider()
    st.markdown(f"#### {t('order_details')}")
    buyer = st.text_input(t("name"), placeholder=("Tu nombre" if lang()=="es" else "Your name"))
    modality_label = st.radio(t("mode"),
                              [t("pickup"), t("delivery")],
                              index=0, horizontal=True)

    col_dt1, col_dt2 = st.columns(2)
    with col_dt1:
        use_date = st.checkbox(t("choose_dt"))
    if use_date:
        with col_dt1: d = st.date_input(t("date"), value=date.today())
        with col_dt2: tm = st.time_input(t("time"), value=time(18, 0))
        when_txt = f"{d.strftime('%d/%m/%Y')} {tm.strftime('%H:%M')}"
    else:
        when_txt = ""

    address = st.text_input(t("address"),
                            placeholder=("Calle, número, piso…" if lang()=="es" else "Street, number, floor…"))
    notes = st.text_area(t("notes"),
                         placeholder=("Ej: Sin frutos secos" if lang()=="es" else "E.g., no nuts"))

    st.divider()
    if cart_lines:
        msg = build_message(cart_lines, subtotal, buyer, modality_label, when_txt, address, notes, custom_pack_flag)
        st.markdown(
            f"<a href='{whatsapp_url(msg)}' target='_blank' "
            "style='background:#25D366;color:#fff;font-weight:800;"
            "padding:.8rem 1.2rem;border-radius:14px;box-shadow:0 2px 10px rgba(37,211,102,.25); text-decoration:none;'>"
            f"{t('wa_send')}</a>",
            unsafe_allow_html=True
        )
    else:
        st.button(t("wa_send"), disabled=True)

# -------- LEFT: MENU — 1 product per row (Col1: Photo | Col2: Base+Filling | Col3: Packaging+Qty+Button) --------
with left:
    # Anchor to target all product rows that follow
    st.markdown("<div id='menu-list-anchor'></div>", unsafe_allow_html=True)

    st.info(t("notice_title"))
    for item in MENU_ITEMS:
        st.subheader(item["name"])
        # st.caption(item["desc"][lang()])

        # layout: image | options | action
        col_img, col_opts, col_action = st.columns([0.8, 1.4, 1.2], gap="large")

        # Col 1 — Photo
        with col_img:
            if item.get("image") and os.path.exists(item["image"]):
                st.image(item["image"], use_container_width=True)
            else:
                st.markdown("🧁")

        # --- Col 2 — Base + Filling (language-proof, per-item state) ---
        with col_opts:
            base_state_key = f"base_{item['id']}"       # canonical state for base
            fill_state_key = f"fill_{item['id']}"       # canonical state for filling
            base_widget_key = f"{base_state_key}_w"     # widget key (separate)
            fill_widget_key = f"{fill_state_key}_w"     # widget key (separate)

            base_options = [c for c, _ in BASES]
            fill_options = [c for c, _ in FILLINGS]

            # compute indices from canonical state
            def idx(opts, code): 
                return opts.index(code) if code in opts else 0

            base_idx = idx(base_options, st.session_state.get(base_state_key, base_options[0]))
            fill_idx = idx(fill_options, st.session_state.get(fill_state_key, fill_options[0]))

            # render widgets bound to their own keys
            st.selectbox(
                t("base"),
                options=base_options,
                index=base_idx,
                format_func=lambda c: opt_label(BASES, c),
                key=base_widget_key
            )
            st.selectbox(
                t("filling"),
                options=fill_options,
                index=fill_idx,
                format_func=lambda c: opt_label(FILLINGS, c),
                key=fill_widget_key
            )

            # mirror widget values back to canonical per-item state
            st.session_state[base_state_key] = st.session_state[base_widget_key]
            st.session_state[fill_state_key] = st.session_state[fill_widget_key]

            # define the variables used later by the Add-to-cart button
            base_code = st.session_state[base_state_key]
            fill_code = st.session_state[fill_state_key]
        
        # --- Col 3 — Packaging + Qty + Add ---
        with col_action:
            pack_code = st.radio(
                t("packaging"),
                options=["standard", "custom"],
                horizontal=True,
                format_func=lambda c: PACK_LABELS[c][lang()],
                key=f"pack_{item['id']}"
            )
            if pack_code == "custom":
                st.caption(t("pack_note"))

            qty_val = st.number_input(t("qty6"), min_value=6, value=6, step=1, key=f"qty_{item['id']}")
            st.write(f"**{ars(item['price'])}** {t('unit_price')}")

            if st.button(t("add_to_cart"), key=f"add_{item['id']}"):
                key = cart_key(item["id"], base_code, fill_code, pack_code)  # <-- now defined
                add_to_cart(key, qty_val)
                st.session_state._last_added = (item["name"], qty_val)
                st.rerun()

        st.markdown("</div>", unsafe_allow_html=True)
        st.divider()

