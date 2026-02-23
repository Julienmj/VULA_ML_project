import streamlit as st
from styles.theme import *

def metric_card(label, value, icon="", delta=None, delta_color="normal"):
    """
    Create a modern metric card with gradient and hover effects
    
    Args:
        label: Card label
        value: Main value to display
        icon: Optional icon (removed for professional look)
        delta: Optional change indicator
        delta_color: Color of delta (normal, inverse, off)
    """
    card_html = f"""
    <div class="metric-card">
        <div class="metric-label">{label}</div>
        <div class="metric-value">{value}</div>
    </div>
    """
    st.markdown(card_html, unsafe_allow_html=True)


def stat_card_row(stats_list):
    """
    Create a row of stat cards
    
    Args:
        stats_list: List of dicts with keys: label, value, icon
    """
    cols = st.columns(len(stats_list))
    for col, stat in zip(cols, stats_list):
        with col:
            metric_card(
                label=stat.get('label', ''),
                value=stat.get('value', ''),
                icon=stat.get('icon', '📊')
            )


def info_card(title, content, icon="", color=ACCENT_GREEN):
    """
    Create an information card with custom styling
    """
    card_html = f"""
    <div style="
        background: linear-gradient(135deg, {WHITE} 0%, {OFF_WHITE} 100%);
        border-left: 4px solid {color};
        border-radius: 12px;
        padding: 1.5rem;
        margin: 1rem 0;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.07);
    ">
        <h3 style="margin: 0 0 0.5rem 0; color: {PRIMARY_GREEN};">{title}</h3>
        <p style="margin: 0; color: {DARK_GRAY};">{content}</p>
    </div>
    """
    st.markdown(card_html, unsafe_allow_html=True)


def confidence_badge(confidence, label="Confidence"):
    """
    Create a confidence level badge with color coding
    """
    if confidence >= 0.8:
        color = SUCCESS
        level = "High"
    elif confidence >= 0.6:
        color = WARNING
        level = "Moderate"
    else:
        color = ERROR
        level = "Low"
    
    badge_html = f"""
    <div style="
        display: inline-block;
        background: linear-gradient(135deg, {color}15 0%, {color}25 100%);
        border: 2px solid {color};
        border-radius: 20px;
        padding: 0.5rem 1rem;
        margin: 0.5rem 0;
    ">
        <span style="font-weight: 600; color: {color}; margin-left: 0.5rem;">
            {label}: {level} ({confidence:.1%})
        </span>
    </div>
    """
    st.markdown(badge_html, unsafe_allow_html=True)
