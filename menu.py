# capicake_menu.py
import os, json
import streamlit as st
from urllib.parse import quote_plus
from datetime import datetime, date, time

# Optional auto-width detection (safe if missing)
try:
    from streamlit_js_eval import streamlit_js_eval
except Exception:
    streamlit_js_eval = None

# Optional: streamlit-analytics
try:
    from streamlit_analytics import track as sa_track
except Exception:
    sa_track = None

# import streamlit_analytics

# Start analytics. (Optional) persist to JSON so data survives restarts.
# streamlit_analytics.start_tracking(save_to_json="analytics.json")

# =========================
# CONFIG
# =========================
st.set_page_config(page_title="Capicake — Menú & Pedido", page_icon="🧁", layout="wide")

BUSINESS_PHONE = "5491162107712"   # WhatsApp Business CapiCake
CURRENCY = "ARS $"
MOBILE_BREAKPOINT = 768
IMG_W_MOBILE = 5000
IMG_W_DESKTOP = 5000

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
BASES = [
    ("red_velvet", {"es": "Red velvet", "en": "Red velvet", "ru": "Красный бархат"}),
    ("chocolate",  {"es": "Chocolate", "en": "Chocolate", "ru": "Шоколадный"}),
    ("vanilla",    {"es": "Vainilla", "en": "Vanilla",   "ru": "Ванильный"}),
    ("carrot",     {"es": "Carrot cake", "en": "Carrot",   "ru": "Морковный"}),
    ("lemon",      {"es": "Limón",     "en": "Lemon",    "ru": "Лимонный"})
]

# FILLINGS
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
    {"id":"carrot_charm","name":"Carrot Charm","price":7500,"image":"images/orange.png","default_base":"carrot","default_filling":"passionfruit"},
    {"id":"lemon_bliss","name":"Lemon Bliss","price":7500,"image":"images/yellow.png","default_base":"lemon","default_filling":"lemon_curd"},
    {"id":"velvet_bloom","name":"Velvet Bloom","price":7500,"image":"images/velvet.png","default_base":"red_velvet","default_filling":"berry"},
    {"id":"pink_dream","name":"Pink Dream","price":7500,"image":"images/rose.png","default_base":"vanilla","default_filling":"strawberry_confit"},
    {"id":"blue_dream","name":"Blue Dream","price":7500,"image":"images/blue.png","default_base":"vanilla","default_filling":"strawberry_confit"},
    {"id":"romance","name":"Romance","price":7500,"image":"images/joya_rosa.png","default_base":"vanilla","default_filling":"strawberry_confit"},
]

# =========================
# TRACKING HELPERS (custom events + optional file flush)
# =========================
def _log_event(name: str, **props):
    ev = {"ts": datetime.now().isoformat(timespec="seconds"), "event": name, **props}
    st.session_state.setdefault("_event_log", []).append(ev)

def _flush_events_to_disk():
    # optional: write and clear buffer so long sessions don't grow unbounded
    buf = st.session_state.get("_event_log", [])
    if not buf:
        return
    try:
        with open("events.log", "a", encoding="utf-8") as f:
            for ev in buf:
                f.write(json.dumps(ev, ensure_ascii=False) + "\n")
        st.session_state["_event_log"] = []
    except Exception:
        # ignore write errors on ephemeral fs
        pass

# =========================
# APP HELPERS
# =========================
def cart_subtotal() -> int:
    total = 0
    for key, qty in st.session_state.get("cart", {}).items():
        item_id, _, _, _ = parse_key(key)
        item = next((x for x in MENU_ITEMS if x["id"] == item_id), None)
        if item:
            total += item["price"] * qty
    return total

def is_mobile_view() -> bool:
    manual = st.session_state.get("mobile_layout", False)
    vw = st.session_state.get("_viewport_w")  # set once below
    auto = (vw is not None and vw <= MOBILE_BREAKPOINT)
    return manual or auto

# capture viewport once (first run returns None; rerun gives int)
if streamlit_js_eval:
    vw = streamlit_js_eval(js_expressions='window.innerWidth', key='VW', want_output=True)
    if isinstance(vw, (int, float)):
        st.session_state["_viewport_w"] = int(vw)

def ars(n: float) -> str:
    return f"{CURRENCY}{n:,.0f}".replace(",", ".")

def init_state():
    if "cart" not in st.session_state:
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

def init_item_defaults_once():
    if not st.session_state.get("_defaults_seeded", False):
        for it in MENU_ITEMS:
            st.session_state.setdefault(f"base_{it['id']}", it.get("default_base", BASES[0][0]))
            st.session_state.setdefault(f"fill_{it['id']}", it.get("default_filling", FILLINGS[0][0]))
        st.session_state["_defaults_seeded"] = True

DEV_WA = "541162109738"

def wa_chat_url(phone: str, text: str) -> str:
    return f"https://wa.me/{phone}?text={quote_plus(text)}"

def auto_contact_message() -> str:
    ctx = ""
    items = sum(st.session_state.get("cart", {}).values()) if st.session_state.get("cart") else 0
    if items:
        ctx = {
            "es": f" Estuve probando el sitio ahora (subtotal actual {ars(cart_subtotal())}).",
            "en": f" I was trying the site just now (current subtotal {ars(cart_subtotal())}).",
            "ru": f" Сейчас пробовал(а) сайт (текущая сумма {ars(cart_subtotal())}).",
        }.get(lang(), "")
    base = {
        "es": "¡Hola! Vi el sitio de Capicake y quiero algo similar para mi negocio. Mi rubro: ____ . ¿Podemos hablar? 😊",
        "en": "Hi! I saw the Capicake site and I'd love something similar for my business. Industry: ____ . Can we chat? 😊",
        "ru": "Здравствуйте! Увидел(а) сайт Capicake и хочу похожий для моего бизнеса. Сфера: ____ . Можно обсудить? 😊",
    }.get(lang(), "Hi! I saw the Capicake site and I'd love something similar for my business. Can we chat? 😊")
    ts = datetime.now().strftime("%Y-%m-%d %H:%M")
    tail = {
        "es": f" (mensaje auto-generado {ts})",
        "en": f" (auto-generated message {ts})",
        "ru": f" (авто-сообщение {ts})",
    }.get(lang(), f" (auto-generated {ts})")
    return base + ctx + " " + tail

# =========================
# STYLES
# =========================
st.markdown("""
<style>
  :root{ --cap-pink:#FF5CA8; --cap-bg:#FFF7FB; --cap-card:#FFFFFF; --cap-text:#2C2C2C; --cap-border:rgba(0,0,0,.12); }
  .stApp, body { background: var(--cap-bg) !important; color: var(--cap-text) !important; }
  .block-container{ max-width: 1600px; padding-top: .5rem; }

  .stButton>button{
     background: var(--cap-pink) !important; border:0 !important; padding:.62rem 1rem !important;
     border-radius:14px !important; font-weight:700 !important; box-shadow: 0 2px 10px rgba(255,92,168,.25) !important; color:#fff !important;
  }
  .stButton>button:hover{ filter:brightness(0.97); }

  .stTextInput>div>div>input, .stTextArea textarea, .stDateInput>div>div input, .stTimeInput>div>div input, .stNumberInput input, .stSelectbox div[data-baseweb="select"] input{
     background:#FFFFFF !important; color:#2C2C2C !important;
  }
  .stTextInput>div>div, .stTextArea>div>div, .stDateInput>div>div, .stTimeInput>div>div, .stNumberInput>div>div, .stSelectbox>div>div{
     border:1px solid var(--cap-border) !important; border-radius:12px !important; background:#FFFFFF !important;
  }
  input::placeholder, textarea::placeholder{ color:#9A9A9A !important; opacity:1 !important; }
  .stTextInput>div>div:focus-within, .stTextArea>div>div:focus-within, .stDateInput>div>div:focus-within, .stTimeInput>div>div:focus-within, .stNumberInput>div>div:focus-within, .stSelectbox>div>div:focus-within{
     border-color: var(--cap-pink) !important; box-shadow: 0 0 0 3px rgba(255,92,168,.18) !important;
  }

  .subtotal-btn .stButton > button{
    background: var(--cap-pink) !important; border-radius: 20px !important; box-shadow: 0 8px 24px rgba(255,92,168,.25) !important;
    padding: 1.1rem 1.4rem !important; display:flex; justify-content:space-between; align-items:center; color:#fff !important;
    font-size:1.6rem !important; font-weight:900 !important;
  }

  .cart-panel{ position: sticky; top: 1rem; }
  .cap-mini-note{ font-size:.85rem; color:#7A7A7A; margin-top:.25rem; }

  @media (max-width: 768px){
    .cap-cart-fab{
      position: fixed; right: 16px; bottom: calc(88px + env(safe-area-inset-bottom)); z-index: 10000;
      background: var(--cap-pink); color:#fff; font-weight: 800; padding: .9rem 1.1rem; border-radius: 999px;
      box-shadow: 0 10px 30px rgba(255,92,168,.35); text-decoration: none; display:inline-flex; align-items:center; gap:.5rem;
    }
    #cart-section{ scroll-margin-top: 12px; }
    .cap-cart-fab, .cap-cart-fab:link, .cap-cart-fab:visited, .cap-cart-fab:hover, .cap-cart-fab:active{ color:#fff !important; text-decoration:none !important; }
  }
  html{ scroll-behavior: smooth; }

  .cap-back-btn, .cap-back-btn:link, .cap-back-btn:visited, .cap-back-btn:hover, .cap-back-btn:active{
    display: inline-flex; align-items: center; gap: .4rem; background: transparent; color: var(--cap-text) !important;
    font-weight: 600; font-size: .85rem; padding: .35rem .6rem; border-radius: 10px; border: 1px solid var(--cap-border);
    box-shadow: none; text-decoration: none !important; opacity: .85; margin: .25rem 0 .5rem 0;
  }
  .cap-back-btn:hover{ background: rgba(0,0,0,.04); opacity: 1; }
  @media (min-width: 769px){ .cap-back-btn{ display:none; } }

  /* Footer */
  .cap-contact-footer{ max-width: 900px; margin: 2rem auto 1.2rem; padding: 1.1rem; background:#FFF; border:1px solid var(--cap-border); border-radius:16px; text-align:center; }
  .cap-contact-title{ margin:.1rem 0 .75rem; font-weight:800; font-size:1.15rem; }
  .cap-contact-actions{ display:flex; gap:.6rem; justify-content:center; flex-wrap:wrap; }
  .cap-cta, .cap-cta:link, .cap-cta:visited, .cap-cta:hover, .cap-cta:active{ display:inline-flex; align-items:center; gap:.5rem; padding:.6rem 1rem; border-radius:12px; font-weight:800; text-decoration:none !important; color:#fff !important; }
  .cap-cta--ig{ background: linear-gradient(45deg,#f58529,#dd2a7b,#8134af,#515bd4); }
  .cap-cta--wa{ background:#25D366; }
  .cap-contact-inline{
      display:flex;
      align-items:center;
      justify-content:center;
      gap:.6rem;
      flex-wrap: nowrap;          /* keep on one line */
      margin:.2rem 0 .6rem;
    }
    @media (max-width: 420px){
      .cap-contact-inline{ flex-wrap: wrap; } /* allow wrap on tiny phones */
    }
  .cap-contact-inline .cap-contact-title{ margin:0; font-weight:800; font-size:1.05rem; }
  .cap-contact-inline .cap-cta--wa{ margin-left:.1rem; }
</style>
""", unsafe_allow_html=True)

# =========================
# STATE INIT & TOAST
# =========================
init_state()
init_item_defaults_once()

# one-time page load event
if not st.session_state.get("_page_seen"):
    _log_event("page_load", lang=lang(), viewport=st.session_state.get("_viewport_w"))
    st.session_state["_page_seen"] = True

if "_last_added" in st.session_state:
    name, q = st.session_state.pop("_last_added")
    try:
        st.toast((f"Agregado: {name} x{q}" if lang()=="es" else f"Added: {name} x{q}"), icon="🧁")
    except Exception:
        pass

def render_app():
    # =========================
    # HEADER with Logo + Title + Language selector (+ track change)
    # =========================
    prev_lang = lang()
    if is_mobile_view():
        h1, h2 = st.columns([0.22, 0.22], gap="small")
        with h1:
            st.image("images/logo.png", use_container_width=False)
            st.markdown(f"<h1 style='margin:0'>{t('title')}</h1>", unsafe_allow_html=True)
            st.caption(t("subtitle"))
        with h2:
            st.selectbox(
                "Language / Idioma",
                options=list(LANGS.keys()),
                index=list(LANGS.keys()).index(lang()),
                format_func=lambda k: LANGS[k],
                key="lang"
            )
    else:
        h1, h2, h3 = st.columns([0.12, 0.75, 0.22], gap="small")
        with h1:
            st.image("images/logo.png", use_container_width=True)
        with h2:
            st.markdown(f"<h1 style='margin:0'>{t('title')}</h1>", unsafe_allow_html=True)
            st.caption(t("subtitle"))
        with h3:
            st.selectbox(
                "Language / Idioma",
                options=list(LANGS.keys()),
                index=list(LANGS.keys()).index(lang()),
                format_func=lambda k: LANGS[k],
                key="lang"
            )

    if lang() != prev_lang:
        _log_event("lang_change", old=prev_lang, new=lang())

    st.divider()

    # =========================
    # LAYOUT: Menu (left) | Cart (right)
    # =========================
    left, right = st.columns([3, 1], gap=("small" if is_mobile_view() else "large"))

    # -------- RIGHT: CART --------
    with right:
        st.markdown("<div id='cart-section'></div>", unsafe_allow_html=True)
        st.markdown(f"### 🛒 {t('cart')}")
        subtotal = 0
        items_count = 0
        custom_pack_flag = False
        cart_lines = []

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
                _log_event("cart_toggle", open=st.session_state.cart_open, items=items_count, subtotal=subtotal)
                st.rerun()
            st.markdown('</div>', unsafe_allow_html=True)

            if st.session_state.cart_open:
                if is_mobile_view():
                    for key, qty in list(st.session_state.cart.items()):
                        item_id, base_code, fill_code, pack_code = parse_key(key)
                        item = next((x for x in MENU_ITEMS if x["id"] == item_id), None)
                        if not item:
                            continue
                        base_label = opt_label(BASES, base_code)
                        fill_label = opt_label(FILLINGS, fill_code)
                        pack_label = PACK_LABELS[pack_code][lang()]
                        st.write(f"**{item['name']}** · x{qty}")
                        st.caption(f"{t('base')}: {base_label} · {t('filling')}: {fill_label} · {t('packaging')}: {pack_label}")
                        if pack_code == "custom":
                            st.caption(t("pack_note"))
                        st.write(f"{t('item_total')}: **{ars(item['price'] * qty)}**")
                        if st.button(t("remove"), key=f"rm_{key}"):
                            _log_event("remove_from_cart", key=key, qty=qty, value=item["price"]*qty)
                            remove_from_cart(key)
                            st.rerun()
                else:
                    for key, qty in list(st.session_state.cart.items()):
                        item_id, base_code, fill_code, pack_code = parse_key(key)
                        item = next((x for x in MENU_ITEMS if x["id"] == item_id), None)
                        if not item:
                            continue
                        base_label = opt_label(BASES, base_code)
                        fill_label = opt_label(FILLINGS, fill_code)
                        pack_label = PACK_LABELS[pack_code][lang()]
                        c1, c2 = st.columns([1, 2], gap="small")
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
                                _log_event("remove_from_cart", key=key, qty=qty, value=item["price"]*qty)
                                remove_from_cart(key)
                                st.rerun()

        # mobile-only back-to-menu button (anchor)
        if is_mobile_view():
            back_lbl = {"es": "⬆️ Volver al menú", "en": "⬆️ Back to menu", "ru": "⬆️ Вверх к меню"}[lang()]
            st.markdown(f"<a href='#menu-start' class='cap-back-btn'>{back_lbl}</a>", unsafe_allow_html=True)

        # Order form
        st.divider()
        st.markdown(f"#### {t('order_details')}")
        buyer = st.text_input(t("name"), placeholder=("Tu nombre" if lang()=="es" else "Your name"))
        modality_label = st.radio(t("mode"), [t("pickup"), t("delivery")], index=0, horizontal=True)

        # tracked date toggle
        prev_use_date = st.session_state.get("use_date", False)
        col_dt1, col_dt2 = st.columns(2)
        with col_dt1:
            use_date = st.checkbox(t("choose_dt"), key="use_date")
        if use_date != prev_use_date:
            _log_event("toggle_datepicker", enabled=use_date)

        if use_date:
            with col_dt1: d = st.date_input(t("date"), value=date.today(), key="date_pick")
            with col_dt2: tm = st.time_input(t("time"), value=time(18, 0), key="time_pick")
            when_txt = f"{d.strftime('%d/%m/%Y')} {tm.strftime('%H:%M')}"
        else:
            when_txt = ""

        address = st.text_input(t("address"),
                                placeholder=("Calle, número, piso…" if lang()=="es" else "Street, number, floor…"))
        notes = st.text_area(t("notes"),
                             placeholder=("Ej: Sin frutos secos" if lang()=="es" else "E.g., no nuts"))

        # Checkout: use a button to log, then open WA in new tab
        if cart_lines:
            msg = build_message(cart_lines, subtotal, buyer, modality_label, when_txt, address, notes, custom_pack_flag)
            if st.button(t("wa_send"), key="wa_checkout_btn"):
                _log_event("wa_checkout", subtotal=subtotal, items=items_count, has_custom=custom_pack_flag)
                if streamlit_js_eval:
                    streamlit_js_eval(js_expressions=f"window.open('{whatsapp_url(msg)}','_blank')",
                                      key=f"WA_OPEN_{subtotal}_{items_count}",
                                      want_output=False)
                else:
                    st.markdown(f"[{t('wa_send')}]({whatsapp_url(msg)})")
        else:
            st.button(t("wa_send"), disabled=True)

    # -------- LEFT: MENU — items --------
    with left:
        st.markdown("<div id='menu-start'></div>", unsafe_allow_html=True)
        st.info(t("notice_title"))

        # Floating Cart button on mobile
        if is_mobile_view():
            subtotal_val = cart_subtotal()
            label = f"🛒 {ars(subtotal_val)}" if subtotal_val > 0 else f"🛒 {t('cart')}"
            st.markdown(f"<a href='#cart-section' class='cap-cart-fab'>{label}</a>", unsafe_allow_html=True)

        for item in MENU_ITEMS:
            st.subheader(item["name"])
            col_img, col_opts, col_action = st.columns([0.8, 1.4, 1.2], gap="small")

            with col_img:
                if item.get("image") and os.path.exists(item["image"]):
                    st.image(item["image"], width=IMG_W_DESKTOP)
                else:
                    st.markdown("🧁")

            with col_opts:
                base_state_key = f"base_{item['id']}"
                fill_state_key = f"fill_{item['id']}"
                base_widget_key = f"{base_state_key}_w"
                fill_widget_key = f"{fill_state_key}_w"

                base_options = [c for c, _ in BASES]
                fill_options = [c for c, _ in FILLINGS]

                def idx(opts, code):
                    return opts.index(code) if code in opts else 0

                base_idx = idx(base_options, st.session_state.get(base_state_key, base_options[0]))
                fill_idx = idx(fill_options, st.session_state.get(fill_state_key, fill_options[0]))

                prev_base = st.session_state.get(base_state_key, base_options[0])
                prev_fill = st.session_state.get(fill_state_key, fill_options[0])

                st.selectbox(t("base"), options=base_options, index=base_idx,
                             format_func=lambda c: opt_label(BASES, c), key=base_widget_key)
                st.selectbox(t("filling"), options=fill_options, index=fill_idx,
                             format_func=lambda c: opt_label(FILLINGS, c), key=fill_widget_key)

                st.session_state[base_state_key] = st.session_state[base_widget_key]
                st.session_state[fill_state_key] = st.session_state[fill_widget_key]

                if st.session_state[base_state_key] != prev_base:
                    _log_event("base_change", item_id=item["id"], base=st.session_state[base_state_key])
                if st.session_state[fill_state_key] != prev_fill:
                    _log_event("filling_change", item_id=item["id"], filling=st.session_state[fill_state_key])

                base_code = st.session_state[base_state_key]
                fill_code = st.session_state[fill_state_key]

            with col_action:
                pack_key = f"pack_{item['id']}"
                prev_pack = st.session_state.get(pack_key, "standard")
                pack_code = st.radio(t("packaging"), options=["standard", "custom"],
                                     horizontal=True, format_func=lambda c: PACK_LABELS[c][lang()],
                                     key=pack_key)
                if pack_code != prev_pack:
                    _log_event("pack_change", item_id=item["id"], pack=pack_code)

                if pack_code == "custom":
                    st.caption(t("pack_note"))

                qty_key = f"qty_{item['id']}"
                prev_qty = st.session_state.get(qty_key, 6)
                qty_val = st.number_input(t("qty6"), min_value=6, value=prev_qty, step=1, key=qty_key)
                if qty_val != prev_qty:
                    _log_event("qty_change", item_id=item["id"], qty=int(qty_val))

                st.write(f"**{ars(item['price'])}** {t('unit_price')}")

                if st.button(t("add_to_cart"), key=f"add_{item['id']}"):
                    key = cart_key(item["id"], base_code, fill_code, pack_code)
                    add_to_cart(key, qty_val)
                    _log_event("add_to_cart",
                               item_id=item["id"], item_name=item["name"],
                               base=base_code, filling=fill_code,
                               qty=int(qty_val), value=item["price"] * int(qty_val))
                    st.session_state._last_added = (item["name"], qty_val)
                    st.rerun()

            if is_mobile_view():
                st.divider()
            else:
                st.subheader("")

    # ---------- CONTACT FOOTER ----------
    lbl_title = {
        "es": "¿Querés un sitio como este?",
        "en": "Want a site like this?",
        "ru": "Хотите такой же сайт?",
    }[lang()]
    
    msg = auto_contact_message()
    wa_url = wa_chat_url(DEV_WA, msg)
    
    st.divider()
    st.markdown(
        f"""
        <div class="cap-contact-footer">
          <div class="cap-contact-inline">
            <span class="cap-contact-title">{lbl_title}</span>
            <a class="cap-cta cap-cta--wa" href="{wa_url}" target="_blank" rel="noopener">📲 WhatsApp</a>
          </div>
        </div>
        """,
        unsafe_allow_html=True
        )
    
    if st.button("📲 WhatsApp", key="footer_wa_btn"):
        _log_event("contact_whatsapp_footer", msg_len=len(msg))
        if streamlit_js_eval:
            streamlit_js_eval(js_expressions=f"window.open('{wa_url}','_blank')",
                              key="WA_CONTACT_OPEN", want_output=False)
        else:
            st.markdown(f"[📲 WhatsApp]({wa_url})")

    # Periodically flush custom events to disk
    _flush_events_to_disk()

# =========================
# RUN (with streamlit-analytics if available)
# =========================
if sa_track:
    with sa_track(unsafe_password=None):  # open /?analytics=on to view the built-in dashboard
        render_app()
else:
    render_app()
