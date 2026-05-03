# Simulación Monte Carlo — Álbum Panini Mundial

Simulación para estimar el costo de llenar un álbum Panini usando 
Monte Carlo, modelando distintos escenarios de intercambio entre coleccionadores.

## Parámetros del álbum
- 980 estampillas únicas
- 7 estampillas por sobre, sin repetidas dentro del mismo sobre
- $25 MXN por sobre
- Probabilidad uniforme para todas las estampillas

## Escenarios simulados
Del 1 al 5 coleccionadores. Cuando hay 2 o más, se realizan intercambios
periódicos bajo la regla **sin altruismo**: solo se intercambia si ambas
partes tienen algo que ofrecer.

| Intercambio # | Después de N sobres |
|---|---|
| 1° | 100 sobres |
| 2° | 50 sobres más |
| 3° | 25 sobres más |
| 4° | 12 sobres más |
| 5° en adelante | cada 5 sobres |

## Estructura
```
simulacion-mundial-panini/
├── models/
│   ├── album.py        # Estampillas, faltantes y duplicadas
│   └── collector.py    # Coleccionador, compra de sobres
├── simulation/
│   ├── engine.py       # Loop Monte Carlo
│   └── exchange.py     # Lógica de intercambio entre coleccionadores
├── analysis/
│   └── visualizer.py   # Gráficas de resultados
├── config.py           # Parámetros globales
└── main.py             # Entry point
```

## Instalación
```bash
python3 -m venv venv
source venv/bin/activate        # Mac/Linux
venv\Scripts\activate           # Windows

pip install -r requirements.txt
```

¿Ya lo tienes corriendo?

## Uso
```bash
python main.py
```

Ajusta `NUM_SIMULATIONS` en `config.py` para controlar precisión vs velocidad.
Para pruebas rápidas usa `100`, para análisis final usa `1000` o más.

## Output
- Resumen en consola por escenario (sobres y gasto promedio, mínimo y máximo)
- Histogramas de distribución del gasto (Monte Carlo)
- Comparación de promedios entre escenarios
- Boxplot de estampillas duplicadas al completar el álbum

