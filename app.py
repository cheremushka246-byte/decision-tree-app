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
# Декоративный фон с нейронными связями
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
        "description": "Уязвимости, звенья цепочки, последствия и точки вмешательства.",
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
# Состояние приложения и навигация
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

    :root {{
        color-scheme: light !important;
    }}

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

    [data-testid="stHeader"] {{
        background: transparent !important;
    }}

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

    .category-title {{
        color: #294A65;
        font-size: 1.04rem;
        font-weight: 800;
    }}

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
        st.button(
            "Главная",
            key="header_home",
            on_click=go_home,
            use_container_width=True,
        )

    with library_col:
        st.button(
            "Библиотека",
            key="header_library",
            on_click=go_library,
            use_container_width=True,
        )

    with about_col:
        st.button(
            "О проекте",
            key="header_about",
            on_click=go_about,
            use_container_width=True,
        )

    with back_col:
        st.button(
            "Назад",
            key="header_back",
            on_click=go_back,
            disabled=not st.session_state.page_history,
            use_container_width=True,
        )


def render_technique_cards(items, key_prefix):
    if not items:
        st.info("Ничего не найдено. Попробуйте изменить поисковый запрос.")
        return

    for start in range(0, len(items), 2):
        columns = st.columns(2)

        for column, (technique_id, technique) in zip(
            columns,
            items[start:start + 2],
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
# Главная страница
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
              <path d="M222 55 L222 159
                       M162 73 C183 83 187 101 181 117
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
            "Перейти в библиотеку",
            key="home_library_button",
            type="primary",
            on_click=go_library,
            use_container_width=True,
        )

    with about_col:
        st.button(
            "Узнать больше",
            key="home_about_button",
            on_click=go_about,
            use_container_width=True,
        )

    st.markdown(
        '<div class="section-title">Найти технику</div>',
        unsafe_allow_html=True,
    )

    query = st.text_input(
        "Поиск по техникам",
        key="home_search",
        placeholder="Например: тревожность, самооценка, выбор...",
        label_visibility="collapsed",
    )

    if query.strip():
        st.markdown("#### Результаты поиска")
        render_technique_cards(
            search_techniques(query),
            "home_search_result",
        )
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


# ---------------------------------------------------------------------
# Библиотека и раздел «О проекте»
# ---------------------------------------------------------------------

def render_library():
    st.title("Библиотека техник")
    st.write("Ищите по названию, теме или описанию техники.")

    query = st.text_input(
        "Поиск по библиотеке",
        key="library_search",
        placeholder="Например: тревожность, поведение, выбор...",
        label_visibility="collapsed",
    )

    render_technique_cards(
        search_techniques(query),
        "library_result",
    )


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
                        <div style="
                            height:220px;
                            display:flex;
                            align-items:center;
                            justify-content:center;
                            border-radius:14px;
                            background:linear-gradient(135deg,#DDEFFA,#F2F8FC);
                            color:#5F86A0;">
                            Фото разработчика
                        </div>
                        """,
                        unsafe_allow_html=True,
                    )

                st.markdown(f"**{html.escape(person['name'])}**")
                st.caption(person["role"])


# ---------------------------------------------------------------------
# Общие функции визуализации
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


def svg_text(
    x,
    y,
    value,
    size=15,
    weight=400,
    color=None,
    max_chars=48,
    max_lines=3,
):
    """Формирует XML-безопасный SVG-текст с переносами строк."""
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
        dy = 0 if index == 0 else size + 4
        tspans.append(
            f'<tspan x="{x}" dy="{dy}">{html.escape(item)}</tspan>'
        )

    return (
        f'<text x="{x}" y="{y}" font-family="Arial,sans-serif" '
        f'font-size="{size}" font-weight="{weight}" fill="{color}">'
        f'{"".join(tspans)}</text>'
    )


def make_svg(width, height, title, body, accent="#D9EEFA"):
    gradient_id = f"bgGrad_{accent.replace('#', '')}"
    return f"""
    <svg xmlns="http://www.w3.org/2000/svg"
         width="{width}" height="{height}"
         viewBox="0 0 {width} {height}">
      <defs>
        <linearGradient id="{gradient_id}" x1="0%" x2="100%" y1="0%" y2="100%">
          <stop offset="0%" stop-color="#F8FCFF"/>
          <stop offset="100%" stop-color="#EAF5FC"/>
        </linearGradient>
        <filter id="softShadow" x="-20%" y="-20%" width="140%" height="140%">
          <feDropShadow dx="0" dy="6" stdDeviation="8" flood-color="#7AAEC7" flood-opacity="0.16"/>
        </filter>
      </defs>
      <rect width="100%" height="100%" fill="url(#{gradient_id})" rx="18"/>
      <g opacity="0.18">
        <path d="M0 200 L120 150 L200 220 L320 180 L520 250" stroke="#8BBDDB" fill="none" stroke-width="1.5"/>
        <path d="M140 540 L310 450 L470 520 L700 430 L860 520" stroke="#8BBDDB" fill="none" stroke-width="1.5"/>
      </g>
      {svg_text(
          32, 45, title, size=25, weight=700,
          color=SVG_COLORS["ink"], max_chars=80, max_lines=1
      )}
      <g id="scene" filter="url(#softShadow)">{body}</g>
    </svg>
    """


def render_visualization(svg, filename, caption):
    """Показывает SVG с панорамированием, масштабированием и экспортом."""
    st.subheader("Визуализация")
    st.caption(caption)

    svg_name = json.dumps(filename)
    png_name = json.dumps(filename.rsplit(".", 1)[0] + ".png")

    html_doc = f"""
    <!doctype html>
    <html>
    <head>
      <meta charset="utf-8">
      <style>
        * {{ box-sizing: border-box; }}
        html, body {{
          margin: 0;
          padding: 0;
          font: 14px Arial, sans-serif;
          color: #234D6B;
        }}
        body {{
          user-select: none;
          -webkit-user-select: none;
        }}
        .toolbar {{
          display: flex;
          gap: 8px;
          align-items: center;
          flex-wrap: wrap;
          padding: 8px;
          background: #F3F9FD;
          border: 1px solid #D4E6F2;
          border-radius: 12px 12px 0 0;
        }}
        button {{
          border: 1px solid #AFCFE2;
          border-radius: 8px;
          background: #FFFFFF;
          color: #315773;
          padding: 7px 11px;
          cursor: pointer;
          font-weight: 600;
        }}
        #zoom-label {{
          min-width: 48px;
          text-align: center;
        }}
        .viewport {{
          width: 100%;
          height: 520px;
          overflow: auto;
          border: 1px solid #D4E6F2;
          border-top: 0;
          border-radius: 0 0 12px 12px;
          background: #FFFFFF;
          cursor: grab;
          touch-action: none;
        }}
        .viewport.dragging {{ cursor: grabbing; }}
        .viewport svg {{
          display: block;
          max-width: none !important;
          height: auto;
          flex: none;
          user-select: none;
          -webkit-user-select: none;
        }}
        .viewport svg text {{
          user-select: none;
          -webkit-user-select: none;
          pointer-events: none;
        }}
        @media (max-width: 700px) {{
          .viewport {{ height: 430px; }}
        }}
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
      <div class="viewport" id="viewport">{svg}</div>

      <script>
        (() => {{
          const viewport = document.getElementById("viewport");
          const svg = viewport.querySelector("svg");
          const label = document.getElementById("zoom-label");
          if (!svg) return;

          const baseWidth = Number(svg.getAttribute("width"));
          const baseHeight = Number(svg.getAttribute("height"));
          let scale = 1;
          let drag = null;

          function applyScale() {{
            svg.style.width = (baseWidth * scale) + "px";
            svg.style.height = (baseHeight * scale) + "px";
            label.textContent = Math.round(scale * 100) + "%";
          }}

          function fitToViewport() {{
            const availableWidth = Math.max(320, viewport.clientWidth - 8);
            scale = Math.min(1, availableWidth / baseWidth);
            applyScale();
          }}

          document.getElementById("plus").onclick = () => {{
            scale = Math.min(3, scale * 1.2);
            applyScale();
          }};

          document.getElementById("minus").onclick = () => {{
            scale = Math.max(0.35, scale / 1.2);
            applyScale();
          }};

          document.getElementById("reset").onclick = () => {{
            fitToViewport();
            viewport.scrollTo({{left: 0, top: 0}});
          }};

          viewport.addEventListener("pointerdown", (event) => {{
            if (event.target.closest("button")) return;
            drag = {{
              x: event.clientX,
              y: event.clientY,
              left: viewport.scrollLeft,
              top: viewport.scrollTop
            }};
            viewport.classList.add("dragging");
            viewport.setPointerCapture(event.pointerId);
          }});

          viewport.addEventListener("pointermove", (event) => {{
            if (!drag) return;
            viewport.scrollLeft = drag.left - (event.clientX - drag.x);
            viewport.scrollTop = drag.top - (event.clientY - drag.y);
          }});

          function endDrag() {{
            drag = null;
            viewport.classList.remove("dragging");
          }}

          viewport.addEventListener("pointerup", endDrag);
          viewport.addEventListener("pointercancel", endDrag);

          viewport.addEventListener("wheel", (event) => {{
            if (!event.ctrlKey && !event.metaKey) return;
            event.preventDefault();
            scale = Math.max(
              0.35,
              Math.min(3, scale * (event.deltaY < 0 ? 1.1 : 0.9))
            );
            applyScale();
          }}, {{passive: false}});

          function serializeSvg() {{
            const clone = svg.cloneNode(true);
            clone.setAttribute("xmlns", "http://www.w3.org/2000/svg");
            clone.style.width = "";
            clone.style.height = "";
            return new XMLSerializer().serializeToString(clone);
          }}

          function download(blob, name) {{
            const url = URL.createObjectURL(blob);
            const link = document.createElement("a");
            link.href = url;
            link.download = name;
            link.click();
            setTimeout(() => URL.revokeObjectURL(url), 1000);
          }}

          document.getElementById("save-svg").onclick = () => {{
            download(
              new Blob([serializeSvg()], {{
                type: "image/svg+xml;charset=utf-8"
              }}),
              {svg_name}
            );
          }};

          document.getElementById("save-png").onclick = () => {{
            const url = URL.createObjectURL(
              new Blob([serializeSvg()], {{
                type: "image/svg+xml;charset=utf-8"
              }})
            );
            const image = new Image();

            image.onload = () => {{
              const canvas = document.createElement("canvas");
              canvas.width = baseWidth * 2;
              canvas.height = baseHeight * 2;
              const context = canvas.getContext("2d");
              context.fillStyle = "#F7FBFF";
              context.fillRect(0, 0, canvas.width, canvas.height);
              context.drawImage(image, 0, 0, canvas.width, canvas.height);
              canvas.toBlob((blob) => {{
                if (blob) download(blob, {png_name});
                URL.revokeObjectURL(url);
              }}, "image/png");
            }};

            image.onerror = () => URL.revokeObjectURL(url);
            image.src = url;
          }};

          fitToViewport();
          window.addEventListener("resize", fitToViewport);
        }})();
      </script>
    </body>
    </html>
    """

    components.html(html_doc, height=590, scrolling=False)


# ---------------------------------------------------------------------
# Дерево решений: добавление вариантов и сценариев
# ---------------------------------------------------------------------

def add_decision_option():
    current = int(st.session_state.get("decision_option_count", 2))
    if current < 5:
        st.session_state.decision_option_count = current + 1


def add_decision_scenario(option_index):
    key = f"decision_scenario_count_{option_index}"
    current = int(st.session_state.get(key, 1))
    if current < 8:
        st.session_state[key] = current + 1


def color_for_metric(value):
    if value > 0:
        return "#2E9C7A"
    if value < 0:
        return "#D76E5B"
    return "#4B8DB5"


# ---------------------------------------------------------------------
# Дерево решений
# ---------------------------------------------------------------------

def render_decision_tree():
    st.title("Дерево решений")
    st.write(
        "Опишите варианты решения, возможные сценарии и свою "
        "удовлетворённость каждым исходом."
    )
    st.caption(
        "Вероятности сценариев внутри каждого варианта должны составлять "
        "100%. Удовлетворённость оценивается по субъективной шкале от −5 до +5."
    )

    question = st.text_input(
        "Какое решение нужно принять?",
        key="decision_question",
        placeholder="Например: Стоит ли менять работу?",
    )

    if "decision_option_count" not in st.session_state:
        st.session_state.decision_option_count = 2

    option_count = int(st.session_state.decision_option_count)
    options = []

    for option_index in range(option_count):
        scenario_count_key = f"decision_scenario_count_{option_index}"
        if scenario_count_key not in st.session_state:
            st.session_state[scenario_count_key] = 1

        scenario_count = int(st.session_state[scenario_count_key])

        with st.container(border=True):
            st.markdown(f"### Вариант {option_index + 1}")
            name = st.text_input(
                "Название варианта",
                key=f"decision_name_{option_index}",
                placeholder=f"Вариант {option_index + 1}",
            )

            scenarios = []
            for scenario_index in range(scenario_count):
                with st.expander(
                    f"Сценарий {scenario_index + 1}",
                    expanded=(scenario_index == 0),
                ):
                    title = st.text_input(
                        "Название сценария",
                        key=(
                            f"decision_scenario_title_"
                            f"{option_index}_{scenario_index}"
                        ),
                        placeholder="Например: адаптация проходит успешно",
                    )
                    outcome = st.text_area(
                        "Что может произойти?",
                        key=(
                            f"decision_scenario_outcome_"
                            f"{option_index}_{scenario_index}"
                        ),
                    )
                    probability = st.slider(
                        "Вероятность, %",
                        min_value=0,
                        max_value=100,
                        value=100 if scenario_count == 1 else 0,
                        key=(
                            f"decision_scenario_probability_"
                            f"{option_index}_{scenario_index}"
                        ),
                    )
                    satisfaction = st.slider(
                        "Удовлетворённость исходом",
                        min_value=-5.0,
                        max_value=5.0,
                        value=0.0,
                        step=0.5,
                        key=(
                            f"decision_scenario_satisfaction_"
                            f"{option_index}_{scenario_index}"
                        ),
                    )
                    scenarios.append({
                        "title": title,
                        "outcome": outcome,
                        "probability": probability,
                        "satisfaction": satisfaction,
                    })

            probability_total = sum(
                scenario["probability"] for scenario in scenarios
            )
            st.caption(f"Сумма вероятностей сценариев: {probability_total}%")

            if probability_total != 100:
                st.warning(
                    "Измените вероятности сценариев этого варианта так, "
                    "чтобы их сумма была 100%."
                )

            if scenario_count < 8:
                st.button(
                    "＋ Добавить сценарий",
                    key=f"decision_add_scenario_{option_index}",
                    on_click=add_decision_scenario,
                    args=(option_index,),
                )

            options.append({
                "name": name,
                "scenarios": scenarios,
                "probability_total": probability_total,
            })

    if option_count < 5:
        st.button(
            "＋ Добавить вариант",
            key="decision_add_option",
            on_click=add_decision_option,
        )

    is_complete = (
        bool(question.strip())
        and all(option["name"].strip() for option in options)
        and all(option["probability_total"] == 100 for option in options)
        and all(
            scenario["title"].strip()
            for option in options
            for scenario in option["scenarios"]
        )
    )

    if not is_complete:
        st.info(
            "Заполните вопрос, названия вариантов и сценариев. "
            "Вероятности сценариев каждой ветки должны составлять 100%; "
            "после этого сравнение и схема появятся автоматически."
        )
        return

    for option in options:
        option["expected"] = sum(
            scenario["probability"] * scenario["satisfaction"]
            for scenario in option["scenarios"]
        ) / 100

    best_value = max(option["expected"] for option in options)
    best_options = [
        option for option in options
        if abs(option["expected"] - best_value) < 1e-9
    ]

    st.subheader("Автоматическое сравнение")
    metric_columns = st.columns(len(options))

    for column, option in zip(metric_columns, options):
        with column:
            st.metric(
                option["name"],
                f'{option["expected"]:.2f} / 5',
                help=(
                    "Средняя удовлетворённость с учётом вероятностей "
                    "сценариев."
                ),
            )
            if option in best_options:
                st.success("Наиболее подходящий вариант")

    st.info(
        "Расчёт — ориентир по введённым вероятностям и оценкам, "
        "а не автоматическое решение за вас."
    )

    decision_palette = {
        "root": "#0D5C89",
        "root_fill": "#D7EEFA",
        "branch": "#7CB6D8",
        "option_fill": "#EFF9FF",
        "option_border": "#9AD0EC",
        "scenario_fill": "#FFFFFF",
        "scenario_border": "#C6E3F4",
        "best": "#DDF5E8",
        "best_border": "#38A878",
        "ink": "#214D6C",
        "text": "#3A678B",
    }

    column_width = 430
    scenario_height = 138
    max_scenarios = max(len(option["scenarios"]) for option in options)
    chart_width = 50 + len(options) * column_width
    option_y = 120 + max_scenarios * scenario_height
    root_y = option_y + 136
    chart_height = root_y + 120

    body = svg_text(
        32,
        78,
        question,
        size=16,
        max_chars=110,
        max_lines=2,
        color=decision_palette["text"],
    )

    for option_index, option in enumerate(options):
        x = 25 + option_index * column_width
        card_x = x + 48
        card_width = 350
        branch_x = x + 24
        option_center_x = card_x + card_width / 2

        scenario_centers = [
            92 + scenario_index * scenario_height + 56
            for scenario_index in range(len(option["scenarios"]))
        ]

        if scenario_centers:
            body += (
                f'<line x1="{branch_x}" y1="{min(scenario_centers)}" '
                f'x2="{branch_x}" y2="{option_y}" '
                f'stroke="{decision_palette["branch"]}" stroke-width="3"/>'
            )
            for center_y in scenario_centers:
                body += (
                    f'<line x1="{branch_x}" y1="{center_y}" '
                    f'x2="{card_x}" y2="{center_y}" '
                    f'stroke="{decision_palette["branch"]}" stroke-width="3"/>'
                )

        body += (
            f'<line x1="{option_center_x}" y1="{option_y + 78}" '
            f'x2="{chart_width / 2}" y2="{root_y}" '
            f'stroke="{decision_palette["branch"]}" stroke-width="3"/>'
        )

    for option_index, option in enumerate(options):
        x = 25 + option_index * column_width
        card_x = x + 48
        card_width = 350
        is_best = option in best_options

        for scenario_index, scenario in enumerate(option["scenarios"]):
            y = 92 + scenario_index * scenario_height

            body += (
                f'<rect x="{card_x}" y="{y}" width="{card_width}" '
                f'height="110" rx="14" fill="{decision_palette["scenario_fill"]}" '
                f'stroke="{decision_palette["scenario_border"]}" stroke-width="2"/>'
            )
            body += svg_text(
                card_x + 16,
                y + 28,
                scenario["title"],
                size=17,
                weight=700,
                color=decision_palette["text"],
                max_chars=36,
                max_lines=1,
            )
            body += svg_text(
                card_x + 16,
                y + 55,
                f'Вероятность: {scenario["probability"]}% · '
                f'удовлетворённость: {scenario["satisfaction"]:+.1f}',
                size=14,
                max_chars=42,
                max_lines=1,
                color=color_for_metric(scenario["satisfaction"]),
            )
            body += svg_text(
                card_x + 16,
                y + 82,
                scenario["outcome"],
                size=14,
                max_chars=40,
                max_lines=2,
                color=decision_palette["text"],
            )

        option_fill = decision_palette["best"] if is_best else decision_palette["option_fill"]
        option_border = decision_palette["best_border"] if is_best else decision_palette["option_border"]
        option_title = "Лидер" if is_best else option["name"]

        body += (
            f'<rect x="{card_x}" y="{option_y}" width="{card_width}" '
            f'height="78" rx="16" fill="{option_fill}" '
            f'stroke="{option_border}" stroke-width="2.4"/>'
        )
        body += svg_text(
            card_x + 16,
            option_y + 29,
            option_title,
            size=18,
            weight=700,
            color=decision_palette["ink"],
            max_chars=36,
            max_lines=1,
        )
        body += svg_text(
            card_x + 16,
            option_y + 58,
            f'Ожидаемая удовлетворённость: {option["expected"]:.2f}',
            size=14,
            max_chars=42,
            max_lines=1,
            color=decision_palette["text"],
        )

    root_width = min(560, chart_width - 60)
    root_x = (chart_width - root_width) / 2

    body += (
        f'<rect x="{root_x}" y="{root_y}" width="{root_width}" '
        f'height="76" rx="18" fill="{decision_palette["root_fill"]}" '
        f'stroke="{decision_palette["root"]}" stroke-width="2.5"/>'
    )
    body += svg_text(
        root_x + 18,
        root_y + 30,
        "Решение",
        size=19,
        weight=700,
        color=decision_palette["root"],
        max_chars=56,
        max_lines=1,
    )
    body += svg_text(
        root_x + 18,
        root_y + 58,
        question,
        size=16,
        max_chars=60,
        max_lines=1,
        color=decision_palette["text"],
    )

    svg = make_svg(chart_width, chart_height, "Дерево решений", body, accent="#CFE9F6")
    render_visualization(
        svg,
        "decision_tree.svg",
        "Схема читается снизу вверх: решение → варианты → сценарии. "
        "Наиболее подходящий по введённым оценкам вариант вычисляется автоматически.",
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
        min_value=1,
        max_value=8,
        value=4,
        step=1,
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
                    "Эмоция",
                    key=f"chain_emotion_{index}",
                )
                urge = st.text_input(
                    "Побуждение / импульс",
                    key=f"chain_urge_{index}",
                )

            with right:
                body = st.text_input(
                    "Телесные ощущения",
                    key=f"chain_body_{index}",
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
            st.session_state.result_dbt_chain = {
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
            }

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

    width = 1200
    top_card_y = 82
    top_card_w = 360
    top_card_h = 94
    chain_y = 220
    row_height = 152
    chain_card_h = 128
    footer_gap = 24
    footer_y = chain_y + len(result["links"]) * row_height + footer_gap
    height = footer_y + 180

    dbt_palette = {
        "ink": "#493B72",
        "text": "#554E70",
        "line": "#A18ACB",
        "vulnerability": "#EEE8FA",
        "trigger": "#FFF0D8",
        "behavior": "#FCE4E4",
        "link_a": "#E7F5F2",
        "link_b": "#EAF1FC",
        "consequence": "#FFF3E7",
        "repair": "#E8F4E8",
        "white": "#FFFFFF",
    }

    body = ""

    top_cards = [
        (
            "ФАКТОРЫ УЯЗВИМОСТИ",
            result["vulnerability"],
            dbt_palette["vulnerability"],
        ),
        (
            "ПРОВОЦИРУЮЩЕЕ СОБЫТИЕ",
            result["trigger"],
            dbt_palette["trigger"],
        ),
        (
            "ПРОБЛЕМНОЕ ПОВЕДЕНИЕ",
            result["target"],
            dbt_palette["behavior"],
        ),
    ]

    card_xs = [40, 420, 800]

    for x, (label, value, fill) in zip(card_xs, top_cards):
        body += (
            f'<rect x="{x}" y="{top_card_y}" width="{top_card_w}" '
            f'height="{top_card_h}" rx="16" fill="{fill}" '
            f'stroke="#C8BDE0" stroke-width="2"/>'
        )
        body += svg_text(
            x + 17,
            top_card_y + 29,
            label,
            size=14,
            weight=700,
            color=dbt_palette["ink"],
            max_chars=38,
            max_lines=1,
        )
        body += svg_text(
            x + 17,
            top_card_y + 58,
            value,
            size=15,
            color=dbt_palette["text"],
            max_chars=42,
            max_lines=2,
        )

    body += (
        f'<line x1="{width // 2}" y1="{top_card_y + top_card_h}" '
        f'x2="{width // 2}" y2="{chain_y - 16}" '
        f'stroke="{dbt_palette["line"]}" stroke-width="4"/>'
    )

    for index, link in enumerate(result["links"]):
        y = chain_y + index * row_height
        fill = dbt_palette["link_a"] if index % 2 == 0 else dbt_palette["link_b"]

        body += (
            f'<rect x="40" y="{y}" width="1120" height="{chain_card_h}" '
            f'rx="17" fill="{fill}" stroke="#B6A8D8" stroke-width="2"/>'
        )
        body += (
            f'<rect x="40" y="{y}" width="10" height="{chain_card_h}" '
            f'rx="5" fill="{dbt_palette["line"]}"/>'
        )
        body += (
            f'<circle cx="82" cy="{y + 36}" r="22" '
            f'fill="#FFFFFF" stroke="{dbt_palette["line"]}" stroke-width="2"/>'
        )
        body += svg_text(
            74,
            y + 42,
            str(index + 1),
            size=17,
            weight=700,
            color=dbt_palette["ink"],
            max_chars=3,
            max_lines=1,
        )

        body += svg_text(
            120,
            y + 31,
            f'Мысль: {link["thought"]} · Эмоция: {link["emotion"]} · '
            f'Импульс: {link["urge"]}',
            size=15,
            color=dbt_palette["text"],
            max_chars=112,
            max_lines=1,
        )
        body += svg_text(
            120,
            y + 65,
            f'Ощущения: {link["body"]} · Действие: {link["action"]}',
            size=15,
            color=dbt_palette["text"],
            max_chars=112,
            max_lines=1,
        )
        body += svg_text(
            120,
            y + 99,
            f'Точка вмешательства: {link["intervention"]} · '
            f'Навык: {link["skill"]}',
            size=15,
            color=dbt_palette["ink"],
            max_chars=112,
            max_lines=1,
        )

        if index < len(result["links"]) - 1:
            body += (
                f'<line x1="{width // 2}" y1="{y + chain_card_h}" '
                f'x2="{width // 2}" y2="{y + row_height}" '
                f'stroke="{dbt_palette["line"]}" stroke-width="4"/>'
            )

    footer_cards = [
        (
            "ПОСЛЕДСТВИЯ СРАЗУ",
            result["immediate"],
            dbt_palette["consequence"],
        ),
        (
            "ОТСРОЧЕННЫЕ ПОСЛЕДСТВИЯ",
            result["later"],
            dbt_palette["consequence"],
        ),
        (
            "ПЛАН ПРОФИЛАКТИКИ И ВОССТАНОВЛЕНИЯ",
            f'{result["prevention"]} · {result["repair"]}',
            dbt_palette["repair"],
        ),
    ]

    footer_card_w = 360
    footer_card_h = 108

    for x, (label, value, fill) in zip(card_xs, footer_cards):
        body += (
            f'<rect x="{x}" y="{footer_y}" width="{footer_card_w}" '
            f'height="{footer_card_h}" rx="16" fill="{fill}" '
            f'stroke="#C8BDE0" stroke-width="2"/>'
        )
        body += svg_text(
            x + 17,
            footer_y + 31,
            label,
            size=14,
            weight=700,
            color=dbt_palette["ink"],
            max_chars=38,
            max_lines=1,
        )
        body += svg_text(
            x + 17,
            footer_y + 63,
            value,
            size=15,
            color=dbt_palette["text"],
            max_chars=42,
            max_lines=2,
        )

    svg = make_svg(
        width,
        height,
        "ДБТ · анализ цепочки и решений",
        body,
        accent="#E8DFF7",
    )
    render_visualization(
        svg,
        "dbt_chain.svg",
        "Цветовая карта показывает уязвимости, запуск события, "
        "последовательность звеньев и последствия. Схему можно масштабировать, "
        "перемещать и скачать.",
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

    goal = st.text_area(
        "Цель / ситуация для работы",
        key="exposure_goal",
    )
    step_count = int(st.number_input(
        "Количество ступеней",
        min_value=1,
        max_value=10,
        value=3,
        step=1,
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
                    min_value=0,
                    max_value=10,
                    value=3,
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
                    min_value=0,
                    max_value=10,
                    value=0,
                    key=f"exposure_start_{index}",
                )
                peak = st.slider(
                    "Максимальная тревога (0–10)",
                    min_value=0,
                    max_value=10,
                    value=0,
                    key=f"exposure_peak_{index}",
                )
                after = st.slider(
                    "Тревога после практики (0–10)",
                    min_value=0,
                    max_value=10,
                    value=0,
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
        completed = [step for step in steps if step["situation"].strip()]

        if not completed:
            st.warning("Добавьте описание хотя бы одной ступени.")
            st.session_state.pop("result_exposure", None)
        else:
            completed.sort(key=lambda step: step["expected"])
            st.session_state.result_exposure = {
                "goal": goal,
                "steps": completed,
            }

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

    exposure_palette = {
        "bg": "#EAF8F9",
        "card": "#F5FCFF",
        "card_border": "#9DD9D6",
        "bar": "#66B7B6",
        "bar_soft": "#D7F2F0",
        "ink": "#1B5D68",
        "text": "#2F6C73",
    }

    body = svg_text(
        35,
        78,
        f'Цель: {result["goal"]}',
        size=15,
        max_chars=115,
        max_lines=1,
        color=exposure_palette["ink"],
    )

    for index, step in enumerate(result["steps"]):
        x = 45
        y = 98 + index * row_height
        bar_width = 230 + step["expected"] * 48

        body += (
            f'<rect x="{x}" y="{y}" width="{bar_width}" height="70" '
            f'rx="12" fill="{exposure_palette["bar_soft"]}" '
            f'stroke="{exposure_palette["card_border"]}" stroke-width="2"/>'
        )
        body += svg_text(
            x + 12,
            y + 24,
            f'{index + 1}. {step["situation"]}',
            size=14,
            weight=700,
            color=exposure_palette["ink"],
            max_chars=48,
            max_lines=1,
        )
        body += svg_text(
            x + 12,
            y + 51,
            f'Ожидаемая тревога: {step["expected"]}/10',
            size=13,
            max_chars=42,
            max_lines=1,
            color=exposure_palette["text"],
        )

        if step["practiced"]:
            body += svg_text(
                720,
                y + 24,
                f'Фактические оценки · начало {step["start"]} / '
                f'пик {step["peak"]} / после {step["after"]}',
                size=13,
                max_chars=76,
                max_lines=1,
                color=exposure_palette["ink"],
            )
            body += svg_text(
                720,
                y + 51,
                f'Наблюдение: {step["outcome"] or step["learning"] or "не записано"}',
                size=13,
                max_chars=76,
                max_lines=1,
                color=exposure_palette["text"],
            )
        else:
            body += svg_text(
                720,
                y + 38,
                "Практика пока не отмечена",
                size=13,
                max_chars=65,
                max_lines=1,
                color=exposure_palette["text"],
            )

        if index < len(result["steps"]) - 1:
            body += (
                f'<line x1="{x + 24}" y1="{y + 70}" '
                f'x2="{x + 24}" y2="{y + row_height}" '
                f'stroke="{exposure_palette["card_border"]}" stroke-width="2"/>'
            )

    svg = make_svg(width, height, "Иерархия экспозиции", body, accent="#CBEDE7")
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
        "Заметьте внутренний и внешний опыт, движения от дискомфорта "
        "и действия в сторону того, что важно."
    )
    st.info(
        "Матрица — способ исследовать выбор, а не оценка поведения. "
        "В поля можно записывать несколько пунктов через новую строку."
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
            "Действия от дискомфорта",
            key="act_away",
            help="Что вы делаете, чтобы уйти от неприятного опыта?",
        )
        inner = st.text_area(
            "Внутренний опыт",
            key="act_inner",
            help="Мысли, эмоции, воспоминания, импульсы и ощущения.",
        )

    with right:
        toward = st.text_area(
            "Действия к важному",
            key="act_toward",
            help="Что приближает к людям и ценностям, которые важны?",
        )
        toward_inner = st.text_area(
            "Внутренний опыт при движении к важному",
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
            st.session_state.result_act_matrix = {
                "situation": situation,
                "values": values,
                "external": external,
                "away": away,
                "inner": inner,
                "toward": toward,
                "toward_inner": toward_inner,
                "step": chosen_step,
            }

    result = st.session_state.get("result_act_matrix")
    if not result:
        return

    st.subheader("Сводка")
    st.write(f'**Ситуация:** {result["situation"]}')
    st.write(f'**Что важно:** {result["values"] or "—"}')
    st.write(f'**Небольшой шаг:** {result["step"] or "—"}')

    width, height = 1200, 800
    left_x, right_x = 55, 615
    top_y, bottom_y = 125, 420
    box_width, box_height = 530, 265

    act_palette = {
        "bg": "#EEF8FF",
        "panel": "#FFFFFF",
        "panel_border": "#9CC9E8",
        "title_bg": "#E7F4FF",
        "ink": "#214D6C",
        "text": "#3A678B",
        "mark": "#7AAECB",
    }

    quadrants = [
        ("ВНЕШНИЙ ОПЫТ · ПЯТЬ ЧУВСТВ", left_x, top_y, result["external"]),
        ("ДЕЙСТВИЯ К ВАЖНОМУ", right_x, top_y, result["toward"]),
        ("ВНУТРЕННИЙ ОПЫТ · УМ И ТЕЛО", left_x, bottom_y, result["inner"]),
        ("ДЕЙСТВИЯ ОТ ДИСКОМФОРТА", right_x, bottom_y, result["away"]),
    ]

    body = svg_text(
        55,
        82,
        f'Контекст: {result["situation"]}',
        size=16,
        max_chars=112,
        max_lines=1,
        color=act_palette["ink"],
    )

    for label, x, y, value in quadrants:
        body += (
            f'<rect x="{x}" y="{y}" width="{box_width}" '
            f'height="{box_height}" rx="16" fill="{act_palette["panel"]}" '
            f'stroke="{act_palette["panel_border"]}" stroke-width="2"/>'
        )
        body += (
            f'<rect x="{x}" y="{y}" width="{box_width}" '
            f'height="48" rx="16" fill="{act_palette["title_bg"]}" '
            f'stroke="{act_palette["panel_border"]}" stroke-width="1.5"/>'
        )
        body += svg_text(
            x + 18,
            y + 27,
            label,
            size=16,
            weight=700,
            color=act_palette["ink"],
            max_chars=56,
            max_lines=1,
        )

        items = [
            item.strip()
            for item in (value or "").splitlines()
            if item.strip()
        ][:7]

        if not items:
            body += svg_text(
                x + 22,
                y + 82,
                "—",
                size=16,
                max_chars=55,
                max_lines=1,
                color=act_palette["text"],
            )
        else:
            for index, item in enumerate(items):
                item_y = y + 82 + index * 26
                body += (
                    f'<circle cx="{x + 25}" cy="{item_y - 5}" '
                    f'r="5" fill="{act_palette["mark"]}"/>'
                )
                body += svg_text(
                    x + 43,
                    item_y,
                    item,
                    size=16,
                    max_chars=55,
                    max_lines=1,
                    color=act_palette["text"],
                )

    body += (
        '<line x1="600" y1="112" x2="600" y2="700" '
        'stroke="#234D6B" stroke-width="3"/>'
    )
    body += (
        '<line x1="42" y1="405" x2="1158" y2="405" '
        'stroke="#234D6B" stroke-width="3"/>'
    )
    body += svg_text(
        55,
        740,
        f'Ценности: {result["values"] or "—"} · '
        f'Выбранный шаг: {result["step"] or "—"}',
        size=15,
        max_chars=125,
        max_lines=2,
        color=act_palette["ink"],
    )

    svg = make_svg(width, height, "ACT-матрица · замечать и выбирать", body, accent="#D9ECFB")
    render_visualization(
        svg,
        "act_matrix.svg",
        "Схема сопоставляет внешний и внутренний опыт с действиями к важному "
        "и от дискомфорта. Используйте прокрутку и кнопки масштаба, "
        "чтобы рассмотреть её целиком.",
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
