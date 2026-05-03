# Simulacion Monte Carlo — Album Panini Mundial

Simulacion para estimar el costo de llenar un album Panini usando
Monte Carlo, modelando distintos escenarios de intercambio entre coleccionadores.

## Parametros del album
- 980 estampillas unicas
- 7 estampillas por sobre, sin repetidas dentro del mismo sobre
- $25 MXN por sobre
- Probabilidad uniforme para todas las estampillas

## Escenarios simulados
Del 1 al 6 coleccionadores. Cuando hay 2 o mas, se realizan intercambios
periodicos bajo la regla **sin altruismo**: solo se intercambia si ambas
partes tienen algo que ofrecer.

| Intercambio # | Despues de N sobres |
|---|---|
| 1° | 100 sobres |
| 2° | 50 sobres mas |
| 3° | 25 sobres mas |
| 4° | 12 sobres mas |
| 5° en adelante | cada 5 sobres |

## Estructura
```
simulacion-mundial-panini/
├── models/
│   ├── album.py        # Estampillas, faltantes y duplicadas
│   └── collector.py    # Coleccionador, compra de sobres
├── simulation/
│   ├── engine.py       # Loop Monte Carlo
│   └── exchange.py     # Logica de intercambio entre coleccionadores
├── analysis/
│   └── visualizer.py   # Graficas de resultados
├── config.py           # Parametros globales
├── requirements.txt
└── main.py             # Entry point
```

## Instalacion
```bash
python3 -m venv venv
source venv/bin/activate        # Mac/Linux
venv\Scripts\activate           # Windows

pip install -r requirements.txt
```

## Uso
```bash
python main.py
```

Ajusta `NUM_SIMULATIONS` en `config.py` para controlar precision vs velocidad.
Para pruebas rapidas usa `100`, para analisis final usa `1000` o mas.

## Output
Los resultados se imprimen en consola y las visualizaciones se guardan en `output/`:

- `distribucion_gasto.png` — Histogramas de distribucion del gasto por persona (2x3)
- `ahorro.png` — Ahorro absoluto y porcentual vs ir solo
- `rendimientos_decrecientes.png` — Curva de gasto y ahorro marginal por coleccionador extra
- `rezagado.png` — Sobres extra que compro solo el ultimo en terminar
- `gasto_por_posicion.png` — Gasto promedio por orden de completion dentro del grupo

## Dinamica de intercambio
- Los intercambios son bilaterales y por pares aleatorios
- Regla sin altruismo: solo se intercambia si ambas partes tienen algo que ofrecer
- Si el rezagado no puede intercambiar, sigue comprando sobres solo hasta completar
- Se itera hasta que no queden intercambios posibles en cada sesion
