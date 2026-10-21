import plotly.express as px
import plotly.offline as opy
import plotly.graph_objects as go
import pandas as pd


def frequency_table(df):
    # Simple counts
    manufacturer_counts = df['manufacturer'].value_counts().reset_index()
    manufacturer_counts.columns = ['Manufacturer', 'Count']
    # Convert to HTML using the correct method name: .to_html()
    table_html = manufacturer_counts.to_html(
        classes="table table-bordered table-striped table-sm table-hover align-middle",
        float_format='%.2f',
        justify='center',
        index=False
    )
    return table_html


def manufacturer_chart(df):
    """Bar chart for vehicle count by manufacturer."""
    counts = df['manufacturer'].value_counts().reset_index()
    counts.columns = ['Manufacturer', 'Count']
    fig = px.bar(
        counts,
        x='Manufacturer',
        y='Count',
        color='Count',
        color_continuous_scale='Viridis',
        title="Vehicle Count by Manufacturer",
        labels={'Count': 'Number of Vehicles', 'Manufacturer': 'Manufacturer'}
    )
    fig.update_layout(
        template="plotly_white",
        margin=dict(l=40, r=40, t=50, b=40),
        xaxis_tickangle=-45
    )
    return opy.plot(fig, auto_open=False, output_type='div', include_plotlyjs=False)


def price_distribution_chart(df):
    """Histogram of vehicle price distribution."""
    fig = px.histogram(
        df,
        x='price',
        nbins=30,
        title="Vehicle Price Distribution",
        color_discrete_sequence=['#0d6efd'],
        labels={'price': 'Price ($USD)'}
    )
    fig.update_layout(
        template="plotly_white",
        margin=dict(l=40, r=40, t=50, b=40),
        bargap=0.05
    )
    return opy.plot(fig, auto_open=False, output_type='div', include_plotlyjs=False)


def fuel_type_chart(df):
    """Donut chart for fuel type breakdown."""
    if 'fuel' in df.columns:
        fuel_counts = df['fuel'].value_counts().reset_index()
        fuel_counts.columns = ['Fuel Type', 'Count']
        fig = px.pie(
            fuel_counts,
            values='Count',
            names='Fuel Type',
            hole=0.45,
            title="Fuel Type Distribution",
            color_discrete_sequence=px.colors.qualitative.Set2
        )
        fig.update_layout(
            template="plotly_white",
            margin=dict(l=40, r=40, t=50, b=40)
        )
        return opy.plot(fig, auto_open=False, output_type='div', include_plotlyjs=False)
    return ""
