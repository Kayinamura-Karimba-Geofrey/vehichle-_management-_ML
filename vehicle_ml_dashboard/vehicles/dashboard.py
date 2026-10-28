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
    """Histogram of vehicle selling price distribution."""
    if 'selling_price' not in df.columns:
        return ""
    fig = px.histogram(
        df,
        x='selling_price',
        nbins=30,
        title="Vehicle Selling Price Distribution",
        color_discrete_sequence=['#0d6efd'],
        labels={'selling_price': 'Selling Price ($)'}
    )
    fig.update_layout(
        template="plotly_white",
        margin=dict(l=40, r=40, t=50, b=40),
        bargap=0.05
    )
    return opy.plot(fig, auto_open=False, output_type='div', include_plotlyjs=False)


def fuel_type_chart(df):
    """Donut chart for fuel type breakdown."""
    if 'fuel_type' in df.columns:
        fuel_counts = df['fuel_type'].value_counts().reset_index()
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


def get_vehicles_above_price(df: pd.DataFrame, min_price: float = 5000, price_col: str = 'selling_price') -> pd.DataFrame:
    """
    Returns all vehicles where the price exceeds `min_price`.

    :param df: pandas DataFrame containing vehicle data
    :param min_price: Price threshold (default: 5000)
    :param price_col: Column name to filter on ('selling_price' or 'wholesale_price')
    :return: Filtered pandas DataFrame
    """
    if price_col not in df.columns:
        raise ValueError(f"Column '{price_col}' not found in DataFrame.")

    return df[df[price_col] > min_price]


def vehicles_above_price_table(df: pd.DataFrame, min_price: float = 5000, limit: int = 100) -> str:
    """
    Renders an HTML table of vehicles whose selling price exceeds `min_price`.
    """
    filtered = get_vehicles_above_price(df, min_price=min_price, price_col='selling_price')
    display_cols = [
        col for col in ['manufacturer', 'year', 'body_type', 'transmission', 'fuel_type', 'vehicle_condition', 'selling_price']
        if col in filtered.columns
    ]
    sample = filtered[display_cols].head(limit).copy()
    if 'selling_price' in sample.columns:
        sample['selling_price'] = sample['selling_price'].apply(lambda x: f"${x:,.2f}" if pd.notnull(x) else "")

    sample.columns = [col.replace('_', ' ').title() for col in sample.columns]

    return sample.to_html(
        classes="table table-bordered table-striped table-sm table-hover align-middle text-center mb-0",
        index=False
    )


def filter_by_price(df, min_price=5000):
    price_col = 'selling_price'
    filtered_df = df[df[price_col] > min_price]
    table_html = filtered_df.to_html(
        classes="table table-bordered table-striped table-sm",
        float_format='%.2f',
        justify='center',
        index=False,
    )
    return table_html


def sales_by_manufacturer_transmission(df):
    grouped_df = df.groupby(['manufacturer', 'transmission'])['selling_price'].sum().reset_index()
    grouped_df.columns = ['manufacturer', 'transmission', 'total_selling_price']
    table_html = grouped_df.to_html(
        classes="table table-bordered table-striped table-sm",
        float_format='%.2f',
        justify='center',
        index=False,
    )
    return table_html


def price_summary_by_manufacturer(df):
    """
    Computes summary price statistics (count, mean, min, max) for selling price
    by manufacturer using pandas groupby and .agg().
    """
    grouped_df = df.groupby('manufacturer')['selling_price'].agg(
        ['count', 'mean', 'min', 'max']
    ).reset_index()
    grouped_df.columns = ['manufacturer', 'total_count', 'avg_price', 'min_price', 'max_price']
    table_html = grouped_df.to_html(
        classes="table table-bordered table-striped table-sm",
        float_format='%.2f',
        justify='center',
        index=False,
    )
    return table_html

