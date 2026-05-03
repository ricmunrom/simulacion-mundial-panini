# analysis/visualizer.py

import os
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import numpy as np

OUTPUT_DIR = "output"


def plot_simulation_results(all_scenario_results: list):
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    _plot_distribution(all_scenario_results)
    _plot_savings(all_scenario_results)
    _plot_diminishing_returns(all_scenario_results)
    _plot_straggler(all_scenario_results)
    _plot_spending_by_position(all_scenario_results)


def _plot_distribution(all_scenario_results: list):
    """Histograma de distribución del gasto por persona por escenario."""
    fig, axes = plt.subplots(2, 3, figsize=(18, 8))
    axes = axes.flatten()
    fig.suptitle("Distribucion del gasto por persona segun escenario (Monte Carlo)",
                 fontsize=13, fontweight="bold")

    colors = ["#2E86AB", "#A23B72", "#F18F01", "#C73E1D", "#3B1F2B", "#44BBA4"]

    for ax, scenario, color in zip(axes, all_scenario_results, colors):
        n = scenario["num_collectors"]
        spent_list = [r["avg_spent_per_collector_mxn"] for r in scenario["all_results"]]
        avg = scenario["avg_spent_per_collector_mxn"]

        ax.hist(spent_list, bins=40, color=color, edgecolor="white", alpha=0.85)
        ax.axvline(avg, color="black", linestyle="--", linewidth=1.5,
                   label=f"Promedio: ${avg:,.0f}")
        ax.set_title(f"{n} coleccionador{'es' if n > 1 else ''}", fontsize=10)
        ax.set_xlabel("Gasto por persona (MXN)", fontsize=8)
        ax.xaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f"${x:,.0f}"))
        ax.tick_params(axis="x", labelsize=7, rotation=30)
        ax.legend(fontsize=8)

    plt.tight_layout()
    plt.savefig(f"{OUTPUT_DIR}/distribucion_gasto.png", dpi=150, bbox_inches="tight")
    plt.close()


def _plot_savings(all_scenario_results: list):
    """Ahorro absoluto y porcentual vs coleccionador solo."""
    base = all_scenario_results[0]["avg_spent_per_collector_mxn"]
    labels = [str(r["num_collectors"]) for r in all_scenario_results]
    averages = [r["avg_spent_per_collector_mxn"] for r in all_scenario_results]
    savings_abs = [base - avg for avg in averages]
    savings_pct = [(s / base) * 100 for s in savings_abs]

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(13, 5))
    fig.suptitle("Ahorro por coleccionador adicional vs ir solo", 
                 fontsize=13, fontweight="bold")

    # Ahorro absoluto
    bars = ax1.bar(labels, savings_abs, color="#2E86AB", edgecolor="white", width=0.5)
    ax1.set_title("Ahorro absoluto por persona (MXN)")
    ax1.set_xlabel("Numero de coleccionadores")
    ax1.set_ylabel("MXN ahorrados")
    ax1.bar_label(bars, fmt="$%.0f", padding=4, fontsize=9)
    ax1.yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f"${x:,.0f}"))

    # Ahorro porcentual
    bars2 = ax2.bar(labels, savings_pct, color="#F18F01", edgecolor="white", width=0.5)
    ax2.set_title("Ahorro porcentual por persona vs ir solo")
    ax2.set_xlabel("Numero de coleccionadores")
    ax2.set_ylabel("% ahorrado")
    ax2.bar_label(bars2, fmt="%.1f%%", padding=4, fontsize=9)
    ax2.set_ylim(0, max(savings_pct) * 1.2)

    plt.tight_layout()
    plt.savefig(f"{OUTPUT_DIR}/ahorro.png", dpi=150, bbox_inches="tight")
    plt.close()


def _plot_diminishing_returns(all_scenario_results: list):
    """Curva de rendimientos decrecientes del gasto promedio por persona."""
    n_collectors = [r["num_collectors"] for r in all_scenario_results]
    averages = [r["avg_spent_per_collector_mxn"] for r in all_scenario_results]
    marginal = [0] + [averages[i-1] - averages[i] for i in range(1, len(averages))]

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(13, 5))
    fig.suptitle("Rendimientos decrecientes del intercambio", 
                 fontsize=13, fontweight="bold")

    # Curva de gasto
    ax1.plot(n_collectors, averages, marker="o", color="#2E86AB", 
             linewidth=2.5, markersize=8)
    for x, y in zip(n_collectors, averages):
        ax1.annotate(f"${y:,.0f}", (x, y), textcoords="offset points",
                     xytext=(0, 12), ha="center", fontsize=9)
    ax1.set_title("Gasto promedio por persona segun grupo")
    ax1.set_xlabel("Numero de coleccionadores")
    ax1.set_ylabel("Gasto promedio (MXN)")
    ax1.set_xticks(n_collectors)
    ax1.yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f"${x:,.0f}"))
    ax1.grid(axis="y", linestyle="--", alpha=0.4)

    # Ahorro marginal
    ax2.bar(n_collectors, marginal, color="#A23B72", edgecolor="white", width=0.5)
    ax2.bar_label(ax2.containers[0], fmt="$%.0f", padding=4, fontsize=9)
    ax2.set_title("Ahorro marginal por cada coleccionador extra")
    ax2.set_xlabel("Coleccionador numero N agregado")
    ax2.set_ylabel("MXN ahorrados vs N-1")
    ax2.set_xticks(n_collectors)
    ax2.yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f"${x:,.0f}"))
    ax2.grid(axis="y", linestyle="--", alpha=0.4)

    plt.tight_layout()
    plt.savefig(f"{OUTPUT_DIR}/rendimientos_decrecientes.png", dpi=150, bbox_inches="tight")
    plt.close()


def _plot_straggler(all_scenario_results: list):
    """Historia del rezagado — sobres extra que compro solo al final."""
    multi = [r for r in all_scenario_results if r["num_collectors"] > 1]

    if not multi:
        return

    n_collectors = [r["num_collectors"] for r in multi]
    avg_behind = [r["avg_rounds_behind"] for r in multi]
    max_behind = [r["max_rounds_behind"] for r in multi]

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(13, 5))
    fig.suptitle("El costo de ser el rezagado", fontsize=13, fontweight="bold")

    # Sobres extra promedio
    bars = ax1.bar([str(n) for n in n_collectors], avg_behind,
                   color="#C73E1D", edgecolor="white", width=0.5)
    ax1.bar_label(bars, fmt="%.1f sobres", padding=4, fontsize=9)
    ax1.set_title("Sobres extra promedio que compro solo el rezagado")
    ax1.set_xlabel("Numero de coleccionadores en el grupo")
    ax1.set_ylabel("Sobres extra")
    ax1.grid(axis="y", linestyle="--", alpha=0.4)

    # Distribucion de sobres extra por escenario
    data = []
    labels = []
    for r in multi:
        behind_list = [sim["rounds_behind"] for sim in r["all_results"]]
        data.append(behind_list)
        labels.append(str(r["num_collectors"]))

    ax2.violinplot(data, positions=range(len(data)), showmedians=True)
    ax2.set_xticks(range(len(labels)))
    ax2.set_xticklabels(labels)
    ax2.set_title("Distribucion de sobres extra del rezagado")
    ax2.set_xlabel("Numero de coleccionadores en el grupo")
    ax2.set_ylabel("Sobres extra")
    ax2.grid(axis="y", linestyle="--", alpha=0.4)

    plt.tight_layout()
    plt.savefig(f"{OUTPUT_DIR}/rezagado.png", dpi=150, bbox_inches="tight")
    plt.close()

def _plot_spending_by_position(all_scenario_results: list):
    """Gasto promedio por posicion de completion dentro del grupo."""
    multi = [r for r in all_scenario_results if r["num_collectors"] > 1]

    if not multi:
        return

    n_scenarios = len(multi)
    fig, axes = plt.subplots(1, n_scenarios, figsize=(20, 5), sharey=False)
    if n_scenarios == 1:
        axes = [axes]

    fig.suptitle("Gasto promedio por posicion de completion dentro del grupo",
                 fontsize=13, fontweight="bold")

    colors = ["#2E86AB", "#A23B72", "#F18F01", "#C73E1D", "#3B1F2B", "#44BBA4"]

    for ax, scenario, color in zip(axes, multi, colors):
        n = scenario["num_collectors"]
        positions = [f"pos_{i+1}" for i in range(n)]
        labels = ["1ro", "2do", "3ro", "4to", "5to", "6to"][:n]

        avg_spent = []
        for pos in positions:
            values = [r["spent_by_position"][pos] for r in scenario["all_results"]]
            avg_spent.append(sum(values) / len(values))

        bars = ax.bar(labels, avg_spent, color=color, edgecolor="white", alpha=0.85, width=0.5)
        ax.bar_label(bars, fmt="$%.0f", padding=4, fontsize=8)
        ax.set_title(f"{n} coleccionadores", fontsize=10)
        ax.set_xlabel("Posicion en terminar")
        ax.set_ylabel("Gasto promedio (MXN)")
        ax.yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f"${x:,.0f}"))
        ax.grid(axis="y", linestyle="--", alpha=0.4)

    plt.tight_layout()
    plt.savefig(f"{OUTPUT_DIR}/gasto_por_posicion.png", dpi=150, bbox_inches="tight")
    plt.close()