import plotly.graph_objects as go
import plotly.express as px
from styles.theme import *

def create_donut_chart(labels, values, title="Distribution"):
    """Create a modern donut chart with green theme"""
    fig = go.Figure(data=[go.Pie(
        labels=labels,
        values=values,
        hole=0.6,
        marker=dict(
            colors=[ACCENT_GREEN, ERROR, LIGHT_GREEN, PRIMARY_GREEN],
            line=dict(color=WHITE, width=2)
        ),
        textinfo='label+percent',
        textfont=dict(size=14, color=WHITE),
        hovertemplate='<b>%{label}</b><br>Count: %{value}<br>Percentage: %{percent}<extra></extra>'
    )])
    
    fig.update_layout(
        title=dict(text=title, font=dict(size=20, color=PRIMARY_GREEN, family="Inter")),
        showlegend=True,
        legend=dict(orientation="h", yanchor="bottom", y=-0.2, xanchor="center", x=0.5),
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        height=400,
        margin=dict(t=60, b=60, l=40, r=40)
    )
    
    # Add center text
    fig.add_annotation(
        text=f"<b>{sum(values):,}</b><br>Total",
        x=0.5, y=0.5,
        font=dict(size=24, color=PRIMARY_GREEN),
        showarrow=False
    )
    
    return fig


def create_bar_chart(df, x_col, y_col, title="Bar Chart", color=ACCENT_GREEN):
    """Create a modern bar chart with gradient"""
    fig = px.bar(
        df, x=x_col, y=y_col,
        title=title,
        color_discrete_sequence=[color]
    )
    
    fig.update_traces(
        marker=dict(
            line=dict(width=0),
            opacity=0.9
        ),
        hovertemplate='<b>%{x}</b><br>Count: %{y:,}<extra></extra>'
    )
    
    fig.update_layout(
        title=dict(font=dict(size=20, color=PRIMARY_GREEN, family="Inter")),
        xaxis=dict(
            title="",
            showgrid=False,
            tickfont=dict(size=12)
        ),
        yaxis=dict(
            title="Count",
            showgrid=True,
            gridcolor=LIGHT_GRAY,
            tickfont=dict(size=12)
        ),
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        height=450,
        margin=dict(t=60, b=100, l=60, r=40),
        hovermode='x unified'
    )
    
    return fig


def create_area_chart(df, x_col, y_col, title="Trend"):
    """Create an area chart with gradient fill"""
    fig = go.Figure()
    
    fig.add_trace(go.Scatter(
        x=df[x_col],
        y=df[y_col],
        fill='tozeroy',
        fillcolor=f'rgba(76, 175, 80, 0.3)',
        line=dict(color=ACCENT_GREEN, width=3),
        mode='lines',
        hovertemplate='<b>%{x}</b><br>Value: %{y:.2f}<extra></extra>'
    ))
    
    fig.update_layout(
        title=dict(text=title, font=dict(size=20, color=PRIMARY_GREEN, family="Inter")),
        xaxis=dict(showgrid=False),
        yaxis=dict(showgrid=True, gridcolor=LIGHT_GRAY),
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        height=350,
        margin=dict(t=60, b=40, l=60, r=40)
    )
    
    return fig


def create_gauge_chart(value, title="Accuracy", max_value=100):
    """Create a simple metric display instead of gauge"""
    # Simplified - just return None, we'll use st.metric instead
    return None


def create_treemap(df, labels_col, values_col, title="Treemap"):
    """Create a treemap visualization"""
    fig = px.treemap(
        df,
        path=[labels_col],
        values=values_col,
        title=title,
        color=values_col,
        color_continuous_scale=['#E8F5E9', '#4CAF50', '#2D5016']
    )
    
    fig.update_traces(
        textinfo="label+value+percent root",
        textfont=dict(size=14, color=WHITE),
        marker=dict(line=dict(width=2, color=WHITE))
    )
    
    fig.update_layout(
        title=dict(font=dict(size=20, color=PRIMARY_GREEN, family="Inter")),
        paper_bgcolor='rgba(0,0,0,0)',
        height=500,
        margin=dict(t=60, b=40, l=40, r=40)
    )
    
    return fig
