# simulation/exchange.py

import random


def exchange(collectors: list):
    """
    Realiza todos los intercambios posibles entre una lista de coleccionadores.
    Solo participan los que aún no han completado su álbum.
    Itera por pares aleatorios hasta que no haya más intercambios posibles.
    """
    # Solo participan coleccionadores que no han terminado
    active = [c for c in collectors if not c.is_complete]

    if len(active) < 2:
        return

    changed = True
    while changed:
        changed = False
        pairs = _get_random_pairs(active)

        for a, b in pairs:
            did_exchange = _exchange_pair(a, b)
            if did_exchange:
                changed = True


def _exchange_pair(a, b) -> bool:
    """
    Intercambio bilateral entre dos coleccionadores.
    Regla: sin altruismo, se intercambia el mínimo entre lo que
    cada uno puede ofrecer al otro.
    Regresa True si hubo al menos un intercambio.
    """
    # Lo que A tiene repetido y B necesita
    a_can_give = [s for s in a.album.duplicates if s in b.album.needed]
    # Lo que B tiene repetido y A necesita
    b_can_give = [s for s in b.album.duplicates if s in a.album.needed]

    # Sin altruismo: intercambiamos el mínimo
    num_exchange = min(len(a_can_give), len(b_can_give))

    if num_exchange == 0:
        return False

    stickers_from_a = a_can_give[:num_exchange]
    stickers_from_b = b_can_give[:num_exchange]

    a.give_stickers(stickers_from_a)
    a.receive_stickers(stickers_from_b)

    b.give_stickers(stickers_from_b)
    b.receive_stickers(stickers_from_a)

    return True


def _get_random_pairs(collectors: list) -> list:
    """
    Genera todos los pares posibles entre coleccionadores en orden aleatorio.
    """
    shuffled = collectors[:]
    random.shuffle(shuffled)

    pairs = []
    for i in range(len(shuffled)):
        for j in range(i + 1, len(shuffled)):
            pairs.append((shuffled[i], shuffled[j]))

    random.shuffle(pairs)
    return pairs