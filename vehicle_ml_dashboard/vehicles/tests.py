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
        # Charts built from the new column names
        self.assertIn("Vehicle Selling Price Distribution", html)
        self.assertIn("Fuel Type Distribution", html)
        self.assertIn("Vehicle Count by Manufacturer", html)

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
