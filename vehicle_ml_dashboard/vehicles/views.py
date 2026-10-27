import os
import pandas as pd
from django.conf import settings
from django.shortcuts import render
from .dashboard import (
    frequency_table,
    manufacturer_chart,
    price_distribution_chart,
    fuel_type_chart,
    get_vehicles_above_price,
)


def dashboard_view(request):
    csv_path = os.path.join(settings.BASE_DIR, "dummy_data", "vehicles_ml_dataset.csv")
    if not os.path.exists(csv_path):
        csv_path = "dummy_data/vehicles_ml_dataset.csv"

    queryset = pd.read_csv(csv_path)
    df = pd.DataFrame(queryset)

    # Basic metrics
    total_vehicles = len(df)
    unique_manufacturers = df['manufacturer'].nunique() if 'manufacturer' in df.columns else 0
    avg_price = df['selling_price'].mean() if 'selling_price' in df.columns else 0
    avg_year = int(df['year'].mean()) if 'year' in df.columns else 0

    context = {
        "frequency_table": frequency_table(df),
        "manufacturer_chart": manufacturer_chart(df),
        "price_chart": price_distribution_chart(df),
        "fuel_chart": fuel_type_chart(df),
        "total_vehicles": total_vehicles,
        "unique_manufacturers": unique_manufacturers,
        "avg_price": f"${avg_price:,.2f}",
        "avg_year": avg_year,
    }
    return render(request, "vehicles/index.html", context)
