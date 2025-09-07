# capicake_menu.py
import os
import streamlit as st
from urllib.parse import quote_plus
from datetime import datetime, date, time

# ---------- Optional helpers (safe if missing) ----------
try:
    from streamlit_js_eval import streamlit_js_eval
except Exception:
    streamlit_js_eval = None

# =========================
# CONFIG (must be first Streamlit call)
# =========================
st.set_page_config(page_title="Capicake — Menú & Pedido", page_icon="🧁", layout="wide")

BUSINESS_PHONE = "5491162107712"   # WhatsApp Business CapiCake
CURRENCY = "ARS $"
MOBILE_BREAKPOINT = 768
DISCOUNT_RATE_FIRST = 0.10  # 10% OFF first order
DISCOUNT_RATE_SET12 = 0.10  # extra 10% OFF when total qty of same item in cart >= 12

# =========================
# LANGUAGE / I18N
# =========================
if "lang" not in st.session_state:
    st.session_state.lang = "es"  # default: Español (AR)

LANGS = {"es": "🇦🇷 Español (AR)", "en": "🇬🇧 English", "ru": "🇷🇺 Русский"}

TR = {
    "es": {
        "title": "Menú & Pedido",
        "subtitle": "Elegí tus cupcakes, armá el carrito y enviá el pedido por WhatsApp en 1 click.",
        "discount_banner_l1": "🎉 10% OFF en tu primer pedido",
        "discount_banner_l2": "➕ 10% OFF extra en sets de 12+ del mismo tipo",
        "discount_note_short": "10% primer pedido. +10% extra en sets de 12+ del mismo tipo.",
        "discount_checkbox": "Es mi primer pedido (aplicar 10% OFF)",
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
        "qty6": "Cantidad (mín. 6, múltiplos de 6)",
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
        "msg_discount_first": "• 10% de descuento por primer pedido.",
        "msg_discount_set12": "• 10% extra aplicado en ítems con 12+ del mismo tipo.",
        "msg_end": "¿Me confirmás disponibilidad y total? ¡Gracias! 🧁",
        "notice_title": "ℹ️ Diseño artesanal: puede variar",
        "qty_invalid": "⚠️ Solo se permiten cantidades múltiplos de 6 (6, 12, 18…).",
        "set12_note": "Aplicado +10% por set de 12+ del mismo tipo.",
    },
    "en": {
        "title": "Menu & Order",
        "subtitle": "Pick your cupcakes, build the cart and send your order via WhatsApp in 1 click.",
        "discount_banner_l1": "🎉 10% OFF your first order",
        "discount_banner_l2": "➕ Extra 10% OFF on 12+ sets of the same type",
        "discount_note_short": "10% first order. +10% extra on 12+ sets (same type).",
        "discount_checkbox": "It's my first order (apply 10% OFF)",
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
        "qty6": "Quantity (min 6, multiples of 6)",
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
        "msg_discount_first": "• 10% first-order discount.",
        "msg_discount_set12": "• Extra 10% applied on items with 12+ of the same type.",
        "msg_end": "Could you confirm availability and total? Thanks! 🧁",
        "notice_title": "ℹ️ Handmade design: variations may occur",
        "qty_invalid": "⚠️ Only multiples of 6 are allowed (6, 12, 18…).",
        "set12_note": "Extra 10% applied for 12+ of the same type.",
    },
    "ru": {
        "title": "Меню и заказ",
        "subtitle": "Выберите капкейки, соберите корзину и отправьте заказ в WhatsApp в один клик.",
        "discount_banner_l1": "🎉 −10% на первый заказ",
        "discount_banner_l2": "➕ Ещё −10% при 12+ одного и того же вида",
        "discount_note_short": "−10% первый заказ. Ещё −10% при 12+ одного вида.",
        "discount_checkbox": "Это мой первый заказ (применить −10%)",
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
        "qty6": "Количество (мин. 6, кратно 6)",
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
        "msg_warn": "⚠️ Выбрана индивидуальная упаковка для некоторых позиций. Доп. стоимость согласуем в WhatsApp.",
        "msg_discount_first": "• −10% за первый заказ.",
        "msg_discount_set12": "• Ещё −10% для позиций с 12+ одного вида.",
        "msg_end": "Подтвердите, пожалуйста, доступность и итоговую стоимость. Спасибо! 🧁",
        "notice_title": "ℹ️ Ручная работа: возможны отличия",
        "qty_invalid": "⚠️ Разрешены только количества, кратные 6 (6, 12, 18…).",
        "set12_note": "Применена доп. скидка −10% за 12+ одного вида.",
    },
}

# BASES / FILLINGS / PACKAGING
BASES = [
    ("red_velvet", {"es": "Red velvet", "en": "Red velvet", "ru": "Красный бархат"}),
    ("chocolate",  {"es": "Chocolate", "en": "Chocolate", "ru": "Шоколадный"}),
    ("vanilla",    {"es": "Vainilla", "en": "Vanilla",   "ru": "Ванильный"}),
    ("carrot",     {"es": "Carrot cake", "en": "Carrot",   "ru": "Морковный"}),
    ("lemon",      {"es": "Limón",     "en": "Lemon",    "ru": "Лимонный"})
]
FILLINGS = [
    ("strawberry_confit", {"es": "Confit de frutilla", "en": "Strawberry confit", "ru": "Клубничное конфи"}),
    ("berry",             {"es": "Frutos rojos",        "en": "Berry mix",        "ru": "Ягодная"}),
    ("dulce",             {"es": "Dulce de leche",     "en": "Dulce de leche",   "ru": "Дульсе де лече"}),
    ("chocolate_praline", {"es": "Praliné de chocolate","en": "Chocolate praline","ru": "Шоколадное пралине"}),
    ("passionfruit",      {"es": "Maracuyá",           "en": "Passion fruit",    "ru": "Маракуйя"}),
    ("lemon_curd",        {"es": "Curd de limón",      "en": "Lemon curd",       "ru": "Лимонный курд"}),
    ("cappuccino",        {"es": "Capuchino",          "en": "Cappuccino",       "ru": "Капучино"})
]
PACK_LABELS = {
    "standard": {"es": "Estandar", "en": "Standard", "ru": "Стандартная"},
    "custom":   {"es": "Personalizado", "en": "Custom", "ru": "Индивидуальная"},
}

# =========================
# DATA
# =========================
MENU_ITEMS = [
    {"id":"carrot_charm","name":"Carrot Charm","price":8500,"image":"images/orange.png","default_base":"carrot","default_filling":"passionfruit"},
    {"id":"lemon_bliss","name":"Lemon Bliss","price":8500,"image":"images/yellow.png","default_base":"lemon","default_filling":"lemon_curd"},
    {"id":"velvet_bloom","name":"Velvet Bloom","price":8500,"image":"images/velvet.png","default_base":"red_velvet","default_filling":"berry"},
    {"id":"pink_dream","name":"Pink Dream","price":8500,"image":"images/rose.png","default_base":"vanilla","default_filling":"strawberry_confit"},
    {"id":"blue_dream","name":"Blue Dream","price":8500,"image":"images/blue.png","default_base":"vanilla","default_filling":"strawberry_confit"},
    {"id":"romance","name":"Romance","price":8500,"image":"images/joya_rosa.png","default_base":"vanilla","default_filling":"strawberry_confit"},
]

# =========================
# APP HELPERS
# =========================
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

def is_mobile_view() -> bool:
    manual = st.session_state.get("mobile_layout", False)
    vw = st.session_state.get("_viewport_w")
    auto = (vw is not None and vw <= MOBILE_BREAKPOINT)
    return manual or auto

# capture viewport
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
    if "first_order" not in st.session_state:
        st.session_state.first_order = True  # default ON to showcase promo

def init_item_defaults_once():
    if not st.session_state.get("_defaults_seeded", False):
        for it in MENU_ITEMS:
            st.session_state.setdefault(f"base_{it['id']}", it.get("default_base", BASES[0][0]))
            st.session_state.setdefault(f"fill_{it['id']}", it.get("default_filling", FILLINGS[0][0]))
        st.session_state["_defaults_seeded"] = True

def cart_key(item_id: str, base_code: str, filling_code: str, pack_code: str) -> str:
    return f"{item_id}||{base_code}||{filling_code}||{pack_code}"

def parse_key(key: str):
    parts = key.split("||")
    parts += ["", "", "", ""]
    return parts[0], parts[1], parts[2], parts[3]

def add_to_cart(key: str, qty: int):
    """Guard: only multiples of 6 allowed."""
    if qty >= 6 and qty % 6 == 0:
        st.session_state.cart[key] = st.session_state.cart.get(key, 0) + qty

def remove_from_cart(key: str):
    if key in st.session_state.cart:
        del st.session_state.cart[key]

def first_order_active() -> bool:
    return bool(st.session_state.get("first_order", False))

def agg_qty_by_item():
    """Return dict item_id -> total qty across all cart lines (ignores base/filling/pack)."""
    totals = {}
    for key, qty in st.session_state.get("cart", {}).items():
        item_id, _, _, _ = parse_key(key)
        totals[item_id] = totals.get(item_id, 0) + qty
    return totals

def unit_price_after_discounts(p: int, item_qty_total: int) -> int:
    """
    Apply stacked discounts multiplicatively:
      - 10% first-order (if active)
      - extra 10% if total qty of the same item in cart >= 12
    Rounds to nearest peso.
    """
    price = float(p)
    if first_order_active():
        price *= (1.0 - DISCOUNT_RATE_FIRST)
    if item_qty_total >= 12:
        price *= (1.0 - DISCOUNT_RATE_SET12)
    return int(round(price))

def totals_after_discounts():
    """Returns (subtotal_original, subtotal_discounted, item_qty_totals dict)."""
    item_totals = agg_qty_by_item()
    subtotal_orig = 0
    subtotal_disc = 0
    for key, qty in st.session_state.get("cart", {}).items():
        item_id, _, _, _ = parse_key(key)
        item = next((x for x in MENU_ITEMS if x["id"] == item_id), None)
        if not item:
            continue
        p = item["price"]
        pd = unit_price_after_discounts(p, item_totals.get(item_id, qty))
        subtotal_orig += p * qty
        subtotal_disc += pd * qty
    return subtotal_orig, subtotal_disc, item_totals

def build_message(cart_lines, subtotal_after, buyer, modality_label, when_txt, address, notes,
                  custom_pack_flag, apply_first: bool, apply_set12: bool):
    lines = [t("msg_hi"), ""]
    lines += cart_lines
    sub_key = "msg_subtotal_no_custom" if custom_pack_flag else "msg_subtotal"
    lines += [TR[lang()][sub_key].format(subtotal=ars(subtotal_after))]
    # Separate promo lines (only if applicable)
    if apply_first:
        lines.append(t("msg_discount_first"))
    if apply_set12:
        lines.append(t("msg_discount_set12"))
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

DEV_WA = "541162109738"
def wa_chat_url(phone: str, text: str) -> str:
    return f"https://wa.me/{phone}?text={quote_plus(text)}"

def auto_contact_message() -> str:
    # show current discounted subtotal
    _, sub_d, _ = totals_after_discounts()
    ctx = ""
    items = sum(st.session_state.get("cart", {}).values()) if st.session_state.get("cart") else 0
    if items:
        ctx = {
            "es": f" Estuve probando el sitio ahora (subtotal actual {ars(sub_d)}).",
            "en": f" I was trying the site just now (current subtotal {ars(sub_d)}).",
            "ru": f" Сейчас пробовал(а) сайт (текущая сумма {ars(sub_d)}).",
        }.get(lang(), "")
    base = {
        "es": "¡Hola! Vi el sitio de Capicake y quiero algo similar para mi negocio. Mi rubro: ____ . ¿Podemos hablar? 😊",
        "en": "Hi! I saw the Capicake site and I'd love something similar for my business. Industry: ____ . Can we chat? 😊",
        "ru": "Здравствуйте! Увидел(а) сайт Capicake и хочу похожий для моего бизнеса. Сфера: ____ . Можно обсудить? 😊",
    }.get(lang(), "Hi! I saw the Capicake site and I'd love something similar for my business. Can we chat? 😊")
    ts = datetime.now().strftime("%Y-%m-%d %H:%M")
    tail = {"es": f" (mensaje auto-generado {ts})", "en": f" (auto-generated message {ts})", "ru": f" (авто-сообщение {ts})"}.get(lang(), f" (auto-generated {ts})")
    return base + ctx + " " + tail

# =========================
# STYLES
# =========================
st.markdown("""
<style>
  :root{
    --cap-pink:#FF5CA8; --cap-red:#D91E41;
    --cap-bg:#FFF7FB; --cap-card:#FFFFFF; --cap-text:#2C2C2C; --cap-border:rgba(0,0,0,.12);
  }
  .stApp, body { background: var(--cap-bg) !important; color: var(--cap-text) !important; }
  .block-container{ max-width: 1600px; padding-top: .5rem; }

  /* Banner */
  .cap-discount-banner{
    background: #FFE4EA; border: 2px dashed var(--cap-red);
    color: var(--cap-red); font-weight: 900; text-align:center;
    padding: .85rem 1rem; border-radius: 16px; margin: .3rem 0 1rem 0; font-size: 1.05rem;
    line-height: 1.25;
  }

  /* Price styles */
  .cap-price { display:flex; align-items:center; gap:.5rem; flex-wrap:wrap; }
  .price-old{ color: var(--cap-red); text-decoration: line-through; font-weight: 800; opacity:.9; }
  .price-new{ color: var(--cap-red); font-weight: 900; font-size: 1.1rem; }
  .cap-mini-note{ font-size:.85rem; color:#7A7A7A; margin-top:.25rem; }

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

  /* Floating Cart button (mobile only) */
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

  /* Footer contact inline */
  .cap-contact-footer{ max-width: 900px; margin: 2rem auto 1.2rem; padding: 1.1rem; background:#FFF; border:1px solid var(--cap-border); border-radius:16px; text-align:center; }
  .cap-contact-inline{ display:flex; align-items:center; justify-content:center; gap:.6rem; flex-wrap: nowrap; margin:.2rem 0 .6rem; }
  .cap-contact-title{ margin:0; font-weight:800; font-size:1.05rem; }
  .cap-cta, .cap-cta:link, .cap-cta:visited, .cap-cta:hover, .cap-cta:active{ display:inline-flex; align-items:center; gap:.5rem; padding:.6rem 1rem; border-radius:12px; font-weight:800; text-decoration:none !important; color:#fff !important; }
  .cap-cta--wa{ background:#25D366; }
</style>
""", unsafe_allow_html=True)

# =========================
# UI HELPERS (HTML-safe blocks)
# =========================
def render_price_pair(label: str, old_amt: str, new_amt: str):
    st.markdown(
        f"""
        <div class="cap-price">
          <strong>{label}:</strong>
          <span class="price-old">{old_amt}</span>
          <span class="price-new">{new_amt}</span>
        </div>
        """,
        unsafe_allow_html=True,
    )

# =========================
# CORE RENDER
# =========================
def main():
    init_state()
    init_item_defaults_once()

    # ----- Header -----
    if is_mobile_view():
        h1, h2 = st.columns([0.22, 0.22], gap="small")
        with h1:
            st.image("images/logo.png", use_container_width=False)
            st.markdown(f"<h1 style='margin:0'>{t('title')}</h1>", unsafe_allow_html=True)
            st.caption(t("subtitle"))
        with h2:
            st.selectbox("Language / Idioma",
                         options=list(LANGS.keys()),
                         index=list(LANGS.keys()).index(lang()),
                         format_func=lambda k: LANGS[k],
                         key="lang")
    else:
        h1, h2, h3 = st.columns([0.12, 0.75, 0.22], gap="small")
        with h1:
            st.image("images/logo.png", use_container_width=True)
        with h2:
            st.markdown(f"<h1 style='margin:0'>{t('title')}</h1>", unsafe_allow_html=True)
        with h3:
            st.selectbox("Language / Idioma",
                         options=list(LANGS.keys()),
                         index=list(LANGS.keys()).index(lang()),
                         format_func=lambda k: LANGS[k],
                         key="lang")

    # PROMO banner (two lines)
    st.markdown(
        f"<div class='cap-discount-banner'><div>{t('discount_banner_l1')}</div><div>{t('discount_banner_l2')}</div></div>",
        unsafe_allow_html=True
    )

    st.divider()

    # ----- Layout -----
    left, right = st.columns([3, 1], gap=("small" if is_mobile_view() else "large"))

    # ===== RIGHT: CART =====
    with right:
        st.markdown("<div id='cart-section'></div>", unsafe_allow_html=True)
        st.markdown(f"### 🛒 {t('cart')}")
        custom_pack_flag = False
        cart_lines = []

        # Build totals + aggregate counts per item for set-of-12 discount
        subtotal_orig, subtotal_disc, item_totals = totals_after_discounts()

        for key, qty in st.session_state.get("cart", {}).items():
            item_id, base_code, fill_code, pack_code = parse_key(key)
            item = next((x for x in MENU_ITEMS if x["id"] == item_id), None)
            if not item:
                continue
            base_label = opt_label(BASES, base_code)
            fill_label = opt_label(FILLINGS, fill_code)
            pack_label = PACK_LABELS[pack_code][lang()]
            if pack_code == "custom":
                custom_pack_flag = True

            cart_lines.append(
                f"- {item['name']} · {t('base').split('(')[0].strip()}: {base_label} · "
                f"{t('filling')}: {fill_label} · {t('packaging')}: {pack_label} · x{qty}"
            )

        if not cart_lines:
            st.info(t("empty_cart"))
        else:
            # Subtotal preview (old -> new)
            if subtotal_orig != subtotal_disc:
                st.markdown(
                    f"<div class='cap-price'><span class='price-old'>{ars(subtotal_orig)}</span>"
                    f"<span class='price-new'>{ars(subtotal_disc)}</span></div>"
                    f"<div class='cap-mini-note'>{t('discount_note_short')}</div>",
                    unsafe_allow_html=True
                )

            # Subtotal button
            items_count = sum(st.session_state.cart.values())
            plural = "" if (lang()=="en" and items_count==1) else ("s" if lang()=="en" else "")
            arrow = "▾" if not st.session_state.cart_open else "▴"
            label = t("subtotal_btn", subtotal=ars(subtotal_disc), items=items_count, plural=plural) + f"  {arrow}"
            st.markdown('<div class="subtotal-btn">', unsafe_allow_html=True)
            if st.button(label, key="toggle_cart", use_container_width=True):
                st.session_state.cart_open = not st.session_state.cart_open
                st.rerun()
            st.markdown('</div>', unsafe_allow_html=True)

            if st.session_state.cart_open:
                for key, qty in list(st.session_state.cart.items()):
                    item_id, base_code, fill_code, pack_code = parse_key(key)
                    item = next((x for x in MENU_ITEMS if x["id"] == item_id), None)
                    if not item: continue
                    base_label = opt_label(BASES, base_code)
                    fill_label = opt_label(FILLINGS, fill_code)
                    pack_label = PACK_LABELS[pack_code][lang()]
                    p = item["price"]
                    line_orig = p * qty
                    pd_unit = unit_price_after_discounts(p, item_totals.get(item_id, qty))
                    line_disc = pd_unit * qty
                    set12_applied = item_totals.get(item_id, 0) >= 12

                    if is_mobile_view():
                        st.write(f"**{item['name']}** · x{qty}")
                        st.caption(f"{t('base')}: {base_label} · {t('filling')}: {fill_label} · {t('packaging')}: {pack_label}")
                        if pack_code == "custom": st.caption(t("pack_note"))
                        render_price_pair(t("item_total"), ars(line_orig), ars(line_disc))
                        if set12_applied: st.caption(t("set12_note"))
                        if st.button(t("remove"), key=f"rm_{key}"):
                            remove_from_cart(key); st.rerun()
                    else:
                        c1, c2 = st.columns([1, 2], gap="small")
                        with c1:
                            if item.get("image") and os.path.exists(item["image"]):
                                st.image(item["image"], use_container_width=True)
                        with c2:
                            st.write(f"**{item['name']}** · x{qty}")
                            st.caption(f"{t('base')}: {base_label} · {t('filling')}: {fill_label} · {t('packaging')}: {pack_label}")
                            if pack_code == "custom": st.caption(t("pack_note"))
                            render_price_pair(t("item_total"), ars(line_orig), ars(line_disc))
                            if set12_applied: st.caption(t("set12_note"))
                            if st.button(t("remove"), key=f"rm_{key}"):
                                remove_from_cart(key); st.rerun()

        # mobile-only back-to-menu link
        if is_mobile_view():
            back_lbl = {"es": "⬆️ Volver al menú", "en": "⬆️ Back to menu", "ru": "⬆️ Вверх к меню"}[lang()]
            st.markdown(f"<a href='#menu-start' class='cap-back-btn'>{back_lbl}</a>", unsafe_allow_html=True)

        # ----- Order form -----
        st.divider()
        st.markdown(f"#### {t('order_details')}")
        buyer = st.text_input(t("name"), placeholder=("Tu nombre" if lang()=="es" else "Your name"))
        modality_label = st.radio(t("mode"), [t("pickup"), t("delivery")], index=0, horizontal=True)

        # First-order checkbox
        st.checkbox(t("discount_checkbox"), key="first_order")

        col_dt1, col_dt2 = st.columns(2)
        with col_dt1:
            use_date = st.checkbox(t("choose_dt"), key="use_date")
        when_txt = ""
        if use_date:
            with col_dt1: d = st.date_input(t("date"), value=date.today(), key="date_pick")
            with col_dt2: tm = st.time_input(t("time"), value=time(18, 0), key="time_pick")
            when_txt = f"{d.strftime('%d/%m/%Y')} {tm.strftime('%H:%M')}"

        address = st.text_input(t("address"),
                                placeholder=("Calle, número, piso…" if lang()=="es" else "Street, number, floor…"))
        notes = st.text_area(t("notes"),
                             placeholder=("Ej: Sin frutos secos" if lang()=="es" else "E.g., no nuts"))

        # Build final message + WA button
        if st.session_state.get("cart"):
            _, subtotal_disc, item_totals = totals_after_discounts()
            apply_first = first_order_active()
            apply_set12 = any(q >= 12 for q in item_totals.values())
            msg = build_message(
                cart_lines, subtotal_disc, buyer, modality_label, when_txt, address, notes,
                custom_pack_flag, apply_first, apply_set12
            )
            if st.button(t("wa_send"), key="wa_checkout_btn"):
                if streamlit_js_eval:
                    streamlit_js_eval(js_expressions=f"window.open('{whatsapp_url(msg)}','_blank')",
                                      key=f"WA_OPEN_{subtotal_disc}_{len(st.session_state.cart)}", want_output=False)
                else:
                    st.markdown(f"[{t('wa_send')}]({whatsapp_url(msg)})")
        else:
            st.button(t("wa_send"), disabled=True)

    # ===== LEFT: MENU =====
    with left:
        st.markdown("<div id='menu-start'></div>", unsafe_allow_html=True)
        st.info(t("notice_title"))

        # Floating Cart button on mobile
        if is_mobile_view():
            _, sub_d, _ = totals_after_discounts()
            label = f"🛒 {ars(sub_d)}" if sub_d > 0 else f"🛒 {t('cart')}"
            st.markdown(f"<a href='#cart-section' class='cap-cart-fab'>{label}</a>", unsafe_allow_html=True)

        # Helper: current qty in cart for a given item_id
        def current_qty_for_item(item_id: str) -> int:
            total = 0
            for key, q in st.session_state.get("cart", {}).items():
                iid, _, _, _ = parse_key(key)
                if iid == item_id: total += q
            return total

        for item in MENU_ITEMS:
            st.subheader(item["name"])
            col_img, col_opts, col_action = st.columns([0.8, 1.4, 1.2], gap="small")

            with col_img:
                if item.get("image") and os.path.exists(item["image"]):
                    st.image(item["image"], use_container_width=True)
                else:
                    st.markdown("🧁")

            with col_opts:
                base_state_key = f"base_{item['id']}"
                fill_state_key = f"fill_{item['id']}"
                base_widget_key = f"{base_state_key}_w"
                fill_widget_key = f"{fill_state_key}_w"

                base_options = [c for c, _ in BASES]
                fill_options = [c for c, _ in FILLINGS]

                def idx(opts, code): return opts.index(code) if code in opts else 0
                base_idx = idx(base_options, st.session_state.get(base_state_key, base_options[0]))
                fill_idx = idx(fill_options, st.session_state.get(fill_state_key, fill_options[0]))

                st.selectbox(t("base"), options=base_options, index=base_idx,
                             format_func=lambda c: opt_label(BASES, c), key=base_widget_key)
                st.selectbox(t("filling"), options=fill_options, index=fill_idx,
                             format_func=lambda c: opt_label(FILLINGS, c), key=fill_widget_key)

                st.session_state[base_state_key] = st.session_state[base_widget_key]
                st.session_state[fill_state_key] = st.session_state[fill_widget_key]

                base_code = st.session_state[base_state_key]
                fill_code = st.session_state[fill_state_key]

            with col_action:
                pack_key = f"pack_{item['id']}"
                pack_code = st.radio(t("packaging"), options=["standard", "custom"],
                                     horizontal=True, format_func=lambda c: PACK_LABELS[c][lang()],
                                     key=pack_key)

                if pack_code == "custom":
                    st.caption(t("pack_note"))

                qty_key = f"qty_{item['id']}"
                qty_val = st.number_input(
                    t("qty6"),
                    min_value=6,
                    value=st.session_state.get(qty_key, 6),
                    step=6,
                    key=qty_key
                )
                is_valid_qty = (qty_val >= 6) and (qty_val % 6 == 0)
                if not is_valid_qty:
                    st.markdown(f"<span style='color:#D91E41'>{t('qty_invalid')}</span>", unsafe_allow_html=True)

                # PRICE BOX (per-unit) — reflect expected discounts if this is added
                p = item["price"]
                predicted_total_for_item = current_qty_for_item(item["id"]) + int(qty_val)
                pd_unit = unit_price_after_discounts(p, predicted_total_for_item)
                if pd_unit != p:
                    st.markdown(
                        f"""
                        <div class='cap-price'>
                          <span class='price-old'>{ars(p)}</span>
                          <span class='price-new'>{ars(pd_unit)}</span>
                        </div>
                        <div class='cap-mini-note'>{t('discount_note_short')}</div>
                        """,
                        unsafe_allow_html=True
                    )
                else:
                    st.write(f"**{ars(p)}** {t('unit_price')}")

                if st.button(t("add_to_cart"), key=f"add_{item['id']}", disabled=not is_valid_qty):
                    key = cart_key(item["id"], base_code, fill_code, pack_code)
                    add_to_cart(key, int(qty_val))
                    st.session_state._last_added = (item["name"], int(qty_val))
                    st.rerun()

            st.divider()

    # ----- Footer contact (inline title + WA button) -----
    lbl_title = {"es": "¿Querés un sitio como este?", "en": "Want a site like this?", "ru": "Хотите такой же сайт?"}[lang()]
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

# =========================
# RUN
# =========================
if __name__ == "__main__":
    main()
