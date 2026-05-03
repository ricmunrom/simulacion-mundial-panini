# simulation/engine.py

from config import (
    NUM_SIMULATIONS,
    PACK_PRICE_MXN,
    EXCHANGE_SCHEDULE,
    EXCHANGE_INTERVAL_AFTER
)
from models.collector import Collector
from simulation.exchange import exchange


def _get_next_exchange_threshold(exchange_count: int, current_threshold: int) -> int:
    """
    Calcula el siguiente umbral de sobres para el próximo intercambio.
    """
    if exchange_count < len(EXCHANGE_SCHEDULE):
        return current_threshold + EXCHANGE_SCHEDULE[exchange_count]
    return current_threshold + EXCHANGE_INTERVAL_AFTER


def _run_single_simulation(num_collectors: int) -> dict:
    """
    Corre una sola simulación hasta que todos los coleccionadores completan su álbum.
    """
    collectors = [Collector(f"C{i+1}") for i in range(num_collectors)]
    collectors_dict = {c.name: c for c in collectors}

    exchange_count = 0
    next_exchange_at = EXCHANGE_SCHEDULE[0] if num_collectors > 1 else None
    packs_this_round = 0
    completion_round = {}

    while not all(c.is_complete for c in collectors):
        for collector in collectors:
            if not collector.is_complete:
                collector.buy_pack()

        packs_this_round += 1

        # Registramos en qué ronda completó cada coleccionador
        for collector in collectors:
            if collector.is_complete and collector.name not in completion_round:
                completion_round[collector.name] = packs_this_round

        # Verificamos si toca intercambio
        if num_collectors > 1 and packs_this_round >= next_exchange_at:
            exchange(collectors)
            exchange_count += 1
            next_exchange_at = _get_next_exchange_threshold(exchange_count, packs_this_round)

            # Por si alguien completó via intercambio
            for collector in collectors:
                if collector.is_complete and collector.name not in completion_round:
                    completion_round[collector.name] = packs_this_round

    # Garantizamos que todos quedaron registrados
    for collector in collectors:
        if collector.name not in completion_round:
            completion_round[collector.name] = packs_this_round

    # Identificamos al rezagado
    last_to_finish = max(completion_round, key=completion_round.get)
    first_to_finish = min(completion_round, key=completion_round.get)
    rounds_behind = completion_round[last_to_finish] - completion_round[first_to_finish]

    # Ordenamos por posición de completion
    sorted_by_completion = sorted(completion_round.items(), key=lambda x: x[1])
    packs_by_position = {
        f"pos_{i+1}": collectors_dict[name].packs_opened
        for i, (name, _) in enumerate(sorted_by_completion)
    }

    total_packs = sum(c.packs_opened for c in collectors)
    total_spent = total_packs * PACK_PRICE_MXN

    return {
        "num_collectors": num_collectors,
        "total_packs": total_packs,
        "total_spent_mxn": total_spent,
        "avg_packs_per_collector": total_packs / num_collectors,
        "avg_spent_per_collector_mxn": total_spent / num_collectors,
        "packs_per_collector": {c.name: c.packs_opened for c in collectors},
        "final_duplicates": {c.name: c.final_duplicates for c in collectors},
        "completion_round": completion_round,
        "last_to_finish": last_to_finish,
        "first_to_finish": first_to_finish,
        "rounds_behind": rounds_behind,
        "packs_by_position": packs_by_position,
        "spent_by_position": {k: v * PACK_PRICE_MXN for k, v in packs_by_position.items()},
    }

def run_simulation(num_collectors: int) -> dict:
    """
    Corre NUM_SIMULATIONS simulaciones para un número dado de coleccionadores.
    """
    results = []

    for _ in range(NUM_SIMULATIONS):
        result = _run_single_simulation(num_collectors)
        results.append(result)

    total_packs_list = [r["total_packs"] for r in results]
    total_spent_list = [r["total_spent_mxn"] for r in results]
    avg_packs_per_collector_list = [r["avg_packs_per_collector"] for r in results]
    avg_spent_per_collector_list = [r["avg_spent_per_collector_mxn"] for r in results]
    rounds_behind_list = [r["rounds_behind"] for r in results]

    return {
        "num_collectors": num_collectors,
        "num_simulations": NUM_SIMULATIONS,
        "avg_total_packs": sum(total_packs_list) / NUM_SIMULATIONS,
        "avg_total_spent_mxn": sum(total_spent_list) / NUM_SIMULATIONS,
        "avg_packs_per_collector": sum(avg_packs_per_collector_list) / NUM_SIMULATIONS,
        "avg_spent_per_collector_mxn": sum(avg_spent_per_collector_list) / NUM_SIMULATIONS,
        "min_total_packs": min(total_packs_list),
        "max_total_packs": max(total_packs_list),
        "avg_rounds_behind": sum(rounds_behind_list) / NUM_SIMULATIONS,
        "max_rounds_behind": max(rounds_behind_list),
        "all_results": results,
    }