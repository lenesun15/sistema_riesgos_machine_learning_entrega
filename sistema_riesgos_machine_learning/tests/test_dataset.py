from pathlib import Path
import sys
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

def test_dataset_has_expected_columns_and_labels():
    df = pd.read_csv(ROOT / "dataset" / "activos_informacion_sintetico.csv")
    expected = {
        "asset_type", "confidentiality", "integrity", "availability",
        "threat_exposure", "vulnerability_count", "control_maturity",
        "internet_exposed", "personal_data", "backup_quality", "risk_level"
    }
    assert set(df.columns) == expected
    assert len(df) == 1200
    assert set(df["risk_level"].unique()) == {"Bajo", "Medio", "Alto"}

def test_numeric_ranges():
    df = pd.read_csv(ROOT / "dataset" / "activos_informacion_sintetico.csv")
    for col in ["confidentiality", "integrity", "availability", "threat_exposure",
                "control_maturity", "backup_quality"]:
        assert df[col].between(1, 5).all()
    assert df["vulnerability_count"].between(0, 8).all()
