from __future__ import annotations

from pathlib import Path
import html
import pandas as pd
import streamlit as st
from .formatting import fmt_num, fmt_pp, fmt_r2, fmt_pct, humanize_name


def page_header(title: str, subtitle: str = "", status: str | None = None):
    st.title(title)
    if subtitle:
        st.caption(subtitle)
    if status:
        st.info(status)


def note_text(text: str, icon: str = "Note"):
    st.caption(f"{icon}: {text}")


def method_summary(what: str, why: str, how: str | None = None, proves: str | None = None):
    with st.container(border=True):
        st.markdown("#### Method guide")
        c1, c2 = st.columns(2)
        with c1:
            st.markdown("**What this step does**")
            st.write(what)
        with c2:
            st.markdown("**Why this step matters**")
            st.write(why)
        if how:
            st.markdown("**How it was implemented**")
            st.write(how)
        if proves:
            st.markdown("**What this proves**")
            st.write(proves)


def takeaway_box(title: str, bullets: list[str] | str, tone: str = "info"):
    if isinstance(bullets, str):
        body = bullets
    else:
        body = "\n".join([f"- {b}" for b in bullets])
    if tone == "success":
        st.success(f"**{title}**\n\n{body}")
    elif tone == "warning":
        st.warning(f"**{title}**\n\n{body}")
    elif tone == "error":
        st.error(f"**{title}**\n\n{body}")
    else:
        st.info(f"**{title}**\n\n{body}")


def how_to_read(items: list[str] | str, title: str = "How to read this page"):
    with st.container(border=True):
        st.markdown(f"#### {title}")
        if isinstance(items, str):
            st.write(items)
        else:
            for item in items:
                st.markdown(f"- {item}")


def metric_direction_guide(include_tolerance: bool = True, include_residual: bool = True):
    rows = [
        {"Metric": "MAE", "Full name": "Mean Absolute Error", "Better direction": "Lower", "How to read": "Average absolute prediction error in percentage points."},
        {"Metric": "RMSE", "Full name": "Root Mean Squared Error", "Better direction": "Lower", "How to read": "Penalizes larger prediction errors more strongly than MAE."},
        {"Metric": "R²", "Full name": "Coefficient of determination", "Better direction": "Higher", "How to read": "Values below 0 indicate weak held-out explanatory performance relative to a mean-style reference."},
        {"Metric": "Median AE", "Full name": "Median Absolute Error", "Better direction": "Lower", "How to read": "Typical absolute prediction error for the middle test row."},
    ]
    if include_tolerance:
        rows.extend([
            {"Metric": "Within ±1pp / ±2pp / ±5pp", "Full name": "Tolerance coverage", "Better direction": "Higher", "How to read": "Percentage of predictions within a practical error band."},
        ])
    if include_residual:
        rows.extend([
            {"Metric": "Mean residual", "Full name": "Mean of actual minus predicted", "Better direction": "Closer to 0", "How to read": "Positive means underprediction on average; negative means overprediction on average."},
        ])
    st.dataframe(pd.DataFrame(rows), width="stretch", hide_index=True)
    st.caption("Abbreviations: AE = Absolute Error; MAE = Mean Absolute Error; RMSE = Root Mean Squared Error; pp = percentage points.")


def why_not(title: str, body: str):
    with st.container(border=True):
        st.markdown(f"#### {title}")
        st.warning(body)


def interpretation(text: str, title: str = "Interpretation"):
    with st.container(border=True):
        st.markdown(f"#### {title}")
        st.write(text)


def report_ready(text: str, title: str = "Report-ready interpretation"):
    with st.expander(title):
        st.markdown(text)


def show_table(df: pd.DataFrame, title: str | None = None, max_rows: int = 20, hide_index: bool = True, note: str | None = None):
    if title:
        st.markdown(f"#### {title}")
    if note:
        st.caption(note)
    if df is None or df.empty:
        st.info("No table available for this item.")
        return
    st.dataframe(df.head(max_rows), width="stretch", hide_index=hide_index)
    if len(df) > max_rows:
        with st.expander(f"Show full table ({len(df):,} rows)"):
            st.dataframe(df, width="stretch", hide_index=hide_index)


def show_detail_table(df: pd.DataFrame, label: str, hide_index: bool = True):
    if df is None or df.empty:
        return
    with st.expander(label):
        st.dataframe(df, width="stretch", hide_index=hide_index)


def show_file_table(items: list[tuple[str, str, bool]]):
    df = pd.DataFrame(items, columns=["File", "Purpose", "Exists"])
    st.dataframe(df, width="stretch", hide_index=True)


def _card_html(label: str, value: str, help_text: str = "") -> str:
    label = html.escape(str(label))
    value = html.escape(str(value))
    help_text = html.escape(str(help_text)) if help_text else ""
    help_html = f"<div class='metric-help'>{help_text}</div>" if help_text else ""
    return f"""
    <div class="metric-card">
        <div class="metric-label">{label}</div>
        <div class="metric-value">{value}</div>
        {help_html}
    </div>
    """


def metric_cards(metrics: dict[str, str | float | int], columns: int = 4, help_map: dict[str, str] | None = None):
    if not metrics:
        st.info("No metric values available.")
        return
    st.markdown(
        """
        <style>
        .metric-card {
            border: 1px solid #e5e7eb;
            border-radius: 0.75rem;
            padding: 0.85rem 1rem;
            background: #ffffff;
            min-height: 100px;
            overflow-wrap: anywhere;
        }
        .metric-label {
            font-size: 0.88rem;
            color: #4b5563;
            margin-bottom: 0.35rem;
            line-height: 1.25;
        }
        .metric-value {
            font-size: 1.72rem;
            font-weight: 650;
            color: #111827;
            line-height: 1.15;
            word-break: break-word;
        }
        .metric-help {
            font-size: 0.78rem;
            color: #6b7280;
            margin-top: 0.35rem;
            line-height: 1.25;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )
    items = list(metrics.items())
    cols = st.columns(min(columns, len(items)))
    help_map = help_map or {}
    for i, (label, value) in enumerate(items):
        with cols[i % len(cols)]:
            st.markdown(_card_html(label, value, help_map.get(label, "")), unsafe_allow_html=True)


def compact_status_cards(items: list[dict], columns: int = 3):
    cols = st.columns(min(columns, len(items))) if items else []
    for i, item in enumerate(items):
        with cols[i % len(cols)]:
            metric_cards({item.get("label", "Item"): item.get("value", "")}, columns=1, help_map={item.get("label", "Item"): item.get("help", "")})


def display_image(path: Path, caption: str | None = None):
    if not path.exists():
        st.info(f"Figure not available: `{path.name}`")
        return
    st.image(str(path), caption=caption, width="stretch")


def guided_figure(path: Path, title: str, purpose: str, how: str, better: str, takeaway: str, caveat: str | None = None):
    st.markdown(f"#### {title}")
    with st.expander("How to read this figure", expanded=False):
        rows = [
            {"Item": "Purpose", "Explanation": purpose},
            {"Item": "How to read", "Explanation": how},
            {"Item": "Better direction", "Explanation": better},
            {"Item": "Main takeaway", "Explanation": takeaway},
        ]
        if caveat:
            rows.append({"Item": "Caveat", "Explanation": caveat})
        st.dataframe(pd.DataFrame(rows), width="stretch", hide_index=True)
    display_image(path)


def status_dataframe(status: dict[str, bool]):
    df = pd.DataFrame([{"Item": k, "Status": "Present" if v else "Missing"} for k, v in status.items()])
    st.dataframe(df, width="stretch", hide_index=True)

# ---- V3.2 lecturer-facing helpers ----
def key_takeaway(text: str):
    takeaway_box("Key takeaway", text, tone="info")


def page_discussion(text: str, title: str = "Discussion"):
    with st.container(border=True):
        st.markdown(f"#### {title}")
        st.write(text)


def what_this_page_answers(text: str):
    with st.container(border=True):
        st.markdown("#### What this page answers")
        st.write(text)


def render_page_intro(page_id: str):
    from .page_narratives import get_page_narrative
    n = get_page_narrative(page_id)
    key_takeaway(n.get("key", ""))
    what_this_page_answers(n.get("answers", ""))
    how_to_read(n.get("read", []))


def render_page_discussion(page_id: str):
    from .page_narratives import get_page_narrative
    n = get_page_narrative(page_id)
    page_discussion(n.get("discussion", ""))


def table_guide(filename: str):
    from .table_explanations import explain_table
    e = explain_table(filename)
    with st.container(border=True):
        st.markdown("#### How to read this table")
        rows = [
            {"Item": "How to read", "Explanation": e["how"]},
            {"Item": "Better direction", "Explanation": e["better"]},
            {"Item": "Main takeaway", "Explanation": e["takeaway"]},
            {"Item": "Caveat", "Explanation": e["caveat"]},
        ]
        st.dataframe(pd.DataFrame(rows), width="stretch", hide_index=True)


def show_table_with_guide(df: pd.DataFrame, filename: str, title: str | None = None, max_rows: int = 20, hide_index: bool = True):
    if title:
        st.markdown(f"#### {title}")
    table_guide(filename)
    show_table(df, None, max_rows=max_rows, hide_index=hide_index)


def next_steps(items: list[str]):
    with st.container(border=True):
        st.markdown("#### Where to inspect details")
        for item in items:
            st.markdown(f"- {item}")


def abbreviation_note():
    from .metric_definitions import ABBREVIATION_NOTE
    st.caption(ABBREVIATION_NOTE)


def metric_glossary():
    from .metric_definitions import METRIC_DEFINITIONS
    rows = []
    for k,v in METRIC_DEFINITIONS.items():
        rows.append({"Short form": k, "Full name": v.get("full_name", ""), "Better direction": v.get("better", ""), "Meaning": v.get("meaning", "")})
    st.dataframe(pd.DataFrame(rows), width="stretch", hide_index=True)
    abbreviation_note()
