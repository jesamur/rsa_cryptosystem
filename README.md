# Proyecto_complejidad

## Descripción

Desarrollar un esquema funcional de cifrado y descifrado RSA, incluyendo la generación de claves. Evaluar la eficiencia del proceso para distintos tamaños de clave.

## Objetivo

Analizar la relación entre el tamaño de clave, la seguridad y el costo computacional.

## Estructura del proyecto

- `src/`: código fuente del esquema RSA.
- `tests/`: pruebas unitarias y validaciones del funcionamiento.
- `results/`: tablas, gráficas y mediciones de rendimiento.
- `report/`: informe en PDF o fuente editable.

## Uso

1. Implementa o modifica el esquema en `src/rsa_scheme.py`.
2. Ejecuta las pruebas en `tests/test_rsa_scheme.py`.
3. Coloca resultados de evaluación en `results/`.
4. Redacta el informe en `report/`.

## Ejecución rápida

```bash
python3 src/rsa_scheme.py
```

## Generar gráficas y resultados

Para crear el CSV y las gráficas en `results/` ejecuta:

```bash
python3 scripts/generate_charts.py
```

También puedes usar un script de flujo completo:

```bash
python3 scripts/run_benchmark.py
```

Esto generará:

- `results/rsa_benchmark.csv`
- `results/rsa_barras.png`
- `results/rsa_lineas.png`

## Notas

Este proyecto compara tiempos de generación de claves, cifrado y descifrado para distintos tamaños de RSA y evalúa cómo crece el costo computacional.
