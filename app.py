import html
import json
from pathlib import Path
from urllib.parse import quote

import streamlit as st
import streamlit.components.v1 as components


st.set_page_config(
    page_title="ПСИ-БЛОК",
    page_icon="favicon.jpg",
    layout="wide",
)

LOGO_PATH = Path(__file__).resolve().parent / "logo.png"


# ---------------------------------------------------------------------
# Декоративный фон
# ---------------------------------------------------------------------

NEURON_SVG = """
<svg xmlns="http://www.w3.org/2000/svg" width="1000" height="800" viewBox="0 0 1000 800">
  <g fill="none" stroke="#4389B5" stroke-opacity="0.13" stroke-width="2">
    <path d="M25 92 L130 145 L225 80 L340 150 L455 70 L565 145 L690 86 L815 155 L955 82"/>
    <path d="M130 145 L175 290 L300 340 L420 250 L565 145"/>
    <path d="M225 80 L245 20"/>
    <path d="M340 150 L325 235 L420 250 L500 360 L635 325 L760 390"/>
    <path d="M455 70 L485 20"/>
    <path d="M565 145 L635 210 L760 170 L815 155"/>
    <path d="M690 86 L710 25"/>
    <path d="M815 155 L860 275 L955 310"/>
    <path d="M175 290 L100 430 L215 510 L300 430 L300 340"/>
    <path d="M420 250 L380 430 L500 520 L635 450 L635 325"/>
    <path d="M760 390 L840 500 L950 455"/>
    <path d="M100 430 L55 600 L180 700 L310 635 L300 520 L215 510"/>
    <path d="M500 520 L455 660 L570 760 L710 675 L635 560 L635 450"/>
    <path d="M840 500 L815 650 L930 735"/>
    <path d="M310 635 L390 760"/>
  </g>
  <g fill="#4389B5" fill-opacity="0.17" stroke="#FFFFFF" stroke-opacity="0.8" stroke-width="3">
    <circle cx="25" cy="92" r="8"/><circle cx="130" cy="145" r="12"/>
    <circle cx="225" cy="80" r="9"/><circle cx="340" cy="150" r="12"/>
    <circle cx="455" cy="70" r="8"/><circle cx="565" cy="145" r="11"/>
    <circle cx="690" cy="86" r="9"/><circle cx="815" cy="155" r="12"/>
    <circle cx="955" cy="82" r="8"/><circle cx="175" cy="290" r="10"/>
    <circle cx="300" cy="340" r="8"/><circle cx="420" cy="250" r="12"/>
    <circle cx="500" cy="360" r="9"/><circle cx="635" cy="325" r="12"/>
    <circle cx="760" cy="390" r="10"/><circle cx="100" cy="430" r="8"/>
    <circle cx="215" cy="510" r="12"/><circle cx="380" cy="430" r="9"/>
    <circle cx="500" cy="520" r="12"/><circle cx="635" cy="450" r="9"/>
    <circle cx="840" cy="500" r="11"/><circle cx="180" cy="700" r="9"/>
    <circle cx="310" cy="635" r="11"/><circle cx="570" cy="760" r="8"/>
    <circle cx="710" cy="675" r="12"/><circle cx="930" cy="735" r="9"/>
  </g>
</svg>
"""

neuron_background = quote(NEURON_SVG, safe="")


# ---------------------------------------------------------------------
# Каталог техник
# ---------------------------------------------------------------------

TECHNIQUES = {
    "decision_tree": {
        "title": "Дерево решений",
        "short": "Разложить сложный выбор на варианты и возможные последствия.",
        "description": "Сценарии, вероятности и оценки удовлетворённости исходом.",
        "keywords": "выбор решение последствия вероятность варианты",
        "category": "Мышление",
    },
    "dbt_chain": {
        "title": "Цепочный анализ поведения (ДБТ)",
        "short": "Исследовать последовательность событий, реакций и последствий.",
        "description": "Уязвимости, звенья поведения, последствия и точки вмешательства.",
        "keywords": "эмоции поведение дбт реакция событие цепочка",
        "category": "Эмоции",
    },
    "exposure": {
        "title": "Иерархия экспозиции",
        "short": "Составить лестницу ситуаций для постепенной практики.",
        "description": "Прогнозы, уровни тревоги, наблюдения и обучение на опыте.",
        "keywords": "тревога тревожность страх экспозиция ситуации практика",
        "category": "Тревожность",
    },
    "act_matrix": {
        "title": "ACT-матрица",
        "short": "Исследовать действия от дискомфорта и шаги к ценностям.",
        "description": "Карта внутреннего опыта, поведения и выбранных действий.",
        "keywords": "ценности дискомфорт действия мысли осознанность act",
        "category": "Самоосознание",
    },
}


# ---------------------------------------------------------------------
# Состояние и навигация
# ---------------------------------------------------------------------

if "page" not in st.session_state:
    st.session_state.page = "home"
if "selected_technique" not in st.session_state:
    st.session_state.selected_technique = None
if "page_history" not in st.session_state:
    st.session_state.page_history = []
if "home_search" not in st.session_state:
    st.session_state.home_search = ""
if "library_search" not in st.session_state:
    st.session_state.library_search = ""


def clear_searches():
    st.session_state.home_search = ""
    st.session_state.library_search = ""


def navigate(page, technique_id=None):
    current = {
        "page": st.session_state.page,
        "technique": st.session_state.selected_technique,
    }
    target = {"page": page, "technique": technique_id}

    if current != target:
        st.session_state.page_history.append(current)
        st.session_state.page_history = st.session_state.page_history[-30:]

    st.session_state.page = page
    st.session_state.selected_technique = technique_id


def go_home():
    clear_searches()
    navigate("home")


def go_library():
    clear_searches()
    navigate("library")


def go_about():
    clear_searches()
    navigate("about")


def go_back():
    clear_searches()
    if st.session_state.page_history:
        previous = st.session_state.page_history.pop()
        st.session_state.page = previous["page"]
        st.session_state.selected_technique = previous["technique"]
    else:
        st.session_state.page = "home"
        st.session_state.selected_technique = None


def open_technique(technique_id):
    navigate("technique", technique_id)


def search_techniques(query):
    query = " ".join((query or "").casefold().split())
    if not query:
        return list(TECHNIQUES.items())

    words = query.split()
    results = []
    for technique_id, technique in TECHNIQUES.items():
        searchable = " ".join(
            [
                technique["title"],
                technique["short"],
                technique["description"],
                technique["keywords"],
                technique["category"],
            ]
        ).casefold()

        if all(word in searchable for word in words):
            results.append((technique_id, technique))

    return results


# ---------------------------------------------------------------------
# Стили сайта
# ---------------------------------------------------------------------

st.markdown(
    f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Nunito+Sans:wght@400;500;600;700;800&display=swap');

    :root {{ color-scheme: light !important; }}

    html, body, [data-testid="stAppViewContainer"] {{
        color-scheme: light !important;
        background-color: #F3F9FD !important;
        color: #294A65 !important;
        font-family: "Nunito Sans", "Segoe UI", sans-serif !important;
    }}

    [data-testid="stAppViewContainer"] {{
        background-image:
            radial-gradient(ellipse at 10% 5%, rgba(196,228,248,.58), transparent 34%),
            radial-gradient(ellipse at 92% 18%, rgba(219,239,251,.68), transparent 36%);
    }}

    [data-testid="stAppViewContainer"]::before {{
        content: "";
        position: fixed;
        inset: 0;
        z-index: 0;
        pointer-events: none;
        opacity: .56;
        background-image: url("data:image/svg+xml,{neuron_background}");
        background-repeat: repeat;
        background-size: 1000px 800px;
        background-position: left top;
    }}

    [data-testid="stAppViewContainer"] > .main {{
        position: relative;
        z-index: 1;
    }}

    [data-testid="stHeader"] {{ background: transparent !important; }}

    .block-container {{
        max-width: 1160px;
        padding-top: 1rem;
        padding-bottom: 4rem;
    }}

    h1, h2, h3, h4, p, label, button, input, textarea, select {{
        font-family: "Nunito Sans", "Segoe UI", sans-serif !important;
    }}

    h1, h2, h3, h4 {{
        color: #294A65 !important;
        letter-spacing: -0.025em;
    }}

    h1 {{ font-size: 2.5rem !important; font-weight: 800 !important; }}
    h2 {{ font-size: 1.8rem !important; font-weight: 800 !important; }}
    h3 {{ font-size: 1.25rem !important; font-weight: 800 !important; }}

    p, label, [data-testid="stCaptionContainer"], [data-testid="stMarkdownContainer"] {{
        color: #476B85 !important;
    }}

    [data-testid="stVerticalBlockBorderWrapper"] {{
        border: 1px solid #C9DFEF !important;
        border-radius: 18px !important;
        background: rgba(248,252,255,.94) !important;
        box-shadow: 0 8px 22px rgba(62,112,148,.06);
    }}

    [data-testid="stTextInput"] [data-baseweb="input"],
    [data-testid="stTextArea"] [data-baseweb="textarea"],
    [data-testid="stNumberInput"] [data-baseweb="input"],
    [data-testid="stSelectbox"] [data-baseweb="select"] > div,
    [data-baseweb="input"], [data-baseweb="textarea"] {{
        color-scheme: light !important;
        background: #FFFFFF !important;
        border: 1px solid #C9DDEB !important;
        border-radius: 12px !important;
        box-shadow: none !important;
    }}

    [data-testid="stTextInput"] input,
    [data-testid="stTextArea"] textarea,
    [data-testid="stNumberInput"] input,
    [data-testid="stSelectbox"] input,
    [data-baseweb="input"] input,
    [data-baseweb="textarea"] textarea {{
        color: #294A65 !important;
        background: #FFFFFF !important;
        -webkit-text-fill-color: #294A65 !important;
        border: 0 !important;
        box-shadow: none !important;
        outline: none !important;
        caret-color: #315773 !important;
    }}

    input::placeholder, textarea::placeholder {{
        color: #7893A8 !important;
        -webkit-text-fill-color: #7893A8 !important;
        opacity: 1 !important;
    }}

    .stButton > button {{
        min-height: 44px;
        border: 1px solid #AFCFE2 !important;
        border-radius: 13px !important;
        background: #F1F8FD !important;
        color: #315773 !important;
        font-size: .98rem;
        font-weight: 700;
        transition: .18s ease;
    }}

    .stButton > button:hover:not(:disabled) {{
        border-color: #6EA7CB !important;
        background: #E0F0FA !important;
        color: #234D6B !important;
        transform: translateY(-1px);
    }}

    .stButton > button:disabled {{ opacity: .45; }}

    .stButton > button[kind="primary"] {{
        min-height: 50px;
        border: 1px solid #6EA7CB !important;
        border-radius: 14px !important;
        background: linear-gradient(135deg, #D9EEFA, #E5F3FC) !important;
        color: #234D6B !important;
        font-weight: 800;
    }}

    [data-testid="stAlert"] {{
        border: 1px solid #BCD9EB !important;
        border-radius: 14px !important;
        background: #EAF5FC !important;
    }}

    [data-testid="stMetric"] {{
        border: 1px solid #C9DFEF;
        border-radius: 16px;
        background: rgba(248,252,255,.96);
        padding: 14px;
    }}

    hr {{ border-color: #D7E6F0 !important; }}

    .brand-name {{
        color: #234D6B;
        font-size: clamp(1.7rem, 3vw, 2.25rem);
        font-weight: 800;
        line-height: 1.05;
        letter-spacing: -.045em;
        white-space: nowrap;
    }}

    .brand-fallback {{
        width: 42px;
        height: 42px;
        display: flex;
        align-items: center;
        justify-content: center;
        border: 1px solid #BBD9EB;
        border-radius: 12px;
        background: rgba(255,255,255,.65);
    }}

    .hero {{
        position: relative;
        display: flex;
        align-items: center;
        min-height: 340px;
        overflow: hidden;
        padding: 38px 44px;
        margin: 20px 0 22px;
        border: 1px solid #D3E5F2;
        border-radius: 28px;
        background:
            radial-gradient(circle at 79% 42%, rgba(174,222,241,.66) 0 18%, transparent 18.5%),
            linear-gradient(110deg, #F8FCFF 0%, #EAF5FC 100%);
    }}

    .hero-copy {{ position: relative; z-index: 1; max-width: 530px; }}
    .hero-title {{
        margin: 0;
        color: #214D6C;
        font-size: clamp(2.8rem, 6vw, 4.3rem);
        font-weight: 800;
        line-height: 1.04;
        letter-spacing: -.05em;
    }}
    .hero-subtitle {{
        max-width: 490px;
        margin: 12px 0 18px;
        color: #294A65;
        font-size: clamp(1.25rem, 2.5vw, 1.85rem);
        font-weight: 700;
        line-height: 1.3;
    }}
    .hero-description {{
        max-width: 460px;
        color: #476B85;
        font-size: 1.05rem;
        line-height: 1.6;
    }}
    .hero-art {{
        position: absolute;
        top: 50%;
        right: 3%;
        width: min(42%, 430px);
        transform: translateY(-50%);
        opacity: .78;
    }}
    .section-title {{
        margin: 28px 0 12px;
        color: #294A65;
        font-size: 1.7rem;
        font-weight: 800;
    }}
    .category-card {{
        min-height: 125px;
        padding: 17px;
        border: 1px solid #D3E3EF;
        border-radius: 18px;
        background: rgba(248,252,255,.94);
    }}
    .category-title {{ color: #294A65; font-size: 1.04rem; font-weight: 800; }}
    .category-description {{
        margin-top: 7px;
        color: #648198;
        font-size: .9rem;
        line-height: 1.45;
    }}

    @media (max-width: 700px) {{
        .hero {{ min-height: 290px; padding: 25px 22px; }}
        .hero-art {{ right: -10%; width: 58%; opacity: .2; }}
    }}
    </style>
    """,
    unsafe_allow_html=True,
)


# ---------------------------------------------------------------------
# Шапка и карточки техник
# ---------------------------------------------------------------------

def render_header():
    brand_col, home_col, library_col, about_col, back_col = st.columns(
        [2.3, 1, 1.25, 1.1, 1]
    )

    with brand_col:
        logo_col, name_col = st.columns([0.6, 3.4])
        with logo_col:
            if LOGO_PATH.is_file():
                st.image(str(LOGO_PATH), width=42)
            else:
                st.markdown(
                    """
                    <div class="brand-fallback">
                      <svg width="30" height="30" viewBox="0 0 30 30"
                           xmlns="http://www.w3.org/2000/svg">
                        <g fill="none" stroke="#315773" stroke-width="1.5"
                           stroke-linecap="round">
                          <path d="M14.8 5.2c-4-3-8 0-7.5 4-3.8 1.3-3.4 6.1-.3 7.4-2.2 3.2.3 6.5 3.7 5.1 1.3 3 4.5 2.6 5.3.2"/>
                          <path d="M15.2 5.2c4-3 8 0 7.5 4 3.8 1.3 3.4 6.1.3 7.4 2.2 3.2-.3 6.5-3.7 5.1-1.3 3-4.5 2.6-5.3.2"/>
                          <path d="M15 5v17M9 10c2 0 3 1 3 3m-5 3c2-.5 4 .5 4 2m10-8c-2 0-3 1-3 3m5 3c-2-.5-4-.5-4 2"/>
                        </g>
                      </svg>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )
        with name_col:
            st.markdown(
                '<div class="brand-name">ПСИ-БЛОК</div>',
                unsafe_allow_html=True,
            )

    with home_col:
        st.button("Главная", key="header_home", on_click=go_home,
                  use_container_width=True)
    with library_col:
        st.button("Библиотека", key="header_library", on_click=go_library,
                  use_container_width=True)
    with about_col:
        st.button("О проекте", key="header_about", on_click=go_about,
                  use_container_width=True)
    with back_col:
        st.button("Назад", key="header_back", on_click=go_back,
                  disabled=not st.session_state.page_history,
                  use_container_width=True)


def render_technique_cards(items, key_prefix):
    if not items:
        st.info("Ничего не найдено. Попробуйте изменить поисковый запрос.")
        return

    for start in range(0, len(items), 2):
        columns = st.columns(2)
        for column, (technique_id, technique) in zip(
            columns, items[start:start + 2]
        ):
            with column:
                with st.container(border=True):
                    st.markdown(f"### {technique['title']}")
                    st.write(technique["short"])
                    st.caption(
                        f"{technique['category']} · {technique['description']}"
                    )
                    st.button(
                        "Открыть",
                        key=f"{key_prefix}_{technique_id}",
                        on_click=open_technique,
                        args=(technique_id,),
                        use_container_width=True,
                    )


# ---------------------------------------------------------------------
# Главная, библиотека и раздел «О проекте»
# ---------------------------------------------------------------------

def render_home():
    st.markdown(
        """
        <section class="hero">
          <div class="hero-copy">
            <h1 class="hero-title">ПСИ-БЛОК</h1>
            <div class="hero-subtitle">
              Инструменты для глубокой психологической работы
            </div>
            <div class="hero-description">
              Библиотека психологических техник для специалистов и клиентов.
              Выбирайте инструмент и исследуйте важные вопросы в удобном темпе.
            </div>
          </div>
          <div class="hero-art" aria-hidden="true">
            <svg viewBox="0 0 440 300" xmlns="http://www.w3.org/2000/svg">
              <path d="M225 18 C155 8 100 48 89 108 C81 151 99 180 72 204
                       C61 214 48 225 51 234 C55 244 73 246 82 250
                       C89 254 85 265 94 269 C105 275 119 269 126 282
                       C132 294 154 296 176 289 L225 278"
                    fill="none" stroke="#5B87A2" stroke-width="3"
                    stroke-linecap="round" stroke-linejoin="round"/>
              <path d="M222 22 C292 17 347 55 356 113 C362 154 343 185 373 212
                       C390 228 412 233 411 244 C410 254 390 260 382 270
                       C374 280 362 291 341 289 L226 278"
                    fill="none" stroke="#5B87A2" stroke-width="3"
                    stroke-linecap="round" stroke-linejoin="round"/>
              <path d="M223 54 C194 33 163 47 162 72 C133 75 132 108 154 119
                       C139 141 159 162 181 156 C188 179 215 178 226 160
                       C240 180 267 173 271 151 C297 151 305 124 287 108
                       C300 84 281 60 258 64 C251 47 236 46 223 54Z"
                    fill="none" stroke="#5B87A2" stroke-width="2.5"
                    stroke-linecap="round" stroke-linejoin="round"/>
              <path d="M222 55 L222 159 M162 73 C183 83 187 101 181 117
                       M258 64 C242 79 242 96 254 109
                       M154 119 C174 117 187 127 181 156
                       M287 108 C264 111 253 127 271 151
                       M188 78 C204 88 206 105 196 119
                       M239 78 C222 90 223 108 239 118
                       M201 140 C212 130 225 131 234 143"
                    fill="none" stroke="#5B87A2" stroke-width="2"
                    stroke-linecap="round"/>
              <ellipse cx="224" cy="150" rx="190" ry="76"
                       transform="rotate(-12 224 150)"
                       fill="none" stroke="#76A6C0" stroke-width="2"/>
            </svg>
          </div>
        </section>
        """,
        unsafe_allow_html=True,
    )

    action_col, about_col, _ = st.columns([1.7, 1.2, 3.5])
    with action_col:
        st.button(
            "Перейти в библиотеку", key="home_library_button",
            type="primary", on_click=go_library, use_container_width=True,
        )
    with about_col:
        st.button(
            "Узнать больше", key="home_about_button",
            on_click=go_about, use_container_width=True,
        )

    st.markdown(
        '<div class="section-title">Найти технику</div>',
        unsafe_allow_html=True,
    )
    query = st.text_input(
        "Поиск по техникам", key="home_search",
        placeholder="Например: тревожность, самооценка, выбор...",
        label_visibility="collapsed",
    )

    if query.strip():
        st.markdown("#### Результаты поиска")
        render_technique_cards(search_techniques(query), "home_search_result")
        return

    st.markdown(
        '<div class="section-title">Исследуйте библиотеку</div>',
        unsafe_allow_html=True,
    )
    categories = [
        ("Эмоции", "Работа с эмоциональными состояниями"),
        ("Коммуникация", "Взаимодействие и отношения"),
        ("Самооценка", "Образ себя и личные границы"),
        ("Мышление", "Убеждения и автоматические мысли"),
    ]
    category_columns = st.columns(4)
    for column, (title, description) in zip(category_columns, categories):
        with column:
            st.markdown(
                f"""
                <div class="category-card">
                    <div class="category-title">{title}</div>
                    <div class="category-description">{description}</div>
                </div>
                """,
                unsafe_allow_html=True,
            )

    st.markdown(
        '<div class="section-title">Популярные инструменты</div>',
        unsafe_allow_html=True,
    )
    render_technique_cards(list(TECHNIQUES.items())[:2], "home_featured")

    st.markdown(
        '<div class="section-title">ПСИ-БЛОК — ваш помощник</div>',
        unsafe_allow_html=True,
    )
    st.info(
        "Инструменты помогают структурировать совместную работу и обсуждение. "
        "Они не заменяют профессиональную психологическую помощь."
    )


def render_library():
    st.title("Библиотека техник")
    st.write("Ищите по названию, теме или описанию техники.")
    query = st.text_input(
        "Поиск по библиотеке", key="library_search",
        placeholder="Например: тревожность, поведение, выбор...",
        label_visibility="collapsed",
    )
    render_technique_cards(search_techniques(query), "library_result")


def render_about():
    st.title("О проекте")
    st.markdown(
        """
        **ПСИ-БЛОК** — библиотека интерактивных инструментов
        для психологических консультаций. Она помогает специалисту
        и клиенту совместно структурировать обсуждение и фиксировать идеи.
        """
    )
    st.divider()
    st.subheader("Команда разработчиков")

    developers = [
        {
            "name": "Артём Черемкин",
            "role": "Разработчик сайта, практикующий психолог",
            "photo": "developer1.jpg",
        },
        {
            "name": "Анна Пыжьянова",
            "role": "Практикующий психолог",
            "photo": "developer2.jpg",
        },
        {
            "name": "Ферузахон Сайдазимова",
            "role": "Практикующий психолог",
            "photo": "developer3.jpg",
        },
    ]

    columns = st.columns(3)
    app_dir = Path(__file__).resolve().parent
    for column, person in zip(columns, developers):
        with column:
            with st.container(border=True):
                photo_path = app_dir / person["photo"]
                if photo_path.is_file():
                    st.image(str(photo_path), use_container_width=True)
                else:
                    st.markdown(
                        """
                        <div style="height:220px;display:flex;align-items:center;
                        justify-content:center;border-radius:14px;
                        background:linear-gradient(135deg,#DDEFFA,#F2F8FC);
                        color:#5F86A0;">Фото разработчика</div>
                        """,
                        unsafe_allow_html=True,
                    )
                st.markdown(f"**{html.escape(person['name'])}**")
                st.caption(person["role"])


# ---------------------------------------------------------------------
# Общие функции построения и просмотра SVG
# ---------------------------------------------------------------------

SVG_COLORS = {
    "ink": "#234D6B",
    "text": "#476B85",
    "line": "#80AFCB",
    "border": "#B9D9EB",
    "panel": "#F7FBFF",
    "pale": "#E7F3FB",
    "white": "#FFFFFF",
    "accent": "#D9EEFA",
}


def svg_text(x, y, value, size=14, weight=400, color=None,
             max_chars=48, max_lines=3):
    """Добавляет в SVG безопасный, ограниченно переносимый текст."""
    text = " ".join(str(value or "—").split())
    words = text.split()
    lines = []
    line = ""

    for word in words:
        candidate = f"{line} {word}".strip()
        if len(candidate) > max_chars and line:
            lines.append(line)
            line = word
        else:
            line = candidate
    if line:
        lines.append(line)

    if len(lines) > max_lines:
        lines = lines[:max_lines]
        lines[-1] = lines[-1][:max_chars - 1] + "…"

    color = color or SVG_COLORS["text"]
    tspans = []
    for index, item in enumerate(lines):
        dy = 0 if index == 0 else 18
        tspans.append(
            f'<tspan x="{x}" dy="{dy}">{html.escape(item)}</tspan>'
        )

    return (
        f'<text x="{x}" y="{y}" font-family="Arial,sans-serif" '
        f'font-size="{size}" font-weight="{weight}" fill="{color}">'
        f'{"".join(tspans)}</text>'
    )


def make_svg(width, height, title, body):
    return f"""<svg xmlns="http://www.w3.org/2000/svg"
        width="{width}" height="{height}" viewBox="0 0 {width} {height}">
        <rect width="100%" height="100%" fill="{SVG_COLORS['panel']}"/>
        {svg_text(32, 42, title, size=24, weight=700,
                  color=SVG_COLORS['ink'], max_chars=80, max_lines=1)}
        <g id="scene">{body}</g>
    </svg>"""


def render_visualization(svg, filename, caption):
    """Панорамирование, масштабирование и скачивание схемы."""
    st.subheader("Визуализация")
    st.caption(caption)

    html_doc = """
    <!doctype html>
    <html>
    <head>
      <meta charset="utf-8">
      <style>
        * { box-sizing: border-box; }
        body { margin: 0; font: 14px Arial, sans-serif; color: #234D6B; }
        .toolbar {
          display:flex; gap:8px; align-items:center; flex-wrap:wrap;
          padding:8px; background:#F3F9FD;
          border:1px solid #D4E6F2; border-radius:12px 12px 0 0;
        }
        button {
          border:1px solid #AFCFE2; border-radius:8px;
          background:white; color:#315773; padding:7px 11px;
          cursor:pointer; font-weight:600;
        }
        #zoom-label { min-width:48px; text-align:center; }
        .viewport {
          height:520px; overflow:auto; border:1px solid #D4E6F2;
          border-top:0; border-radius:0 0 12px 12px;
          background:white; touch-action:none;
        }
        svg { display:block; width:100%; height:100%; min-width:720px; }
        svg #scene { cursor:grab; }
        svg #scene:active { cursor:grabbing; }
        @media (max-width:700px) { .viewport { height:430px; } }
      </style>
    </head>
    <body>
      <div class="toolbar">
        <button id="minus" type="button" aria-label="Уменьшить">−</button>
        <button id="plus" type="button" aria-label="Увеличить">+</button>
        <button id="reset" type="button">Сбросить вид</button>
        <span id="zoom-label">100%</span>
        <button id="save-svg" type="button">Скачать SVG</button>
        <button id="save-png" type="button">Скачать PNG</button>
      </div>
      <div class="viewport" id="viewport">__SVG__</div>
      <script>
        (() => {
          const svg = document.querySelector('#viewport svg');
          const scene = svg && svg.querySelector('#scene');
          const label = document.getElementById('zoom-label');
          if (!svg || !scene) return;

          let scale = 1, tx = 0, ty = 0, drag = null;
          const update = () => {
            scene.setAttribute('transform',
              `translate(${tx} ${ty}) scale(${scale})`);
            label.textContent = `${Math.round(scale * 100)}%`;
          };

          document.getElementById('plus').onclick = () => {
            scale = Math.min(4, scale * 1.2); update();
          };
          document.getElementById('minus').onclick = () => {
            scale = Math.max(.4, scale / 1.2); update();
          };
          document.getElementById('reset').onclick = () => {
            scale = 1; tx = 0; ty = 0; update();
          };
          svg.addEventListener('wheel', (event) => {
            event.preventDefault();
            scale = Math.max(.4, Math.min(4,
              scale * (event.deltaY < 0 ? 1.1 : .9)));
            update();
          }, {passive:false});

          svg.addEventListener('pointerdown', (event) => {
            drag = {x:event.clientX - tx, y:event.clientY - ty};
            svg.setPointerCapture(event.pointerId);
          });
          svg.addEventListener('pointermove', (event) => {
            if (!drag) return;
            tx = event.clientX - drag.x;
            ty = event.clientY - drag.y;
            update();
          });
          svg.addEventListener('pointerup', () => drag = null);
          svg.addEventListener('pointercancel', () => drag = null);

          const serialized = () => {
            const clone = svg.cloneNode(true);
            clone.setAttribute('xmlns', 'http://www.w3.org/2000/svg');
            return new XMLSerializer().serializeToString(clone);
          };
          const save = (blob, name) => {
            const link = document.createElement('a');
            link.href = URL.createObjectURL(blob);
            link.download = name;
            link.click();
            setTimeout(() => URL.revokeObjectURL(link.href), 1000);
          };

          document.getElementById('save-svg').onclick = () => {
            save(new Blob([serialized()],
              {type:'image/svg+xml;charset=utf-8'}), __SVG_NAME__);
          };
          document.getElementById('save-png').onclick = () => {
            const blob = new Blob([serialized()],
              {type:'image/svg+xml;charset=utf-8'});
            const url = URL.createObjectURL(blob);
            const image = new Image();
            image.onload = () => {
              const viewBox = svg.viewBox.baseVal;
              const canvas = document.createElement('canvas');
              canvas.width = viewBox.width * 2;
              canvas.height = viewBox.height * 2;
              const context = canvas.getContext('2d');
              context.fillStyle = '#F7FBFF';
              context.fillRect(0, 0, canvas.width, canvas.height);
              context.drawImage(image, 0, 0, canvas.width, canvas.height);
              canvas.toBlob((png) => {
                if (png) save(png, __PNG_NAME__);
                URL.revokeObjectURL(url);
              }, 'image/png');
            };
            image.onerror = () => URL.revokeObjectURL(url);
            image.src = url;
          };
        })();
      </script>
    </body>
    </html>
    """
    html_doc = (
        html_doc.replace("__SVG__", svg)
        .replace("__SVG_NAME__", json.dumps(filename))
        .replace("__PNG_NAME__", json.dumps(filename.rsplit(".", 1)[0] + ".png"))
    )
    components.html(html_doc, height=590, scrolling=False)


def store_result(key, value):
    st.session_state[key] = value


# ---------------------------------------------------------------------
# Дерево решений
# ---------------------------------------------------------------------

def render_decision_tree():
    st.title("Дерево решений")
    st.write(
        "Для каждого варианта опишите несколько возможных сценариев, "
        "вероятность каждого и удовлетворённость исходом."
    )
    st.caption(
        "Вероятности сценариев внутри одного варианта должны составлять 100%. "
        "Оценка удовлетворённости — субъективная шкала от −5 до +5."
    )

    question = st.text_input(
        "Какое решение нужно принять?",
        key="decision_question",
        placeholder="Например: Стоит ли менять работу?",
    )
    option_count = int(st.number_input(
        "Количество вариантов",
        min_value=2, max_value=5, value=2, step=1,
        key="decision_option_count",
    ))

    options = []
    for option_index in range(option_count):
        with st.container(border=True):
            st.markdown(f"### Вариант {option_index + 1}")
            name = st.text_input(
                "Название варианта",
                key=f"decision_name_{option_index}",
                placeholder=f"Вариант {option_index + 1}",
            )
            scenario_count = int(st.number_input(
                "Количество сценариев",
                min_value=2, max_value=6, value=2, step=1,
                key=f"decision_scenario_count_{option_index}",
            ))

            scenarios = []
            for scenario_index in range(scenario_count):
                with st.expander(
                    f"Сценарий {scenario_index + 1}",
                    expanded=(scenario_index == 0),
                ):
                    title = st.text_input(
                        "Название сценария",
                        key=f"decision_scenario_title_{option_index}_{scenario_index}",
                        placeholder="Например: адаптация проходит успешно",
                    )
                    outcome = st.text_area(
                        "Что может произойти?",
                        key=f"decision_scenario_outcome_{option_index}_{scenario_index}",
                    )
                    probability = st.slider(
                        "Вероятность, %",
                        min_value=0, max_value=100,
                        value=100 // scenario_count,
                        key=f"decision_scenario_probability_{option_index}_{scenario_index}",
                    )
                    satisfaction = st.slider(
                        "Удовлетворённость исходом",
                        min_value=-5.0, max_value=5.0,
                        value=0.0, step=0.5,
                        key=f"decision_scenario_satisfaction_{option_index}_{scenario_index}",
                    )
                    scenarios.append({
                        "title": title,
                        "outcome": outcome,
                        "probability": probability,
                        "satisfaction": satisfaction,
                    })

            options.append({"name": name, "scenarios": scenarios})

    if st.button(
        "Сформировать дерево и сравнить",
        key="decision_calculate",
        type="primary",
        use_container_width=True,
    ):
        errors = []
        if not question.strip():
            errors.append("Сформулируйте решение.")
        if any(not option["name"].strip() for option in options):
            errors.append("Укажите название каждого варианта.")

        for option_index, option in enumerate(options, start=1):
            total = sum(
                scenario["probability"] for scenario in option["scenarios"]
            )
            if any(not scenario["title"].strip()
                   for scenario in option["scenarios"]):
                errors.append(
                    f"Заполните названия сценариев варианта {option_index}."
                )
            if total != 100:
                errors.append(
                    f"Вероятности сценариев варианта {option_index} "
                    f"составляют {total}%, а должны составлять 100%."
                )

        if errors:
            for error in errors:
                st.warning(error)
            st.session_state.pop("result_decision_tree", None)
        else:
            prepared = []
            for option in options:
                expected = sum(
                    item["probability"] * item["satisfaction"]
                    for item in option["scenarios"]
                ) / 100
                prepared.append({**option, "expected": expected})
            store_result("result_decision_tree", {
                "question": question,
                "options": prepared,
            })

    result = st.session_state.get("result_decision_tree")
    if not result:
        return

    options = result["options"]
    best_option = max(options, key=lambda item: item["expected"])
    st.subheader("Ожидаемая удовлетворённость — ориентир для обсуждения")
    columns = st.columns(len(options))
    for column, option in zip(columns, options):
        with column:
            st.metric(option["name"], f'{option["expected"]:.2f} / 5')
            if option is best_option:
                st.caption("Наибольшая оценка по введённым данным")

    column_width = 390
    chart_width = 50 + len(options) * column_width
    scenario_height = 118
    chart_height = 220 + max(
        len(option["scenarios"]) for option in options
    ) * scenario_height

    body = svg_text(
        32, 78, result["question"], size=15,
        max_chars=120, max_lines=2,
    )

    root_width = 420
    root_x = (chart_width - root_width) // 2
    body += (
        f'<rect x="{root_x}" y="96" width="{root_width}" height="62" '
        f'rx="14" fill="{SVG_COLORS["accent"]}" '
        f'stroke="{SVG_COLORS["line"]}"/>'
    )
    body += svg_text(
        root_x + 16, 122, "Решение", size=16, weight=700,
        color=SVG_COLORS["ink"], max_lines=1,
    )
    body += svg_text(
        root_x + 16, 145, result["question"], size=12,
        max_chars=48, max_lines=1,
    )

    for option_index, option in enumerate(options):
        x = 25 + option_index * column_width
        option_y = 190
        box_width = column_width - 30

        body += (
            f'<line x1="{root_x + root_width / 2}" y1="158" '
            f'x2="{x + box_width / 2}" y2="{option_y}" '
            f'stroke="{SVG_COLORS["line"]}" stroke-width="2"/>'
        )
        body += (
            f'<rect x="{x}" y="{option_y}" width="{box_width}" height="64" '
            f'rx="13" fill="{SVG_COLORS["pale"]}" '
            f'stroke="{SVG_COLORS["line"]}"/>'
        )
        body += svg_text(
            x + 13, option_y + 25, option["name"], size=15, weight=700,
            color=SVG_COLORS["ink"], max_chars=38, max_lines=1,
        )
        body += svg_text(
            x + 13, option_y + 48,
            f'Ожидаемая удовлетворённость: {option["expected"]:.2f}',
            size=12, max_chars=43, max_lines=1,
        )

        for scenario_index, scenario in enumerate(option["scenarios"]):
            y = 274 + scenario_index * scenario_height
            body += (
                f'<line x1="{x + 25}" y1="{option_y + 64}" '
                f'x2="{x + 25}" y2="{y}" '
                f'stroke="{SVG_COLORS["line"]}" stroke-width="2"/>'
            )
            body += (
                f'<rect x="{x + 38}" y="{y}" width="{box_width - 38}" '
                f'height="100" rx="11" fill="{SVG_COLORS["white"]}" '
                f'stroke="{SVG_COLORS["border"]}"/>'
            )
            body += svg_text(
                x + 50, y + 22, scenario["title"], size=13, weight=700,
                color=SVG_COLORS["ink"], max_chars=34, max_lines=1,
            )
            body += svg_text(
                x + 50, y + 44,
                f'Вероятность {scenario["probability"]}% · '
                f'удовлетворённость {scenario["satisfaction"]:+.1f}',
                size=11, max_chars=43, max_lines=1,
            )
            body += svg_text(
                x + 50, y + 66, scenario["outcome"],
                size=11, max_chars=39, max_lines=2,
            )

    svg = make_svg(chart_width, chart_height, "Дерево решений", body)
    render_visualization(
        svg,
        "decision_tree.svg",
        "Сценарии показаны внутри вариантов; ожидаемая оценка рассчитана "
        "как сумма оценок, взвешенных по вероятностям.",
    )
    st.info(
        "Расчёт не принимает решение за вас: используйте его для обсуждения "
        "предпочтений, ценностей и неопределённости."
    )


# ---------------------------------------------------------------------
# Цепочный анализ поведения ДБТ
# ---------------------------------------------------------------------

def render_chain():
    st.title("Цепочный анализ поведения (ДБТ)")
    st.write(
        "Восстановите провоцирующее событие, последовательность звеньев, "
        "последствия и возможные места для навыков или поддержки."
    )
    st.info(
        "Можно пропустить поле или остановиться в любой момент. "
        "Если есть непосредственная опасность для вас или другого человека, "
        "обратитесь за срочной помощью к местным службам или специалисту."
    )

    vulnerability = st.text_area(
        "Факторы уязвимости",
        key="chain_vulnerability",
        placeholder="Например: недосып, стресс, боль, конфликт",
    )
    trigger = st.text_area(
        "Провоцирующее событие",
        key="chain_trigger",
        placeholder="Последнее событие, запустившее последовательность",
    )
    target = st.text_area(
        "Проблемное поведение, которое анализируем",
        key="chain_target",
        placeholder="Опишите конкретно, что произошло, без оценочных ярлыков",
    )

    link_count = int(st.number_input(
        "Количество звеньев цепочки",
        min_value=1, max_value=8, value=4, step=1,
        key="chain_link_count",
    ))

    links = []
    for index in range(link_count):
        with st.expander(
            f"Звено {index + 1}: что произошло дальше?",
            expanded=(index < 2),
        ):
            left, right = st.columns(2)
            with left:
                thought = st.text_area(
                    "Мысль / интерпретация",
                    key=f"chain_thought_{index}",
                )
                emotion = st.text_input(
                    "Эмоция", key=f"chain_emotion_{index}"
                )
                urge = st.text_input(
                    "Побуждение / импульс", key=f"chain_urge_{index}"
                )
            with right:
                body = st.text_input(
                    "Телесные ощущения", key=f"chain_body_{index}"
                )
                action = st.text_area(
                    "Действие / следующий шаг",
                    key=f"chain_action_{index}",
                )
                intervention = st.text_area(
                    "Возможная точка вмешательства",
                    key=f"chain_intervention_{index}",
                )
            skill = st.text_input(
                "Навык или поддержка для этой точки",
                key=f"chain_skill_{index}",
                placeholder="Например: пауза, заземление, обратиться за поддержкой",
            )
            links.append({
                "thought": thought,
                "emotion": emotion,
                "urge": urge,
                "body": body,
                "action": action,
                "intervention": intervention,
                "skill": skill,
            })

    left, right = st.columns(2)
    with left:
        immediate = st.text_area(
            "Последствия сразу после (для себя и других)",
            key="chain_immediate",
        )
        immediate_reinforcement = st.text_area(
            "Что могло подкрепить поведение сразу?",
            key="chain_immediate_reinforcement",
        )
    with right:
        later = st.text_area(
            "Отсроченные последствия",
            key="chain_later",
        )
        later_reinforcement = st.text_area(
            "Что могло поддержать повторение поведения?",
            key="chain_later_reinforcement",
        )

    prevention = st.text_area(
        "План профилактики на будущее",
        key="chain_prevention",
        placeholder="Какие уязвимости можно уменьшить? Что подготовить заранее?",
    )
    repair = st.text_area(
        "Восстановление / исправление последствий, если необходимо",
        key="chain_repair",
    )

    if st.button(
        "Сформировать карту цепочки",
        key="chain_build",
        type="primary",
        use_container_width=True,
    ):
        if not target.strip():
            st.warning("Опишите поведение, которое анализируете.")
            st.session_state.pop("result_dbt_chain", None)
        else:
            store_result("result_dbt_chain", {
                "vulnerability": vulnerability,
                "trigger": trigger,
                "target": target,
                "links": links,
                "immediate": immediate,
                "immediate_reinforcement": immediate_reinforcement,
                "later": later,
                "later_reinforcement": later_reinforcement,
                "prevention": prevention,
                "repair": repair,
            })

    result = st.session_state.get("result_dbt_chain")
    if not result:
        return

    st.subheader("Сводка цепочки и анализа решений")
    for title, value in [
        ("Факторы уязвимости", result["vulnerability"]),
        ("Провоцирующее событие", result["trigger"]),
        ("Проблемное поведение", result["target"]),
        ("Последствия сразу", result["immediate"]),
        ("Что подкрепляло поведение", result["immediate_reinforcement"]),
        ("Отсроченные последствия", result["later"]),
        ("План профилактики", result["prevention"]),
        ("Восстановление", result["repair"]),
    ]:
        st.markdown(f"**{title}:** {value or '—'}")

    for index, link in enumerate(result["links"], start=1):
        with st.expander(f"Содержание звена {index}", expanded=False):
            st.write(
                f'Мысль: {link["thought"] or "—"} · '
                f'Эмоция: {link["emotion"] or "—"} · '
                f'Импульс: {link["urge"] or "—"} · '
                f'Ощущения: {link["body"] or "—"}'
            )
            st.write(f'Действие: {link["action"] or "—"}')
            st.write(
                f'Точка вмешательства: {link["intervention"] or "—"} · '
                f'Навык/поддержка: {link["skill"] or "—"}'
            )

    width = 1180
    row_height = 142
    height = 265 + len(result["links"]) * row_height + 190
    body = ""

    for row_index, (label, value) in enumerate([
        ("Факторы уязвимости", result["vulnerability"]),
        ("Провоцирующее событие", result["trigger"]),
        ("Проблемное поведение", result["target"]),
    ]):
        y = 75 + row_index * 58
        body += (
            f'<rect x="40" y="{y}" width="1100" height="46" rx="10" '
            f'fill="{SVG_COLORS["pale"]}" stroke="{SVG_COLORS["line"]}"/>'
        )
        body += svg_text(
            54, y + 19, label, size=12, weight=700,
            color=SVG_COLORS["ink"], max_chars=29, max_lines=1,
        )
        body += svg_text(
            285, y + 19, value, size=12, max_chars=108, max_lines=1,
        )

    for index, link in enumerate(result["links"]):
        y = 258 + index * row_height
        body += (
            f'<rect x="40" y="{y}" width="1100" height="118" rx="13" '
            f'fill="{SVG_COLORS["white"]}" stroke="{SVG_COLORS["border"]}"/>'
        )
        body += svg_text(
            56, y + 25, f"Звено {index + 1}", size=14, weight=700,
            color=SVG_COLORS["ink"], max_lines=1,
        )
        body += svg_text(
            200, y + 24,
            f'Мысль: {link["thought"]} · Эмоция: {link["emotion"]} · '
            f'Импульс: {link["urge"]}',
            size=11, max_chars=112, max_lines=1,
        )
        body += svg_text(
            200, y + 54,
            f'Ощущения: {link["body"]} · Действие: {link["action"]}',
            size=11, max_chars=112, max_lines=1,
        )
        body += svg_text(
            200, y + 84,
            f'Вмешательство: {link["intervention"]} · Навык: {link["skill"]}',
            size=11, max_chars=112, max_lines=1,
        )
        if index < len(result["links"]) - 1:
            body += (
                f'<line x1="590" y1="{y + 118}" x2="590" '
                f'y2="{y + row_height}" stroke="{SVG_COLORS["line"]}" '
                f'stroke-width="2"/>'
            )

    footer_y = 258 + len(result["links"]) * row_height
    for index, (label, value) in enumerate([
        ("Последствия сразу", result["immediate"]),
        ("Отсроченные последствия", result["later"]),
        ("Профилактика / восстановление",
         f'{result["prevention"]} · {result["repair"]}'),
    ]):
        y = footer_y + index * 52
        body += (
            f'<rect x="40" y="{y}" width="1100" height="42" rx="9" '
            f'fill="{SVG_COLORS["accent"]}" stroke="{SVG_COLORS["line"]}"/>'
        )
        body += svg_text(
            54, y + 18, label, size=11, weight=700,
            color=SVG_COLORS["ink"], max_chars=32, max_lines=1,
        )
        body += svg_text(
            285, y + 18, value, size=11, max_chars=104, max_lines=1,
        )

    svg = make_svg(width, height, "ДБТ · анализ цепочки и решений", body)
    render_visualization(
        svg,
        "dbt_chain.svg",
        "Карта показывает уязвимости, запускающее событие, звенья, "
        "последствия и возможные места для навыков или поддержки.",
    )


# ---------------------------------------------------------------------
# Иерархия экспозиции
# ---------------------------------------------------------------------

def render_exposure():
    st.title("Иерархия экспозиции")
    st.write(
        "Составьте добровольную лестницу практики. До практики зафиксируйте "
        "прогноз, а после — наблюдаемый исход и то, что удалось узнать."
    )
    st.info(
        "Практикуйте только добровольно и в безопасных ситуациях; "
        "не используйте экспозицию для реальной опасности. "
        "План можно обсудить со специалистом. Не обязательно ждать, "
        "пока тревога полностью исчезнет: важно также проверить прогнозы "
        "и получить новый опыт."
    )

    goal = st.text_area("Цель / ситуация для работы", key="exposure_goal")
    step_count = int(st.number_input(
        "Количество ступеней",
        min_value=1, max_value=10, value=3, step=1,
        key="exposure_count",
    ))

    steps = []
    for index in range(step_count):
        with st.expander(f"Ступень {index + 1}", expanded=(index < 2)):
            situation = st.text_input(
                "Ситуация / упражнение",
                key=f"exposure_situation_{index}",
            )
            left, right = st.columns(2)
            with left:
                expected = st.slider(
                    "Ожидаемая тревога (0–10)",
                    min_value=0, max_value=10, value=3,
                    key=f"exposure_distress_{index}",
                )
                prediction = st.text_area(
                    "Прогноз или опасение",
                    key=f"exposure_prediction_{index}",
                )
                plan = st.text_area(
                    "Посильный план практики",
                    key=f"exposure_plan_{index}",
                )
            with right:
                practiced = st.checkbox(
                    "Практика выполнена",
                    key=f"exposure_practiced_{index}",
                )
                start = st.slider(
                    "Тревога в начале (0–10)",
                    min_value=0, max_value=10, value=0,
                    key=f"exposure_start_{index}",
                )
                peak = st.slider(
                    "Максимальная тревога (0–10)",
                    min_value=0, max_value=10, value=0,
                    key=f"exposure_peak_{index}",
                )
                after = st.slider(
                    "Тревога после практики (0–10)",
                    min_value=0, max_value=10, value=0,
                    key=f"exposure_after_{index}",
                )
                outcome = st.text_area(
                    "Что произошло на самом деле?",
                    key=f"exposure_outcome_{index}",
                )
                learning = st.text_area(
                    "Что вы узнали / что попробовать дальше?",
                    key=f"exposure_learning_{index}",
                )

            steps.append({
                "situation": situation,
                "expected": expected,
                "prediction": prediction,
                "plan": plan,
                "practiced": practiced,
                "start": start,
                "peak": peak,
                "after": after,
                "outcome": outcome,
                "learning": learning,
            })

    if st.button(
        "Сформировать лестницу",
        key="exposure_build",
        type="primary",
        use_container_width=True,
    ):
        completed = [
            step for step in steps if step["situation"].strip()
        ]
        if not completed:
            st.warning("Добавьте описание хотя бы одной ступени.")
            st.session_state.pop("result_exposure", None)
        else:
            completed.sort(key=lambda step: step["expected"])
            store_result("result_exposure", {
                "goal": goal,
                "steps": completed,
            })

    result = st.session_state.get("result_exposure")
    if not result:
        return

    st.subheader("Лестница: от меньшей ожидаемой тревоги к большей")
    for index, step in enumerate(result["steps"], start=1):
        with st.container(border=True):
            st.markdown(
                f'**{index}. {step["situation"]}** · '
                f'ожидаемая тревога {step["expected"]}/10'
            )
            if step["prediction"]:
                st.write(f'Прогноз: {step["prediction"]}')
            if step["plan"]:
                st.write(f'План: {step["plan"]}')
            if step["practiced"]:
                st.write(
                    f'Практика: начало {step["start"]}/10, '
                    f'максимум {step["peak"]}/10, '
                    f'после {step["after"]}/10.'
                )
                if step["outcome"]:
                    st.write(f'Наблюдаемый исход: {step["outcome"]}')
                if step["learning"]:
                    st.write(f'Вывод / следующий шаг: {step["learning"]}')

    width = 1300
    row_height = 105
    height = 130 + len(result["steps"]) * row_height
    body = svg_text(
        35, 78, f'Цель: {result["goal"]}', size=14,
        max_chars=115, max_lines=1,
    )

    for index, step in enumerate(result["steps"]):
        x, y = 45, 98 + index * row_height
        bar_width = 230 + step["expected"] * 48
        body += (
            f'<rect x="{x}" y="{y}" width="{bar_width}" height="70" '
            f'rx="12" fill="{SVG_COLORS["accent"]}" '
            f'stroke="{SVG_COLORS["line"]}"/>'
        )
        body += svg_text(
            x + 12, y + 23, f'{index + 1}. {step["situation"]}',
            size=12, weight=700, color=SVG_COLORS["ink"],
            max_chars=48, max_lines=1,
        )
        body += svg_text(
            x + 12, y + 48,
            f'Ожидаемая тревога: {step["expected"]}/10',
            size=11, max_chars=42, max_lines=1,
        )

        if step["practiced"]:
            body += svg_text(
                720, y + 22,
                f'Фактические оценки · начало {step["start"]} / '
                f'пик {step["peak"]} / после {step["after"]}',
                size=11, max_chars=76, max_lines=1,
            )
            body += svg_text(
                720, y + 48,
                f'Наблюдение: {step["outcome"] or step["learning"] or "не записано"}',
                size=11, max_chars=76, max_lines=1,
            )
        else:
            body += svg_text(
                720, y + 34, "Практика пока не отмечена",
                size=11, max_chars=65, max_lines=1,
            )

        if index < len(result["steps"]) - 1:
            body += (
                f'<line x1="{x + 24}" y1="{y + 70}" '
                f'x2="{x + 24}" y2="{y + row_height}" '
                f'stroke="{SVG_COLORS["line"]}" stroke-width="2"/>'
            )

    svg = make_svg(width, height, "Иерархия экспозиции", body)
    render_visualization(
        svg,
        "exposure_hierarchy.svg",
        "Ступени упорядочены по субъективной ожидаемой тревоге. "
        "После практики схема показывает фактические оценки и наблюдения.",
    )


# ---------------------------------------------------------------------
# ACT-матрица
# ---------------------------------------------------------------------

def render_act_matrix():
    st.title("ACT-матрица")
    st.write(
        "Заметьте внутренний опыт, действия от дискомфорта и действия, "
        "которые приближают к важному."
    )
    st.info(
        "Матрица — способ исследовать выбор, а не оценка поведения. "
        "Записывайте несколько пунктов через новую строку."
    )

    situation = st.text_area(
        "Ситуация / контекст",
        key="act_situation",
    )
    values = st.text_area(
        "Люди и ценности, которые важны",
        key="act_values",
        placeholder="Например: близкие отношения, забота, обучение",
    )
    external = st.text_area(
        "Что вы замечаете снаружи пятью чувствами?",
        key="act_external",
        placeholder="Что можно увидеть, услышать или заметить в ситуации?",
    )

    left, right = st.columns(2)
    with left:
        away = st.text_area(
            "Действия от дискомфорта: что вы делаете, "
            "чтобы уйти от неприятного?",
            key="act_away",
        )
        inner = st.text_area(
            "Внутренний опыт, от которого хочется уйти",
            key="act_inner",
            placeholder="Мысли, эмоции, воспоминания, импульсы, ощущения",
        )
    with right:
        toward = st.text_area(
            "Действия к важному: что помогает приближаться к ценностям?",
            key="act_toward",
        )
        toward_inner = st.text_area(
            "Что может возникать внутри, когда вы движетесь к важному?",
            key="act_toward_inner",
        )

    chosen_step = st.text_area(
        "Один небольшой выбранный шаг к важному",
        key="act_step",
    )

    if st.button(
        "Сформировать ACT-матрицу",
        key="act_build",
        type="primary",
        use_container_width=True,
    ):
        if not situation.strip():
            st.warning("Добавьте ситуацию, которую исследуете.")
            st.session_state.pop("result_act_matrix", None)
        else:
            store_result("result_act_matrix", {
                "situation": situation,
                "values": values,
                "external": external,
                "away": away,
                "inner": inner,
                "toward": toward,
                "toward_inner": toward_inner,
                "step": chosen_step,
            })

    result = st.session_state.get("result_act_matrix")
    if not result:
        return

    st.subheader("Сводка")
    st.write(f'**Ситуация:** {result["situation"]}')
    st.write(f'**Что важно:** {result["values"] or "—"}')
    st.write(f'**Небольшой шаг:** {result["step"] or "—"}')

    width, height = 1120, 760
    left_x, right_x = 55, 575
    top_y, bottom_y = 125, 395
    box_width, box_height = 490, 245

    quadrants = [
        (left_x, top_y, "ДЕЙСТВИЯ ОТ ДИСКОМФОРТА", result["away"]),
        (right_x, top_y, "ДЕЙСТВИЯ К ВАЖНОМУ", result["toward"]),
        (left_x, bottom_y, "ВНУТРЕННИЙ ОПЫТ", result["inner"]),
        (right_x, bottom_y, "ВНУТРЕННИЙ ОПЫТ ПРИ ДВИЖЕНИИ К ВАЖНОМУ",
         result["toward_inner"]),
    ]

    body = svg_text(
        55, 82, f'Контекст: {result["situation"]}',
        size=13, max_chars=112, max_lines=1,
    )

    for x, y, label, value in quadrants:
        body += (
            f'<rect x="{x}" y="{y}" width="{box_width}" '
            f'height="{box_height}" rx="15" '
            f'fill="{SVG_COLORS["white"]}" '
            f'stroke="{SVG_COLORS["line"]}" stroke-width="2"/>'
        )
        body += svg_text(
            x + 16, y + 27, label,
            size=12, weight=700, color=SVG_COLORS["ink"],
            max_chars=56, max_lines=1,
        )
        items = [item.strip() for item in (value or "").splitlines()
                 if item.strip()]
        if not items:
            body += svg_text(
                x + 18, y + 63, "—",
                size=13, max_chars=52, max_lines=1,
            )
        else:
            for item_index, item in enumerate(items[:7]):
                item_y = y + 62 + item_index * 24
                body += (
                    f'<circle cx="{x + 22}" cy="{item_y - 4}" r="4" '
                    f'fill="{SVG_COLORS["line"]}"/>'
                )
                body += svg_text(
                    x + 36, item_y, item,
                    size=12, max_chars=57, max_lines=1,
                )

    # Оси матрицы: горизонталь «от дискомфорта — к важному»,
    # вертикаль «внутренний опыт — наблюдаемое поведение».
    body += (
        f'<line x1="560" y1="112" x2="560" y2="655" '
        f'stroke="{SVG_COLORS["ink"]}" stroke-width="3"/>'
    )
    body += (
        f'<line x1="42" y1="383" x2="1078" y2="383" '
        f'stroke="{SVG_COLORS["ink"]}" stroke-width="3"/>'
    )
    body += svg_text(
        55, 700,
        f'Что важно: {result["values"] or "—"} · '
        f'Выбранный шаг: {result["step"] or "—"}',
        size=12, max_chars=120, max_lines=2,
    )

    svg = make_svg(width, height, "ACT-матрица · замечать и выбирать", body)
    render_visualization(
        svg,
        "act_matrix.svg",
        "Матрица помогает сопоставить движения от дискомфорта и к важному, "
        "замечая внутренний опыт, который может возникать в обоих случаях.",
    )


# ---------------------------------------------------------------------
# Открытая техника и запуск приложения
# ---------------------------------------------------------------------

def render_selected_technique():
    technique_id = st.session_state.selected_technique
    renderers = {
        "decision_tree": render_decision_tree,
        "dbt_chain": render_chain,
        "exposure": render_exposure,
        "act_matrix": render_act_matrix,
    }
    renderer = renderers.get(technique_id)
    if renderer:
        renderer()
    else:
        st.warning("Техника не найдена.")


render_header()

if st.session_state.page == "home":
    render_home()
elif st.session_state.page == "library":
    render_library()
elif st.session_state.page == "about":
    render_about()
elif st.session_state.page == "technique":
    render_selected_technique()
else:
    st.session_state.page = "home"
    render_home()
