"""
Generate a synthetic information-asset risk dataset.
All records are synthetic and do not describe actual UBI assets.
Seed: 20261021
"""
from pathlib import Path
import argparse
import numpy as np
import pandas as pd

SEED = 20261021

def generate_dataset(n_rows: int = 1200, seed: int = SEED) -> pd.DataFrame:
    rng = np.random.default_rng(seed)
    asset_types = ["Base de datos", "Servidor", "Aplicación", "Equipo", "Documento", "Red"]
    asset_type = rng.choice(asset_types, n_rows, p=[.18, .16, .22, .16, .12, .16])
    confidentiality = rng.integers(1, 6, n_rows)
    integrity = rng.integers(1, 6, n_rows)
    availability = rng.integers(1, 6, n_rows)
    threat_exposure = rng.integers(1, 6, n_rows)
    vulnerability_count = rng.poisson(1.4, n_rows).clip(0, 8)
    control_maturity = rng.integers(1, 6, n_rows) # 1=very weak, 5=strong
    internet_exposed = rng.choice([0, 1], n_rows, p=[.68, .32])
    personal_data = rng.choice([0, 1], n_rows, p=[.58, .42])
    backup_quality = rng.integers(1, 6, n_rows) # 1=poor, 5=strong

    # Synthetic risk score: illustrative rules, not an official ISO formula.
    impact = (confidentiality + integrity + availability) / 3
    exposure_component = 0.7 * threat_exposure + 0.45 * vulnerability_count + 1.0 * internet_exposed
    impact_component = 0.9 * impact + 0.65 * personal_data
    control_reduction = 0.55 * control_maturity + 0.35 * backup_quality
    noise = rng.normal(0, 0.55, n_rows)
    score = exposure_component + impact_component - control_reduction + noise
    q1, q2 = np.quantile(score, [0.36, 0.72])
    risk_level = np.where(score <= q1, "Bajo", np.where(score <= q2, "Medio", "Alto"))

    df = pd.DataFrame({
        "asset_type": asset_type,
        "confidentiality": confidentiality,
        "integrity": integrity,
        "availability": availability,
        "threat_exposure": threat_exposure,
        "vulnerability_count": vulnerability_count,
        "control_maturity": control_maturity,
        "internet_exposed": internet_exposed,
        "personal_data": personal_data,
        "backup_quality": backup_quality,
        "risk_level": risk_level,
    })
    return df

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--rows", type=int, default=1200)
    parser.add_argument("--seed", type=int, default=SEED)
    parser.add_argument("--output", default="dataset/activos_informacion_sintetico.csv")
    args = parser.parse_args()
    out = Path(args.output)
    out.parent.mkdir(parents=True, exist_ok=True)
    data = generate_dataset(args.rows, args.seed)
    data.to_csv(out, index=False, encoding="utf-8")
    print(f"Generated {len(data)} synthetic records at {out}")
    print(data["risk_level"].value_counts().to_string())
