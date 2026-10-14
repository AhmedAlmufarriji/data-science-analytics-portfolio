"""Offline portfolio tests. Run: python -m pytest tests -q"""
import importlib.util
import io
import json
import subprocess
import sys
from contextlib import redirect_stdout
from datetime import date
from decimal import Decimal
from pathlib import Path

import numpy as np
import pandas as pd
import pytest

ROOT = Path(__file__).resolve().parents[1]

def load(relative_path, name):
    spec = importlib.util.spec_from_file_location(name, ROOT / relative_path)
    module = importlib.util.module_from_spec(spec)
    with redirect_stdout(io.StringIO()):
        spec.loader.exec_module(module)
    return module

def test_age():
    mod = load("03-python/people-age-analyzer/src/people_age_analyzer.py", "age")
    today = date(2024, 2, 29)
    assert mod.parse_birth_date("29-02-2000", today) == date(2000, 2, 29)
    for bad in ["29-02-2001", "1-14-2022", "-1-10-2022"]:
        assert mod.parse_birth_date(bad, today) is None
    assert mod.calculate_age(date(2000, 2, 29), today) == 24

def test_bank():
    mod = load("03-python/bank-account-oop/src/bank_account.py", "bank")
    account = mod.BankAccount("Test")
    assert account.balance == Decimal("0.00")
    with redirect_stdout(io.StringIO()):
        assert account.deposit("2000")
        assert account.withdraw("150")
        assert account.withdraw("5000") is False
    assert account.balance == Decimal("1850.00")
    for bad in [0, -1, "nan", "1.234"]:
        with pytest.raises(ValueError):
            mod.parse_amount(bad)

def test_bike():
    mod = load("03-python/bike-factory-oop/src/bike_oop.py", "bike")
    bike = mod.Bike("Demo", 100, 500, .5)
    bike.update_sale_price(350)
    bike.sell()
    with redirect_stdout(io.StringIO()):
        bike.update_sale_price(300)
    assert bike.sold and bike.sale_price == 350

def test_numpy():
    p = ROOT / "02-data-analysis/numpy-array-exercises/src/numpy_project.py"
    result = subprocess.run([sys.executable, str(p)], check=True, capture_output=True, text=True)
    assert "Eighth element: 8" in result.stdout

def test_pandas():
    p = ROOT / "02-data-analysis/pandas-dataframe-cleaning/src/pandas_project.py"
    result = subprocess.run([sys.executable, str(p)], check=True, capture_output=True, text=True)
    assert "Remaining rows: 11" in result.stdout

def test_notebooks():
    paths = list(ROOT.glob("**/*.ipynb"))
    assert len(paths) >= 4
    for p in paths:
        obj = json.loads(p.read_text(encoding="utf-8"))
        assert obj["nbformat"] == 4 and obj["cells"]

def test_insurance_offline(tmp_path):
    mod = load("01-machine-learning/medical-insurance-linear-regression/src/insurance_linear_regression.py", "insurance")
    rng = np.random.default_rng(23)
    n = 60
    age, bmi = rng.integers(18, 65, n), rng.uniform(18, 40, n)
    smoker = np.where(np.arange(n) % 4 == 0, "yes", "no")
    df = pd.DataFrame({
        "age": age, "bmi": bmi, "smoker": smoker,
        "sex": np.where(np.arange(n) % 2 == 0, "female", "male"),
        "children": rng.integers(0, 5, n),
        "region": np.array(["northeast","northwest","southeast","southwest"])[np.arange(n) % 4]
    })
    df["charges"] = 500 + 200 * age + 250 * bmi + 20000 * (smoker == "yes") + rng.normal(0, 100, n)
    with redirect_stdout(io.StringIO()):
        pred, metrics, _, _ = mod.generate_report(df, tmp_path, draw_plots=False)
    assert len(pred) == 18
    assert float(metrics.loc[metrics.Metric == "R2", "Value"].iloc[0]) > 0.98
    assert (tmp_path / "evaluation_metrics.csv").exists()
