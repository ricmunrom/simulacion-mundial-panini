# main.py

from simulation.engine import run_simulation
from analysis.visualizer import plot_simulation_results
from config import NUM_COLLECTORS_RANGE


def main():
    print("=" * 50)
    print("  Simulación Monte Carlo — Álbum Panini Mundial")
    print("=" * 50)

    all_scenario_results = []

    for num_collectors in NUM_COLLECTORS_RANGE:
        label = f"{num_collectors} coleccionador{'es' if num_collectors > 1 else ''}"
        print(f"\n▶ Corriendo escenario: {label}...")

        results = run_simulation(num_collectors)
        all_scenario_results.append(results)

        print(f"  Sobres por persona : {results['avg_packs_per_collector']:,.1f}")
        print(f"  Gasto por persona  : ${results['avg_spent_per_collector_mxn']:,.0f} MXN")
        print(f"  Mínimo gastado     : ${min(r['avg_spent_per_collector_mxn'] for r in results['all_results']):,.0f} MXN")
        print(f"  Máximo gastado     : ${max(r['avg_spent_per_collector_mxn'] for r in results['all_results']):,.0f} MXN")

    print("\n Generando visualizaciones...")
    plot_simulation_results(all_scenario_results)


if __name__ == "__main__":
    main()