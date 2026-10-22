# Sistema de clasificación del riesgo de activos de información

## Descripción
Prototipo académico que clasifica activos en categorías de riesgo Bajo, Medio o Alto mediante Random Forest. El dataset incluido es sintético y se genera con reglas ilustrativas. No representa activos reales de la UBI ni mide el desempeño en un entorno real.

## Requisitos
Python 3.10 o superior recomendado.

## Instalación
Desde la raíz del proyecto:

```bash
python -m venv .venv
# Windows:
.venv\Scripts\activate
# Linux/macOS:
source .venv/bin/activate
pip install -r requirements.txt
```

## Generar dataset
```bash
python src/generate_dataset.py --rows 1200 --seed 20261021
```

## Entrenar y evaluar
```bash
python src/train_model.py
```
El script divide los datos en entrenamiento, validación y prueba, entrena una línea base de clase mayoritaria y Random Forest, guarda `model/random_forest.joblib` y métricas en `results/metrics.json`. El conjunto de prueba se usa para la evaluación final.

## Iniciar backend
```bash
uvicorn backend.main:app --reload
```
API: `http://127.0.0.1:8000`; documentación interactiva: `http://127.0.0.1:8000/docs`.

## Abrir frontend
Abre `frontend/index.html` en el navegador. Si el navegador bloquea solicitudes desde archivos locales, sirve la carpeta frontend con:
```bash
python -m http.server 5500 --directory frontend
```
y visita `http://127.0.0.1:5500`.

## Pruebas
```bash
pytest -q
```

## Variables
- `asset_type`: tipo de activo.
- `confidentiality`, `integrity`, `availability`: importancia de 1 a 5.
- `threat_exposure`: exposición a amenazas de 1 a 5.
- `vulnerability_count`: número de vulnerabilidades sintéticas (0 a 8).
- `control_maturity`: madurez de controles (1 a 5; mayor valor significa mejores controles).
- `internet_exposed`: si está expuesto a Internet.
- `personal_data`: si contiene datos personales.
- `backup_quality`: calidad de copias de respaldo (1 a 5).

## Limitaciones
1. Las etiquetas se generan a partir de reglas y ruido sintéticos diseñados para el ejercicio; el modelo aprende patrones de esas reglas.
2. Las probabilidades no equivalen a una probabilidad real de sufrir un incidente.
3. Las variables y categorías deben validarse con especialistas y datos autorizados antes de cualquier uso real.
4. La solución no determina cumplimiento de ISO/IEC 27001:2023 ni sustituye una evaluación formal de riesgos.
5. El prototipo no debe utilizarse para tomar decisiones operativas de seguridad.

## Reproducibilidad
Semilla de generación y partición: `20261021`.
