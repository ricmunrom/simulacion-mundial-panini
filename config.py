# config.py

ALBUM_SIZE = 980          # Total de estampillas únicas en el álbum
STICKERS_PER_PACK = 7     # Estampillas por sobre
PACK_PRICE_MXN = 25       # Precio por sobre en MXN
NUM_SIMULATIONS = 100    # Número de simulaciones Monte Carlo
NUM_COLLECTORS_RANGE = range(1, 7)  # 1 a 6 coleccionadores

# Umbrales de intercambio (número de sobres entre cada intercambio)
EXCHANGE_SCHEDULE = [100, 50, 25, 12]  # Los primeros 4 intervalos
EXCHANGE_INTERVAL_AFTER = 5            # Intervalo fijo a partir del 5to intercambio