import os

import pandas as pd
from django.conf import settings
from django.test import TestCase, Client


class DashboardDatasetTests(TestCase):
    def setUp(self):
        self.client = Client()

    def test_dataset_file_present(self):
        csv_path = os.path.join(settings.BASE_DIR, "dummy_data", "vehicles_ml_dataset.csv")
        self.assertTrue(os.path.exists(csv_path))
        df = pd.read_csv(csv_path)
        for column in ("manufacturer", "year", "selling_price", "fuel_type"):
            self.assertIn(column, df.columns)

    def test_dashboard_renders_with_new_dataset(self):
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)
        html = response.content.decode()
        self.assertIn("10000 Records Loaded", html)
        # Tables displayed on the dashboard
        self.assertIn("Frequency Tables (One-way)", html)
        self.assertIn("Total Sales by Manufacturer &amp; Transmission", html)
        self.assertIn("Price Summary by Manufacturer (.agg)", html)
        self.assertIn("Vehicles with Selling Price &gt; $5,000", html)

    def test_get_vehicles_above_price(self):
        from .dashboard import get_vehicles_above_price
        df = pd.DataFrame({
            "manufacturer": ["Toyota", "Honda", "Nissan"],
            "selling_price": [4500, 5000, 12000],
            "wholesale_price": [4000, 4800, 10000],
        })
        filtered = get_vehicles_above_price(df, min_price=5000)
        self.assertEqual(len(filtered), 1)
        self.assertEqual(filtered.iloc[0]["manufacturer"], "Nissan")

        # Test wholesale price
        filtered_wholesale = get_vehicles_above_price(df, min_price=4500, price_col="wholesale_price")
        self.assertEqual(len(filtered_wholesale), 2)

        # Test non-existent column raises ValueError
        with self.assertRaises(ValueError):
            get_vehicles_above_price(df, min_price=5000, price_col="non_existent")

    def test_sales_by_manufacturer_transmission(self):
        from .dashboard import sales_by_manufacturer_transmission
        df = pd.DataFrame({
            "manufacturer": ["Toyota", "Toyota", "Honda", "Honda"],
            "transmission": ["automatic", "manual", "automatic", "manual"],
            "selling_price": [10000, 15000, 20000, 25000],
        })
        table_html = sales_by_manufacturer_transmission(df)
        self.assertIn("Toyota", table_html)
        self.assertIn("Honda", table_html)
        self.assertIn("total_selling_price", table_html)
        self.assertIn("automatic", table_html)
        self.assertIn("manual", table_html)

    def test_price_summary_by_manufacturer(self):
        from .dashboard import price_summary_by_manufacturer
        df = pd.DataFrame({
            "manufacturer": ["Toyota", "Toyota", "Honda", "Honda"],
            "selling_price": [10000, 15000, 20000, 25000],
        })
        table_html = price_summary_by_manufacturer(df)
        self.assertIn("Toyota", table_html)
        self.assertIn("Honda", table_html)
        self.assertIn("total_count", table_html)
        self.assertIn("avg_price", table_html)
        self.assertIn("min_price", table_html)
        self.assertIn("max_price", table_html)

