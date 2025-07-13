from game import Game
from stats import SolverStats
import matplotlib.pyplot as plt
import csv
import copy

# 🎯 Parámetros editables en un solo lugar
HEIGHT = 16
WIDTH = 16
BOMBS = 40
PARTIDAS = 100

def run_comparativa_solvers(n_partidas, output_filename_clasico, output_filename_enhanced):
    stats_clasico = SolverStats()
    stats_enhanced = SolverStats()

    # Para comparación directa
    enhanced_mejor = 0
    clasico_mejor = 0
    empates = 0

    for _ in range(n_partidas):
        game_base = Game(height=HEIGHT, width=WIDTH, bomb_number=BOMBS)

        game_clasico = Game(HEIGHT, WIDTH, BOMBS, saved_field=copy.deepcopy(game_base.field), use_enhanced_solver=False)
        game_enhanced = Game(HEIGHT, WIDTH, BOMBS, saved_field=copy.deepcopy(game_base.field), use_enhanced_solver=True)

        game_clasico.RevealFirstCell()
        while not game_clasico.GameIsOver() and not game_clasico.game_is_over_:
            game_clasico.NextSolved(stats=stats_clasico)
        revealed_c = len(game_clasico.field.GetRevealedCells())
        victoria_c = revealed_c >= HEIGHT * WIDTH - BOMBS
        stats_clasico.register_game(victoria_c)

        game_enhanced.RevealFirstCell()
        while not game_enhanced.GameIsOver() and not game_enhanced.game_is_over_:
            game_enhanced.NextSolved(stats=stats_enhanced)
        revealed_e = len(game_enhanced.field.GetRevealedCells())
        victoria_e = revealed_e >= HEIGHT * WIDTH - BOMBS
        stats_enhanced.register_game(victoria_e)

        if victoria_c and not victoria_e:
            clasico_mejor += 1
        elif victoria_e and not victoria_c:
            enhanced_mejor += 1
        else:
            empates += 1

    stats_clasico.save_to_csv(output_filename_clasico)
    stats_enhanced.save_to_csv(output_filename_enhanced)

    print("\n===== Solver Clásico =====")
    stats_clasico.print_summary()

    print("\n===== EnhancedSolver =====")
    stats_enhanced.print_summary()

    print("\n===== Comparación directa (partida por partida) =====")
    print(f"Enhanced ganó y clásico perdió: {enhanced_mejor}")
    print(f"Clásico ganó y enhanced perdió: {clasico_mejor}")
    print(f"Empates (ambos ganan o pierden): {empates}")

    return stats_clasico, stats_enhanced

def read_csv(filename):
    with open(filename, newline='') as csvfile:
        reader = csv.reader(csvfile)
        next(reader)  # Saltar cabecera
        return {rows[0]: float(rows[1]) for rows in reader}

def comparar_solvers():
    print("=== Ejecutando comparativa con tableros compartidos ===")
    run_comparativa_solvers(
        n_partidas=PARTIDAS,
        output_filename_clasico="resultados_solver.csv",
        output_filename_enhanced="resultados_enhanced_solver.csv"
    )

    # 📊 Visualización
    classic = read_csv("resultados_solver.csv")
    enhanced = read_csv("resultados_enhanced_solver.csv")

    labels = ["Precision (%)", "Win Rate (%)"]
    x = range(len(labels))
    classic_vals = [classic[label] for label in labels]
    enhanced_vals = [enhanced[label] for label in labels]

    # Gráfico de barras
    plt.figure(figsize=(8, 5))
    bars1 = plt.bar([i - 0.2 for i in x], classic_vals, width=0.4, label="Solver Clásico")
    bars2 = plt.bar([i + 0.2 for i in x], enhanced_vals, width=0.4, label="EnhancedSolver")
    plt.xticks(x, labels)
    plt.ylabel("Porcentaje")
    plt.title(f"Comparación con tamaño {WIDTH}x{HEIGHT}, {BOMBS} bombas")
    plt.legend()

    # Añadir valores encima de las barras
    for bar in bars1 + bars2:
        height = bar.get_height()
        plt.text(bar.get_x() + bar.get_width()/2.0, height + 0.5, f'{height:.2f}', ha='center', va='bottom', fontsize=8)

    plt.tight_layout()
    plt.savefig("comparacion_solvers.png")
    print(" Gráfico guardado como comparacion_solvers.png")

if __name__ == "__main__":
    comparar_solvers()
    print(" Comparación finalizada")
