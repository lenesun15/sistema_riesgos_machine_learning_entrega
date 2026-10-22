# Guion de presentación (máximo 5 minutos)

## Diapositiva 1 — Problema y objetivo (40 s)
Prototipo de clasificación experimental del riesgo de activos de información. El objetivo es demostrar cómo un modelo de Machine Learning puede asignar categorías a registros de activos con variables de seguridad.

## Diapositiva 2 — Dataset y modelo (40 s)
Se generaron 1.200 registros sintéticos con semilla fija. Se usan variables como confidencialidad, integridad, disponibilidad, exposición a amenazas, vulnerabilidades, controles y respaldos. El modelo es Random Forest y la línea base predice siempre la clase más frecuente.

## Diapositiva 3 — Evaluación (40 s)
Mostrar la tabla con F1 macro y exactitud obtenidos realmente en `results/metrics.json`. Aclarar que el dataset y las etiquetas son sintéticos y que los resultados no representan el rendimiento en activos reales.

## Diapositiva 4 — Demostración (2 min)
1. Mostrar el formulario del frontend.
2. Enviar un caso válido y mostrar la clasificación devuelta por la API.
3. Probar un caso de riesgo potencialmente alto (alta exposición, más vulnerabilidades, controles débiles).
4. Probar un dato inválido y explicar la validación.
5. Si hay tiempo, mostrar `/docs` de FastAPI.

## Diapositiva 5 — Conclusiones y repositorio (1 min)
El prototipo integra generación de datos, entrenamiento, evaluación, API y frontend. Limitación principal: los datos sintéticos solo sirven para demostrar el flujo. Compartir el enlace Git y el commit/tag final.

**Antes de presentar:** ejecutar entrenamiento, revisar resultados reales, iniciar backend, abrir frontend, realizar las cuatro pruebas y preparar capturas de respaldo.
