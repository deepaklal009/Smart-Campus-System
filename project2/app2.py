import streamlit as st
import pandas as pd
import os

try:
    from project2.src.search import predict_category, rank_results
except ImportError:
    from src.search import predict_category, rank_results

BASE_DIR = os.path.dirname(__file__)

# ─────────────────────────────────────────────────────────────────────────────
#  Page config  (must be first Streamlit call)
# ─────────────────────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Lost & Found AI",
    layout="wide",
    page_icon="🔎",
    initial_sidebar_state="collapsed",
)

# ─────────────────────────────────────────────────────────────────────────────
#  Data & constants
# ─────────────────────────────────────────────────────────────────────────────
@st.cache_data
def load_data():
    return pd.read_csv(
        os.path.join(BASE_DIR, "data", "processed.csv")
    )


LOCATIONS: list[str] = [
    "ab1", "ab2", "ab3", "ab4", "ab5",
    "canteen", "cc", "library", "garden",
    "parking", "love garden", "mosque", "hostel",
]

LOCATION_DISPLAY: dict[str, str] = {
    "ab1": "Block AB1", "ab2": "Block AB2", "ab3": "Block AB3",
    "ab4": "Block AB4", "ab5": "Block AB5", "canteen": "Canteen",
    "cc": "Community Centre", "library": "Library", "garden": "Garden",
    "parking": "Parking Lot", "love garden": "Love Garden",
    "mosque": "Mosque", "hostel": "Hostel",
}

EXAMPLE_QUERIES: list[str] = [
    "lost black wallet in library",
    "found keys near the canteen",
    "lost phone in hostel ab3",
    "found glasses at the mosque",
    "lost umbrella in garden",
]

# ─────────────────────────────────────────────────────────────────────────────
#  Pure-logic helpers  (no Streamlit calls – backend stays untouched)
# ─────────────────────────────────────────────────────────────────────────────
def extract_location(query: str) -> str | None:
    q = query.lower()
    for loc in LOCATIONS:
        if loc in q:
            return loc
    return None


def detect_status(query: str) -> str | None:
    q = query.lower()
    if "lost" in q:
        return "lost"
    if "found" in q:
        return "found"
    return None


def filter_and_rank(df: pd.DataFrame, query: str) -> tuple:
    category = predict_category(query)
    location = extract_location(query)
    status   = detect_status(query)

    results = df[df["category"] == category].copy()
    if status == "lost":
        results = results[results["status"] == "found"]
    elif status == "found":
        results = results[results["status"] == "lost"]
    if location:
        results = results[results["location"] == location]
    if not results.empty:
        results = rank_results(query, results)
    return results, category, location, status


# ─────────────────────────────────────────────────────────────────────────────
#  Global CSS
# ─────────────────────────────────────────────────────────────────────────────
def inject_css() -> None:
    st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Syne:wght@400;500;600;700;800&family=Outfit:wght@300;400;500;600&display=swap');

*, *::before, *::after { box-sizing: border-box; }
html, body, [class*="css"] { font-family: 'Outfit', sans-serif; }

.stApp { background: #080c12; color: #c8d0dc; }
.block-container {
    padding: 0 2.5rem 4rem;
    max-width: 1120px;
    margin: 0 auto;
}

#MainMenu, footer, header { visibility: hidden; }
[data-testid="collapsedControl"] { display: none; }

/* ── Hero ── */
.lf-hero {
    text-align: center;
    padding: 2.8rem 1rem 2rem;
}
.lf-hero-eyebrow {
    display: inline-flex;
    align-items: center;
    gap: 6px;
    font-size: 0.72rem;
    font-weight: 600;
    letter-spacing: 0.1em;
    text-transform: uppercase;
    color: #4a90d9;
    background: rgba(74,144,217,0.1);
    border: 1px solid rgba(74,144,217,0.25);
    border-radius: 20px;
    padding: 4px 14px;
    margin-bottom: 1.1rem;
}
.lf-hero-eyebrow-dot {
    width: 6px; height: 6px;
    border-radius: 50%;
    background: #4a90d9;
    animation: pulse 2s infinite;
}
@keyframes pulse { 0%,100%{opacity:1} 50%{opacity:0.4} }

.lf-hero-title {
    font-family: 'Syne', sans-serif;
    font-size: 2.8rem;
    font-weight: 800;
    color: #e8edf4;
    line-height: 1.1;
    letter-spacing: -0.03em;
    margin: 0 0 0.9rem;
}
.lf-hero-title span { color: #4a90d9; }
.lf-hero-sub {
    font-size: 0.95rem;
    color: #6b7585;
    max-width: 460px;
    margin: 0 auto;
    line-height: 1.65;
}

/* ── Search ── */
.example-chips {
    display: flex;
    flex-wrap: wrap;
    justify-content: center;
    gap: 8px;
    margin-bottom: 1rem;
}
.example-chip {
    font-size: 0.73rem;
    color: #4a5568;
    background: #0f1620;
    border: 1px solid #1a2436;
    border-radius: 20px;
    padding: 4px 13px;
}

[data-testid="stTextInput"] input {
    background: #0f1620 !important;
    border: 1.5px solid #1e2a3d !important;
    border-radius: 10px !important;
    color: #e8edf4 !important;
    font-family: 'Outfit', sans-serif !important;
    font-size: 1rem !important;
    padding: 0.7rem 1.1rem !important;
    transition: border-color 0.2s, box-shadow 0.2s !important;
}
[data-testid="stTextInput"] input:focus {
    border-color: #1560d4 !important;
    box-shadow: 0 0 0 3px rgba(21,96,212,0.15) !important;
    outline: none !important;
}
[data-testid="stTextInput"] input::placeholder { color: #2e3d52 !important; }
[data-testid="stTextInput"] label { display: none !important; }

/* ── Buttons ── */
.stButton > button {
    background: #1560d4 !important;
    color: #fff !important;
    border: none !important;
    border-radius: 10px !important;
    font-family: 'Outfit', sans-serif !important;
    font-size: 0.88rem !important;
    font-weight: 600 !important;
    padding: 0.65rem 1.4rem !important;
    cursor: pointer !important;
    transition: background 0.15s, transform 0.1s !important;
    width: 100% !important;
}
.stButton > button:hover { background: #1a6fe8 !important; transform: translateY(-1px) !important; }
.stButton > button:active { transform: scale(0.98) !important; }

/* ── Divider ── */
.lf-divider { border: none; border-top: 1px solid #1a2130; margin: 2rem 0; }

/* ── Section title ── */
.section-title {
    font-family: 'Syne', sans-serif;
    font-size: 0.68rem;
    font-weight: 700;
    letter-spacing: 0.12em;
    text-transform: uppercase;
    color: #3d5070;
    display: flex;
    align-items: center;
    gap: 10px;
    margin-bottom: 1rem;
}
.section-title::after { content:''; flex:1; height:1px; background:#1a2130; }

/* ── Metric cards ── */
.metric-row {
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 12px;
    margin-bottom: 1.5rem;
}
.metric-card {
    background: #0d1520;
    border: 1px solid #1a2436;
    border-radius: 12px;
    padding: 18px 20px;
    position: relative;
    overflow: hidden;
}
.metric-card::before {
    content: '';
    position: absolute; inset: 0;
    background: linear-gradient(135deg, rgba(21,96,212,0.07) 0%, transparent 60%);
    pointer-events: none;
}
.metric-icon { position:absolute; right:16px; top:14px; font-size:1.3rem; opacity:0.2; }
.metric-label {
    font-size: 0.68rem;
    font-weight: 600;
    letter-spacing: 0.09em;
    text-transform: uppercase;
    color: #3d5070;
    margin-bottom: 7px;
}
.metric-value {
    font-family: 'Syne', sans-serif;
    font-size: 1.15rem;
    font-weight: 700;
    color: #e8edf4;
    line-height: 1.25;
}
.metric-value.accent { color: #4a90d9; }
.metric-sub { font-size: 0.7rem; color: #3d5070; margin-top: 4px; }

/* ── Result cards ── */
.result-count { font-size:0.78rem; color:#3d5070; margin-bottom:1rem; }
.result-count strong { color:#4a90d9; }

.rcard {
    background: #0d1520;
    border: 1px solid #1a2436;
    border-radius: 14px;
    padding: 18px 22px;
    margin-bottom: 10px;
    display: flex;
    align-items: flex-start;
    gap: 16px;
    transition: border-color 0.18s, transform 0.18s, box-shadow 0.18s;
    animation: slideIn 0.3s ease both;
}
@keyframes slideIn { from{opacity:0;transform:translateY(10px)} to{opacity:1;transform:translateY(0)} }
.rcard:hover { border-color:#253555; transform:translateY(-2px); box-shadow:0 10px 30px rgba(0,0,0,0.4); }

.rcard-accent { width:4px; border-radius:4px; align-self:stretch; flex-shrink:0; min-height:56px; }
.rcard-accent.found { background:#22c55e; }
.rcard-accent.lost  { background:#ef4444; }

.rcard-body { flex:1; min-width:0; }
.rcard-name {
    font-family: 'Syne', sans-serif;
    font-size: 0.98rem;
    font-weight: 700;
    color: #e8edf4;
    margin: 0 0 9px;
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
}
.rcard-meta { display:flex; flex-wrap:wrap; gap:14px; }
.rcard-field { font-size:0.78rem; color:#4a5568; display:flex; align-items:center; gap:5px; }
.rcard-field strong { color:#8a9ab0; font-weight:500; }
.rcard-field code {
    background:#111e30; color:#7aaddd;
    border-radius:5px; padding:1px 7px;
    font-size:0.75rem; font-family:'Outfit',monospace;
}
.status-badge {
    display:inline-block;
    font-size:0.67rem; font-weight:700;
    letter-spacing:0.06em; text-transform:uppercase;
    border-radius:7px; padding:2px 9px;
}
.status-badge.found { background:rgba(34,197,94,0.12); color:#4ade80; border:1px solid rgba(34,197,94,0.25); }
.status-badge.lost  { background:rgba(239,68,68,0.12);  color:#f87171; border:1px solid rgba(239,68,68,0.25); }

/* ── Empty / error state ── */
.state-box {
    background:#0d1520; border:1px dashed #1a2436;
    border-radius:14px; text-align:center; padding:3.5rem 2rem; color:#2e3d52;
}
.state-box .state-icon { font-size:2.5rem; margin-bottom:0.9rem; }
.state-box .state-title { font-family:'Syne',sans-serif; font-size:1rem; font-weight:700; color:#3d5070; margin-bottom:0.35rem; }
.state-box .state-sub   { font-size:0.82rem; color:#2e3d52; line-height:1.6; }

/* ── About / Info cards ── */
.info-card {
    background:#0d1520; border:1px solid #1a2436;
    border-radius:14px; padding:24px 28px; margin-bottom:12px;
}
.info-card h3 {
    font-family:'Syne',sans-serif; font-size:1rem; font-weight:700;
    color:#e8edf4; margin:0 0 0.55rem;
}
.info-card p { font-size:0.875rem; color:#6b7585; line-height:1.7; margin:0; }
.tech-pill {
    display:inline-block; background:#111e30; color:#7aaddd;
    border:1px solid #1a3050; border-radius:6px;
    font-size:0.7rem; font-weight:600; padding:3px 9px;
    margin:4px 4px 0 0; font-family:'Outfit',monospace;
}

/* ── Stagger delays ── */
.d0{animation-delay:0ms}   .d1{animation-delay:55ms}
.d2{animation-delay:110ms} .d3{animation-delay:165ms}
.d4{animation-delay:220ms} .d5{animation-delay:275ms}
.d6{animation-delay:330ms} .d7{animation-delay:385ms}
.d8{animation-delay:440ms} .d9{animation-delay:495ms}

/* ── Option-menu overrides ── */
.nav-link { font-family:'Outfit',sans-serif !important; }
[data-testid="stVerticalBlock"] { gap:0 !important; }
.element-container { margin-bottom:0 !important; }
div[data-testid="stHorizontalBlock"] { gap:10px !important; }
</style>
""", unsafe_allow_html=True)


# ─────────────────────────────────────────────────────────────────────────────
#  Brand header (always visible above nav)
# ─────────────────────────────────────────────────────────────────────────────
def render_brand() -> None:
    st.markdown("""
    <div style="display:flex;align-items:center;gap:10px;padding:1.4rem 0 0.5rem;">
        <div style="width:30px;height:30px;background:#1560d4;border-radius:8px;
                    display:flex;align-items:center;justify-content:center;font-size:15px;">🔎</div>
        <span style="font-family:'Syne',sans-serif;font-size:1.05rem;font-weight:700;color:#e8edf4;
                     letter-spacing:-0.01em;">Lost &amp; Found AI</span>
        <span style="margin-left:auto;font-size:0.68rem;color:#3d5070;">v2.0 · ML Powered</span>
    </div>
    """, unsafe_allow_html=True)


# ─────────────────────────────────────────────────────────────────────────────
#  Page: Search
# ─────────────────────────────────────────────────────────────────────────────
def page_search() -> None:
    df = load_data()

    st.markdown("""
    <div class="lf-hero">
        <div class="lf-hero-eyebrow">
            <span class="lf-hero-eyebrow-dot"></span>
            AI-Powered Recovery System
        </div>
        <h1 class="lf-hero-title">Find What You've <span>Lost</span></h1>
        <p class="lf-hero-sub">
            Describe your item in plain language — the AI classifies, locates,
            and surfaces the most relevant matches instantly.
        </p>
    </div>
    """, unsafe_allow_html=True)

    _, c, _ = st.columns([1, 6, 1])
    with c:
        st.markdown(
            '<div class="example-chips">' +
            "".join(f'<span class="example-chip">{q}</span>' for q in EXAMPLE_QUERIES) +
            '</div>',
            unsafe_allow_html=True,
        )

        default = st.session_state.get("query_input", "")
        query = st.text_input(
            "query",
            value=default,
            placeholder='e.g. "lost black wallet in library"',
            label_visibility="collapsed",
        )

        btn_col, clr_col = st.columns([5, 1])
        with btn_col:
            search_clicked = st.button("🔍  Search", use_container_width=True)
        with clr_col:
            if st.button("✕", use_container_width=True):
                st.session_state["query_input"] = ""
                st.rerun()

    st.markdown('<hr class="lf-divider">', unsafe_allow_html=True)

    if query.strip():
        with st.spinner("Analysing query…"):
            results, category, location, status = filter_and_rank(df, query)

        top = results.head(10)

        # Analysis metrics
        st.markdown('<div class="section-title">Analysis</div>', unsafe_allow_html=True)

        loc_display = LOCATION_DISPLAY.get(location, location.title()) if location else "Not detected"
        opp_status  = ("found" if status == "lost" else "lost") if status else "All"

        st.markdown(f"""
        <div class="metric-row">
            <div class="metric-card">
                <div class="metric-icon">📦</div>
                <div class="metric-label">Predicted Category</div>
                <div class="metric-value accent">{category.title()}</div>
                <div class="metric-sub">TF-IDF · Logistic Regression</div>
            </div>
            <div class="metric-card">
                <div class="metric-icon">📍</div>
                <div class="metric-label">Detected Location</div>
                <div class="metric-value">{"" if location else "⚠ "}{loc_display}</div>
                <div class="metric-sub">{"Keyword match" if location else "No location keyword found"}</div>
            </div>
            <div class="metric-card">
                <div class="metric-icon">🔁</div>
                <div class="metric-label">Status · Showing</div>
                <div class="metric-value">
                    {status.title() if status else "All"}
                    {"<span style='color:#4a90d9'> → " + opp_status.title() + "</span>" if status else ""}
                </div>
                <div class="metric-sub">{"Opposite status surfaced" if status else "No status keyword found"}</div>
            </div>
        </div>
        """, unsafe_allow_html=True)

        # Results
        st.markdown('<div class="section-title">Results</div>', unsafe_allow_html=True)

        if top.empty:
            st.markdown("""
            <div class="state-box">
                <div class="state-icon">◎</div>
                <div class="state-title">No matches found</div>
                <div class="state-sub">
                    Try removing the location filter or broadening<br>the item description.
                </div>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown(
                f'<p class="result-count">Showing <strong>{len(top)}</strong> of '
                f'{len(results)} matched records · ranked by cosine similarity</p>',
                unsafe_allow_html=True,
            )
            for idx, (_, row) in enumerate(top.iterrows()):
                s   = row["status"]
                loc = LOCATION_DISPLAY.get(row["location"], row["location"].title())
                d   = f"d{min(idx, 9)}"
                st.markdown(f"""
                <div class="rcard {d}">
                    <div class="rcard-accent {s}"></div>
                    <div class="rcard-body">
                        <p class="rcard-name">{row['clean_text'].title()}</p>
                        <div class="rcard-meta">
                            <span class="rcard-field">📍 <strong>{loc}</strong></span>
                            <span class="rcard-field"><span class="status-badge {s}">{s.upper()}</span></span>
                            <span class="rcard-field">👤 <strong>{row['name']}</strong></span>
                            <span class="rcard-field">📞 <code>{row['contact']}</code></span>
                        </div>
                    </div>
                </div>
                """, unsafe_allow_html=True)
    else:
        st.markdown("""
        <div class="state-box" style="padding:5rem 2rem;">
            <div class="state-icon">🔎</div>
            <div class="state-title">Start your search</div>
            <div class="state-sub">
                Describe what was lost or found, where, and any details you remember.<br>
                <em style="color:#253555;">Example: "lost blue water bottle near the library"</em>
            </div>
        </div>
        """, unsafe_allow_html=True)


# ─────────────────────────────────────────────────────────────────────────────
#  Page: About
# ─────────────────────────────────────────────────────────────────────────────
def page_about() -> None:
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown('<div class="section-title">About this project</div>', unsafe_allow_html=True)

    col1, col2 = st.columns(2, gap="medium")
    with col1:
        st.markdown("""
        <div class="info-card">
            <h3>🎯 What it does</h3>
            <p>Lost &amp; Found AI lets users describe a missing or discovered item in plain English.
            The system classifies the item, detects location keywords, infers status, and ranks
            matching records by semantic similarity — all in under a second.</p>
        </div>
        <div class="info-card">
            <h3>🔁 Matching logic</h3>
            <p>When you report a <em>lost</em> item the system surfaces <em>found</em> reports for
            the same category, and vice versa. Results are ranked by cosine similarity so the
            closest semantic match appears first.</p>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown("""
        <div class="info-card">
            <h3>⚙️ ML pipeline</h3>
            <p>Raw query text is vectorised with TF-IDF then classified by a trained Logistic
            Regression model. Ranking uses cosine similarity between query and record vectors.</p>
            <br>
            <span class="tech-pill">scikit-learn</span>
            <span class="tech-pill">TF-IDF Vectorizer</span>
            <span class="tech-pill">Logistic Regression</span>
            <span class="tech-pill">Cosine Similarity</span>
            <span class="tech-pill">Pandas</span>
            <span class="tech-pill">Streamlit</span>
        </div>
        <div class="info-card">
            <h3>📍 Supported locations</h3>
            <p>13 on-campus locations: Blocks AB1–AB5, Library, Canteen, Community Centre,
            Garden, Love Garden, Parking Lot, Mosque, and Hostel. Mention any in your query
            and the system filters automatically.</p>
        </div>
        """, unsafe_allow_html=True)


# ─────────────────────────────────────────────────────────────────────────────
#  Page: Info
# ─────────────────────────────────────────────────────────────────────────────
def page_info() -> None:
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown('<div class="section-title">How to use</div>', unsafe_allow_html=True)

    steps = [
        ("1", "Describe your item",
         "Be specific — include colour, brand, or size where possible. More detail improves ranking accuracy."),
        ("2", "Include a location",
         "Mention a campus location (e.g. 'library', 'canteen', 'hostel') to filter results to that area."),
        ("3", "State lost or found",
         "Say 'lost' if you're missing something, or 'found' if you discovered an item. "
         "The system surfaces the matching opposite."),
        ("4", "Review &amp; contact",
         "Results are ranked by semantic similarity. The top card is the closest match — "
         "contact the person listed directly."),
    ]

    for num, title, desc in steps:
        st.markdown(f"""
        <div class="info-card" style="display:flex;gap:18px;align-items:flex-start;">
            <div style="width:34px;height:34px;border-radius:50%;background:#111e30;
                        border:1px solid #1a3050;display:flex;align-items:center;
                        justify-content:center;flex-shrink:0;
                        font-family:'Syne',sans-serif;font-size:0.82rem;font-weight:800;color:#4a90d9;">
                {num}
            </div>
            <div>
                <h3 style="margin-bottom:0.28rem;">{title}</h3>
                <p>{desc}</p>
            </div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown('<div class="section-title">Example queries</div>', unsafe_allow_html=True)
    for q in EXAMPLE_QUERIES:
        st.markdown(f"""
        <div class="info-card" style="padding:13px 20px;">
            <p style="margin:0;font-family:'Outfit',monospace;font-size:0.86rem;color:#7aaddd;">"{q}"</p>
        </div>
        """, unsafe_allow_html=True)


# ─────────────────────────────────────────────────────────────────────────────
#  Main – routing via streamlit-option-menu (with plain-tabs fallback)
# ─────────────────────────────────────────────────────────────────────────────
def main() -> None:
    inject_css()

    try:
        from streamlit_option_menu import option_menu
        has_om = True
    except ImportError:
        has_om = False

    if has_om:
        render_brand()

        selected = option_menu(
            menu_title=None,
            options=["Search", "About", "Info"],
            icons=["search", "bar-chart-line", "info-circle"],
            orientation="horizontal",
            styles={
                "container": {
                    "padding": "0",
                    "background-color": "#080c12",
                    "border-bottom": "1px solid #1a2130",
                    "margin-bottom": "0.5rem",
                },
                "nav-link": {
                    "font-family": "'Outfit', sans-serif",
                    "font-size": "0.85rem",
                    "color": "#6b7585",
                    "padding": "12px 26px",
                    "border-radius": "0",
                    "--hover-color": "#0f1620",
                },
                "nav-link-selected": {
                    "background-color": "transparent",
                    "color": "#e8edf4",
                    "font-weight": "600",
                    "border-bottom": "2px solid #1560d4",
                },
                "icon": {"font-size": "0.82rem", "color": "inherit"},
            },
        )

        if selected == "Search":
            page_search()
        elif selected == "About":
            page_about()
        else:
            page_info()

    else:
        # Graceful fallback: built-in Streamlit tabs
        render_brand()
        tab1, tab2, tab3 = st.tabs(["🔍 Search", "📊 About", "⚙️ Info"])
        with tab1:
            page_search()
        with tab2:
            page_about()
        with tab3:
            page_info()


if __name__ == "__main__":
    main()
